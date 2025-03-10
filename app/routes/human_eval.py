from typing import List
from pydantic import BaseModel
import logging
import asyncio

from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# Setup flotorch-core path
import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../flotorch_core")))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../flotorch-core")))
sys.path.insert(0, os.path.abspath("../flotorch-core"))


from storage.storage_provider_factory import StorageProviderFactory
from inferencer.inferencer_provider_factory import InferencerProviderFactory
from storage.db.vector.vector_storage_factory import VectorStorageFactory
from embedding.embedding_registry import embedding_registry
from retriever.retriever import Retriever
from reader.json_reader import JSONReader
from core.dynamodb import DynamoDBOperations
from inferencer import bedrock_inferencer
from FLconfig.config import get_config
from ..dependencies.database import get_experiment_db
from boto3.dynamodb.conditions import Key
from typing import List, Dict
from config.config import Config
from config.env_config_provider import EnvConfigProvider
from chunking.chunking import Chunk

from embedding.titanv2_embedding import TitanV2Embedding
from embedding.titanv1_embedding import TitanV1Embedding
from embedding.cohere_embedding import CohereEmbedding
from embedding.bge_large_embedding import BGELargeEmbedding, BGEM3Embedding, GTEQwen2Embedding

# Flotorch-core config
env_config_provider = EnvConfigProvider()
config = Config(env_config_provider)

# Flotorch config
configs = get_config()

logger = logging.getLogger(__name__)
router = APIRouter()


class ExperimentQuery(BaseModel):
    experiment_ids: List[str]
    query: str
    

def get_experiment_configs(experiment_db, experiment_ids: List[str]) -> List[Dict]:
    """
    Get the experiment configs for all experiments using their IDs.

    Args:
        experiment_db: Instance of DynamoDBOperations.
        experiment_ids (List[str]): List of experiment IDs.

    Returns:
        List[Dict]: List of JSON objects for each experiment.
    """
    experiments = []  # List to store results
    
    for experiment_id in experiment_ids:
        key_condition_expression = "id = :id"
        expression_values = {":id": experiment_id}
        
        try:
            # Query DynamoDB for the current experiment ID
            response = experiment_db.query(
                key_condition_expression=key_condition_expression,
                expression_values=expression_values
            )
            
            # Add the items to the results list
            items = response.get('Items', [])
            experiments.extend(items)  # Add all matching items to the list
            
        except Exception as e:
            print(f"Error querying DynamoDB for ID {experiment_id}: {str(e)}")
    
    return experiments

@router.post("/heval/query-experiments", tags=["heval"])
async def query_experiments(
    query: ExperimentQuery,
    experiment_db: DynamoDBOperations = Depends(get_experiment_db)
):

    num_experiments = len(query.experiment_ids)
    if not (2 <= num_experiments <= 3):
        raise HTTPException(
            status_code=400,
            detail="The number of experiment_ids must be between 2 and 3."
        )

    experiment_configs = get_experiment_configs(experiment_db, query.experiment_ids)

    async def run_experiment(exp_config_data):
        experiment_id = exp_config_data.get("id")
        exp_config = exp_config_data.get("config")

        # Common Configurations
        aws_region = exp_config.get("aws_region")
        knowledge_base = exp_config.get("knowledge_base", False)
        bedrock_knowledge_base = exp_config.get("bedrock_knowledge_base", False)

        # Inferencer Initialization
        inferencer = InferencerProviderFactory.create_inferencer_provider(
            exp_config.get("retrieval_service"),
            exp_config.get("retrieval_model"),
            aws_region,
            config.get_sagemaker_arn_role(),
            int(exp_config.get("n_shot_prompts")),
            float(exp_config.get("temp_retrieval_llm")),
            exp_config.get("n_shot_prompt_guide")
        )

        vector_storage = None
        if knowledge_base:
            vector_storage = VectorStorageFactory.create_vector_storage(
                knowledge_base=knowledge_base,
                use_bedrock_kb=bedrock_knowledge_base,
                embedding=(
                    embedding_registry.get_model(exp_config.get("embedding_model"))(
                        exp_config.get("embedding_model"), aws_region, 
                        int(exp_config.get("vector_dimension"))
                    )
                    if not bedrock_knowledge_base else None
                ),
                opensearch_host=config.get_opensearch_host(),
                opensearch_port=config.get_opensearch_port(),
                opensearch_username=config.get_opensearch_username(),
                opensearch_password=config.get_opensearch_password(),
                index_id=config.get_opensearch_index(),
                knowledge_base_id=exp_config.get("kb_data"),
                aws_region=aws_region
            )

        # Answer Generation
        if vector_storage:
            hierarchical = exp_config.get("chunking_strategy") == 'hierarchical'
            question_chunk = Chunk(data=query.query)

            vector_response = await asyncio.to_thread(
                vector_storage.search, question_chunk, exp_config['knn_num'], hierarchical
            )
            vector_response = vector_response.to_json()['result']
            metadata, answer = await asyncio.to_thread(
                inferencer.generate_text, query.query, vector_response
            )
        else:
            metadata, answer = await asyncio.to_thread(
                inferencer.generate_text, query.query
            )

        return {
            "experiment_id": experiment_id,
            "answer": answer,
            "metadata": metadata
        }

    results = await asyncio.gather(*[run_experiment(exp) for exp in experiment_configs])

    return JSONResponse(content={"results": results})
