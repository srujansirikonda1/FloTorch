# New Features

## Version 2.0

### SageMaker Embed and Retrieval Models Integration
Added support for SageMaker Embed and Retrieval Models, enabling seamless integration with AWS SageMaker services for embedding generation and retrieval tasks.

### Guardrails Functionality
Implemented Guardrails to enhance the safety and reliability of system outputs, ensuring adherence to predefined constraints and reducing risks in generated responses.

### Evaluation Metrics
Introduced Evaluation Metrics to measure and assess the performance of models and experiments effectively. These metrics provide deeper insights for optimization and decision-making.

---

# Bug Fixes
- Fixed count mismatch in valid experiments and the selected experiments page.
- Added UI validation messages for input fields.
- Added form validation for Fixed Chunking and Hierarchical Chunking fields.

---

# Enhancements
- Added a drag-and-drop interface for uploading multiple files with validation and preview support.
- Introduced a new **Guardrails and Evaluation** tab with a magnifying glass icon, relocated the Guardrails UI to this tab, and included a link to the AWS Guardrails Console for improved accessibility.
- Updated the interface by:
  - Adding **Fixed Chunking Settings** and **Hierarchical Chunking Settings** as headings inside respective boxes.
  - Removing "Hierarchical" from the labels within the boxes and refining the design for clarity.
- Updated the reranking model dropdown to display a note: *"Re-ranking is not supported in the US East (us-east-1) region"* when this region is selected.
- Made UI updates and enhanced tooltip information.
- Renamed "Embedding LLM" to "Embedding Model."
- Added a "Tokens" label beside chunk size labels for both Fixed and Hierarchical Chunking.
- Disabled ranking selection when the region is set to "us-east-1."
- Added the "None" option for Guardrails and renamed "Sync Guardrails" to "Fetch Guardrails" on the button label.
- Included an AWS Guardrails link in the **Guardrails and Evaluation** tab.
- Made "Guardrails" and "Evaluation" tab options in the service dropdown unselectable.
- Added a modal pop-up for directional pricing when clicking valid experiments on the page.
- Enabled sorting for all columns and tables.
- Reordered table columns.
- Updated the **Experiment Details** page to include SageMaker model and type in the header section.
- Enhanced the **Breakdown** tab on the Experiment Details page with valid labels and values.
- Added three tabs: **Question Metrics**, **Details**, and **Breakdown** in Experiment Question Metrics.
- Displayed a popup with a detailed cost estimate breakdown when hovering over the directional price in the **Valid Experiments** table.

---

# Upgrading

## Known Issues
### Missing Exception Handling
- Uploading a corrupted PDF file to the Knowledge Base does not throw the expected error.

### Project Status Management
- If a Step Function aborts or times out mid-project, the system fails to update the project status, requiring manual intervention.

### Input Length Limit for LLM
- The `llm-falcon-7b-instruct-bf16` model has an input length limit of 1024 tokens. Questions exceeding this limit fail to generate an answer.

### Fetching Valid Experiments with Large Datasets
- Valid experiments cannot be fetched when all parameters and combinations are selected with a large dataset.

### NAN Values in Evaluation Metrics
- NAN values are being populated for Faithfulness and Answer Relevancy metrics during evaluations.

### UI Validation Issues
- Some input fields lack proper UI validations.

### Directional Pricing Discrepancy
- Directional pricing displays a lower value, even when the estimated cost is higher.

### Incorrect Experiment Status
- Some experiments are incorrectly marked as "Complete" despite failures.

### Titan Embeddings G1 Model Cost Issue
- The Titan Embeddings G1 model shows an estimated cost of $0 in evaluation metrics.

### Answer Generation Failure
- Experiments fail to generate answers when using a large parent chunk size with a higher number of parent chunks for retrieval.

### Mismatch in Generated vs. Ground Truth Answers
- Generated answers do not match ground truth answers, requiring rephrasing and formatting improvements.

### Issue with Experiment Time Calculation
- The total time for the experiment is displayed incorrectly in the downloaded results.

### Delayed Validation Messages for Chunking Fields
- Validation messages for chunking and Fixed fields appear only after all other mandatory fields are filled and the "Next" button is clicked again.

### Cost Discrepancies in Pricing for Experiments
- Users may encounter inconsistencies in the displayed pricing for individual experiments.

### Token Limit Issues
- **Titan Text G1 - Lite Model:** Maximum token length is 4096. Inputs exceeding this limit result in an error.
- **tiiuae/falcon-7b-instruct Model:** Maximum token length is 1024. Inputs exceeding this limit result in an error.
