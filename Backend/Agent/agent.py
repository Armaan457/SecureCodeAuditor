from langgraph.graph import StateGraph
from Agent.nodes import GraphState, analyze_text, merge_results
from typing import Dict

graph = StateGraph(GraphState)
graph.add_node("analyze", analyze_text)
graph.add_node("merge", merge_results)
graph.set_entry_point("analyze")
graph.add_edge("analyze", "merge")
app = graph.compile()

def analyze_file(filename: str, content: str) -> Dict:
    try:
        state = {"input_text": content}
        result = app.invoke(state)
        return result
    except Exception as e:
        raise Exception(f"Error processing file {filename}")