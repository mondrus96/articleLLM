import os
os.chdir("/Users/martin/Documents/HealthTech/article_gen")

from helper.get_gspread import get_gspread
from helper.scrape_page import scrape_page
from config.state import WritingState
from llmflow.graph import build_graph
import json

# Load JSON data from a file into a dictionary
with open("config/gspread_locs.json", "r") as file:
    gspread_locs = json.load(file)  # Parse JSON into a Python dictionary

# Pull data
df = get_gspread(gspread_locs)
links = df["Links"][2]; notes = df["Notes"][2]; prompt = df["Prompt"][2]
links = links.split()
scraped = '\n'.join(
    f"Article {i+1}:\n---\n{scrape_page(link).strip()}\n---"
    for i, link in enumerate(links)
)

init_state = WritingState(
    scraped=scraped,
    notes=notes,
    cleaned="",
    summarized="",
    full="",
    short=""
)

# Create the StateGraph and add nodes
app = build_graph()
result = app.invoke(init_state)

# Set up a memory-based checkpointer
memory = MemorySaver()

# Compile the graph with the checkpointer
app = graph.compile(checkpointer=memory)

# Define the thread configuration
thread_config = {"configurable": {"thread_id": "1"}}

# Provide an initial state and invoke the graph
result = app.invoke(init_state, thread=thread_config)


# Thread configuration
config = {"configurable": {"thread_id": "1"}}

# Stream through the graph and print events
for event in app.stream(init_state, config=config, stream_mode="values"):
    print("Event:", event)



graph.add_node("GenerateDraft", clean_scraped)
graph.add_node("SummarizeDraft", summary)
graph.add_node("FixGrammar", fix_grammar)

# Define the workflow's structure
graph.set_entry_point("GenerateDraft")
graph.add_edge("GenerateDraft", "SummarizeDraft")
graph.add_edge("SummarizeDraft", "FixGrammar")
graph.add_edge("FixGrammar", END)

# 5. Compile and run the graph
app = graph.compile()
result = app.invoke({"topic": "How to use LangGraph"})

from langchain_core.runnables.graph import MermaidDrawMethod

# Generate the PNG using Mermaid API
png_data = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

# Save the PNG to a file
with open("langgraph_workflow.png", "wb") as f:
    f.write(png_data)

# 6. Output the final result
print(result)