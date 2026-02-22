from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from model import model

prompt = """



Your job is to suggest a date idea based on the above information provided and you must return the response in the following json format. No markdown only simple json as follows:

Output JSON only with this shape:
{
  "suggestions": [
    {
      "title": "short title",
      "plan": "1-3 sentence plan",
      "why_it_fits": "1 sentence",
      "location_hint": "concise location guidance",
      "estimated_cost": "free | low | medium | high",
      "ideal_time": "morning | afternoon | evening"
    }
  ]
}
Rules:
- Output valid JSON only. No markdown.
- Use the provided distance/location context to keep travel reasonable.
- Avoid unsafe, illegal, or overly risky activities.
- Do not invent specific real-world venues or addresses.
- Respect preferences such as budget, time, outdoors, alcohol, accessibility, and dietary needs.
- Keep suggestions varied and realistic.
The information about the user, his/her match and the date requirements is provided below:
"""

class GraphState(TypedDict):
    input: str
    output: str

def llm_state(state: GraphState) -> dict:
    nums = state["input"]
    print("llm called")
    full_prompt = prompt + nums
    return {
        "output": model(full_prompt)
    }

graph = StateGraph(GraphState)
graph.add_node("llm", llm_state)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)

app = graph.compile()
def run(inp : str):
    result = app.invoke({
    "input": inp
    })
    return result

#print(run("1 and 2")['output']['content'])
