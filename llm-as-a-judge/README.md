# LLM-as-a-Judge Evaluation Script

This directory contains a Python script (`llmjudge.py`) that uses a locally running Large Language Model (LLM) to act as an automated "judge". The script evaluates a chatbot's responses against human-generated ground truth answers using [LangChain](https://python.langchain.com/) and [Ollama](https://ollama.com/).

## Overview

`llmjudge.py` performs the following tasks:
1. **Reads Test Data**: Loads the chatbot's output log (`catalog_bot_output_log.yaml`), automatically cleaning out irrelevant HTTP request lines.
2. **Reads Ground Truth**: Loads the baseline dataset (`groundtruth.yaml`).
3. **Evaluates**: Passes the user query, ground truth answer, and chatbot answer to a local LLM (default: `nemotron-3-nano`, but can be changed) and asks it to score the response (1-10) and provide reasoning.
4. **Outputs Results**: Parses the LLM's YAML-formatted feedback and compiles it into a final output file (`llm_as_a_judge_results.yaml`).

## Prerequisites

### 1. Install Ollama & Pull the Model
Ensure you have [Ollama](https://ollama.com/) installed and running locally. You will need to pull the model you intend to use. For example:
```bash
ollama pull nemotron-3-nano
```

### 2. Install Python Dependencies
`llmjudge.py` works with the same environment as the fmscoupler and fms chatbots:
from the GFDL MSD AMD dev machine:
```bash
module load miniforge
conda create -n msdagents python=3.12 pip
conda activate msdagents
pip install -e .
```
These packages are included in this repository's pyproject.toml

## Required Input Files
`llmjudge.py` requires 2 arguments:

-g, --groundtruth: The groundtruth yaml file
-c, --chatbot, action="store", The chatbot log yaml file

And a third, optional argument:

--simplelog: Indicates to load chatbot log simply (will not be needed when the chatybot logger is available

## Output

`llmjudge.py` generates a file named `llm_as_a_judge_results.yaml` containing the score and reasoning for each evaluated query.

Example Output:
```yaml
What is the capital of France?:
  score: 10
  reasoning: The AI correctly identified Paris as the capital, which perfectly matches the ground truth.
How do I reset my password?:
  score: 1
  reasoning: The AI failed to provide the required steps to reset the password as detailed in the ground truth.
```

## Troubleshooting
* **YAML Parsing Errors:** If the LLM judge hallucinates formatting and fails to return valid YAML, the script will catch the error and dump the raw output into the results file.
* **Missing Ground Truth:** If a query in the test file is not found in the ground truth file, the script will log a warning to the console and skip evaluating that query.
