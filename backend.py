from fastapi import FastAPI, requests
from pydantic import BaseModel
import uvicorn
import uuid
from langchain_core.messages import HumanMessage,ToolMessage
from agent import getAgent
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

user_sessions={}

class query(BaseModel):
    user_query:str
    session_id:str
    

@app.get("/")
def check():
    return {"status":"Up and running"}    

@app.post('/query')
def agent(req: query):
    print(req.user_query)
    session_id = req.session_id
    if session_id not in user_sessions:
        user_sessions[session_id] = []
    user_sessions[session_id].append(HumanMessage(content=req.user_query))
    if(len(user_sessions)>6):
        oldest_key = list(user_sessions.keys())[0]
        user_sessions.pop(oldest_key)
    inputs = {"messages": user_sessions[session_id]}
    print("*"*100)
    print(inputs["messages"])
    print("*"*100)
    # inputs={"messages" : [HumanMessage(content=req.user_query)]}
    result=getAgent(inputs)
    user_sessions[session_id].append(result["messages"][-1])
    if isinstance(result["messages"][-2],ToolMessage):
        table=result["messages"][-2]
        user_sessions[session_id].append(table)
    else:
        table={"content":[]}
    # return {"hello":"hello"}
    return {"status":"success","table":table,"AI":result["messages"][-1]}

if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8080)