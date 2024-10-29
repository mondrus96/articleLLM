from config.config import load_prompts
from config.state import WritingState
from langgraph.graph import StateGraph
from functools import partial
from llmflow.nodes import process_node, main_node

def build_graph():
    # Define your state graph, load prompts
    graph = StateGraph(WritingState)
    prompts = load_prompts()

    # Use partial to create specialized versions of process_node with specific prompts and keys
    gen_draft = partial(process_node, prompt=prompts["clean_scraped"], in_key="scraped", out_key="cleaned")
    sum_draft = partial(process_node, prompt=prompts["summary"], in_key="cleaned", out_key="summarized")
    short_draft = partial(process_node, prompt=prompts["post_process"], in_key="full", out_key="short")

    # Add nodes to the graph
    graph.add_node("GenDraft", gen_draft)
    graph.add_node("SumDraft", sum_draft)
    graph.add_node("MainNode", partial(main_node, prompt=prompts['main']))
    graph.add_node("ShortDraft", short_draft)

    # Define edges between the nodes
    graph.add_edge("GenDraft", "SumDraft")  # GenDraft → SumDraft
    graph.add_edge("SumDraft", "MainNode")  # SumDraft → MainNode
    graph.add_edge("MainNode", "ShortDraft")  # MainNode → ShortDraft

    # Set the entry and finish points for the graph
    graph.set_entry_point("GenDraft")  # Start with GenDraft
    graph.set_finish_point("ShortDraft")  # End with ShortDraft

    # Compile the graph
    return graph.compile()