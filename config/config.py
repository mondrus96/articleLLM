import json
import os
from langchain_openai import ChatOpenAI

# LLM settings
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Load the prompts from the JSON file
def load_prompts() -> dict:
    with open(os.path.join(os.path.dirname(__file__), "prompts.json"), "r") as f:
        return json.load(f)