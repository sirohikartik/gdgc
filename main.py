import json
from fastapi import FastAPI, HTTPException
from agent import run
from utils import get_user_by_name,get_user_matches,calculate_distance


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc
    allow_headers=["*"],  # Authorization, Content-Type, etc
)



@app.get("/")
def hello():
    return {"message":"hello"}

@app.post("/date")
def create_date_idea(username: str, budget: float, time: str, specification: str | None = None):
    user = get_user_by_name(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    match = get_user_matches(user[0]["user_id"])
    if not match:
        raise HTTPException(status_code=404, detail="No matches found for user")

    distance = calculate_distance(user[0]["latitude"], match[0]['latitude'], user[0]["longitude"], match[0]['longitude'])
    
    data = f"The complete data about user1 is {user[0]} and his/her match is {match[0]} and the distance between them is {distance} km and the budget for the date is {budget} and the time is {time} and some other specifications include {specification}"
    try:
        response = run(data)
    except Exception as e:
        raise HTTPException(status_code=500,detail="Failed to run the graph")

    raw_content = response["output"]["content"]
    clean_content = raw_content.strip().strip("`").removeprefix("json").strip()
    
    try:
        return json.loads(clean_content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse LLM response into JSON")



    

    
