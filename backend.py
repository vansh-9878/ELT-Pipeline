from fastapi import FastAPI, requests
from pydantic import BaseModel
import uvicorn
from langchain_core.messages import HumanMessage 
from agent import getAgent


app=FastAPI()

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
    return {"status":"success","table":result["messages"][-2],"AI":result["messages"][-1]}

if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8080)