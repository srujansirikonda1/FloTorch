# Using the FloTorch Application for RAG Evaluation

After you login to the App Runner instance hosting the FloTorch UI application, you will be greeted with a Welcome Page.

## Welcome Page

Upon accessing FloTorch, you are greeted with a welcome page. Click ‘Get started’ to initiate your first project.

---

## Viewing Projects

You’ll be taken to the "Projects" section to view all existing projects.  
Each project is listed with details such as ID, Name, Region, Status, and Date of completion or initiation.  
**Example ID**: `5GM2E`

---

## Creating a New Project

When creating a new project, you'll go through three main steps where you'll need to specify the necessary settings and options for your project.

You will also have the option to use a previously saved configuration file if you have one. Simply click on 'Upload config' and select a valid JSON file with all necessary parameters. The application will automatically load these parameters and display the available experiments you can run. If you don't have a configuration file, please proceed with manual setup.

### Data Strategy

- Click on "Create Project" to start a new project.
- Fill in required fields such as **Project Name**, **Region**, **Knowledge Base Data**, and **Ground Truth Data**.

### Indexing Strategy

In this page, you’ll be configuring experiment indexing-related settings. Define experiment parameters, including:

- **Chunking Strategy**
- **Vector Dimension**
- **Chunk Size**
- **Chunk Overlap Percentage**
- **Indexing Algorithm** (e.g., HNSW)
- **Embedding Model** (e.g., Titan Embeddings V2 - Text)

### Retrieval Strategy

In this page, you’ll be configuring experiment retrieval-related settings. Define the parameters:

- **N shot prompt**; provide a shot prompt file if you’re going with non-zero shot prompt.
- **KNN**
- **Inferencing LLM**
- **Inferencing LLM Temperature**

Once these are selected, all the valid configurations will be displayed on the next page based on the choices you’ve made.

You will have the option to save the valid configurations by clicking the ‘Download config’ button.

Please review the configurations and select all the experiments that you’d like to run by marking the checkboxes and click ‘Run’. Now all the experiments you had marked will be displayed on a table, review it and click ‘Confirm’ to start the experiments.

You’ll now be taken back to the projects page where you can monitor the status of experiments.

Each experiment is tracked by ID, embedding model used, indexing algorithm, and other parameters.  
**Example statuses** include "Not Started", "In Progress", “Failed” or "Completed".

If you select an experiment that is in progress, you’ll be able to view its status in the experiment table.  
**Statuses** include:

- "Not started"
- "Indexing in progress"
- "Retrieval in progress"
- "Completed"

---

## Evaluation

Once an experiment is completed, an evaluation will be run based on a few metrics and the results will be displayed in the experiment table along with directional pricing and the duration.  
The evaluation metrics include:

- **Faithfulness**
- **Context Precision**
- **Aspect Critic**
- **Answer Relevancy**

If you’d like to see the answers the model generated, you can click on the experiment ID to view them along with the questions and the ground truth answers.

You’ll also have the option to view all the parameters of the experiment configuration; click the ‘details’ button on the same page.