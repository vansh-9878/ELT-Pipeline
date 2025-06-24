from fastapi import FastAPI, requests
from pydantic import BaseModel
import uvicorn
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

class query(BaseModel):
    user_query:str
    

@app.get("/")
def check():
    return {"status":"Up and running"}    

@app.post('/query')
def agent(req: query):
    print(req.user_query)
    inputs={"messages" : [HumanMessage(content=req.user_query)]}
    result=getAgent(inputs)
    if isinstance(result["messages"][-2],ToolMessage):
        table=result["messages"][-2]
    else:
        table={"content":[]}
    return {"status":"success","table":table,"AI":result["messages"][-1]}

if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8080)