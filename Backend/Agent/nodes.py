import concurrent.futures
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Dict
from typing_extensions import TypedDict
from Agent.llms_prompt import MODELS

class GraphState(TypedDict):
    input_text: str
    results: List[Dict]

def analyze_text(state: GraphState) -> GraphState:
    results = []

    def invoke_model(model_info):
        model = ChatGoogleGenerativeAI(
            model=model_info["name"], google_api_key=model_info["api_key"]
        )      
        response = model.invoke(
            f"{model_info['task']}\nAnalyze the following input:\n{state['input_text']}"
        )
        return {"output": response}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_agent = {executor.submit(invoke_model, model_info): model_info for model_info in MODELS}
        for future in concurrent.futures.as_completed(future_to_agent):
            agent_name = future_to_agent[future]["name"]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"{agent_name} generated an exception: {exc}")
                raise Exception(f"Error occurred while processing.")
    
    state["results"] = results
    return state

def merge_results(state: GraphState) -> Dict:
    findings = state.get("results", [])
    final_report = {
        "findings": findings
    }
    return final_report