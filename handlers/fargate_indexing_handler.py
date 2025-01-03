import json
import logging

from config.config import Config
from core.service.experimental_config_service import ExperimentalConfigService
from indexing.indexing import Indexer
from task_processor import FargateTaskProcessor

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class IndexingProcessor(FargateTaskProcessor):

    def __init__(self):
        super().__init__()
        self.indexer = Indexer()

    def process(self):
        try:
            logger.info("Input data: %s", self.input_data)
            exp_config_data = self.input_data
            logger.info("Into indexing processor. Processing event: %s", json.dumps(exp_config_data))

             # Load base configuration
            config = Config.load_config()
            
            exp_config = ExperimentalConfigService(config).create_experimental_config(exp_config_data)
            logger.info("Into indexing processor. Processing event: %s", json.dumps(exp_config_data))
                
            self.indexer.chunk_embed_store(config, exp_config)

            self.send_task_success({  
                "status": "success"
            })

        except Exception as e:
            logger.error(f"Error processing event: {str(e)}")
            self.send_task_failure({
                "status": "failed",
                "errorMessage": str(e)
            })


def main():
    try:
        fargate_processor = IndexingProcessor()
        fargate_processor.process()
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        raise

if __name__ == "__main__":
    main()
