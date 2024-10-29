from config.state import WritingState
from config.config import llm
from langchain_core.messages import AIMessage
from typing import List

def process_node(state: WritingState, prompt: str, in_key: str, out_key: str) -> WritingState:
    """
    A generic function to process LLM tasks with different prompts.
    
    Parameters:
        - state (WritingState): The current state of the workflow.
        - prompt (str): The prompt to use with the LLM.
        - key (str): The key in the state to store the LLM output.

    Returns:
        - Updated state (WritingState).
    """
    input_data = state[in_key]
    if isinstance(input_data, AIMessage):
        input_data = input_data.content  # Extract the string content
    llm_out = llm.invoke(prompt + state[in_key])  # Use formatted prompt with state variables
    state[out_key] = llm_out.content if isinstance(llm_out, AIMessage) else llm_out
    return state

def main_node(state: WritingState, prompt: List[str]) -> WritingState:
    """
    A function which takes many contexts and uses them to build the main article.

    Parameters:
        - state (WritingState): The current state of the workflow.
        
    Returns:
        -Updated state (WritingState)
    """
    llm_out = llm.invoke(prompt[0] + state["summarized"] + 
                         prompt[1] + state["notes"] + prompt[2])
    state["full"] = llm_out.content
    return state