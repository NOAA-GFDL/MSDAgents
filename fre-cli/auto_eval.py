from pathlib import Path
from typing import Dict
import yaml
import json
import sys
import subprocess

def main():
    BASELINE_FILE = Path("fre_groundtruth.yaml")
    #$ Parse the BASELINE_FILE yaml and store as a dictionary called groundtruth_yaml
    with BASELINE_FILE.open("r", encoding="utf-8") as f:
        groundtruth_yaml: Dict[str, str] = yaml.safe_load(f)

    #needed for lauren's logger
    OUTPUT_FILE = Path("fre_chatbot.yaml")
    #Dictionary to store logs for lauren
    bot_responses: Dict[str, str]= {}

    for user_question in groundtruth_yaml.keys():
        response = subprocess.run(
            [sys.executable, "fre_cli_chatbot/frontend.py", "query", user_question],
            capture_output=True,
            text=True,
            check=True
        )
        #needed for lauren's logger
        bot_responses[user_question] = response.stdout

    # Outside of the LLM loop, aggregate evaluation results
    # This should be replaced by the logger
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        yaml.dump(
            bot_responses,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
    


if __name__ == "__main__":
    main()
