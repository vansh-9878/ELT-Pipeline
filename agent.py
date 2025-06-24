from typing import TypedDict,Annotated,Sequence
from langgraph.graph import START,END,StateGraph
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage,ToolMessage,BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from semantic_search.query import searchDatabase
import os
from dotenv import load_dotenv
load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

@tool
def NLPtoSQL(user_query:str):
    """
        This tool is used to convert user_query to an sql query and return back the table from vector database
    """
    print("Using tool..")
    rows=searchDatabase(user_query)
    return rows

tools=[NLPtoSQL]

model=ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=os.getenv("GEMINI_API"),
    temperature=0.2
).bind_tools(tools)


def agent(state: AgentState)-> AgentState:
    print("Thinking..")
    prompt=SystemMessage("""You are an intelligent AI assistant that interacts with users, helping them retrieve and understand data. You respond naturally to user queries and can use tools when appropriate. Your responsibilities include:

    Conversational Interaction
    ‣ Respond warmly and naturally to greetings.
    ‣ Keep your tone helpful, concise, and professional.
    Smart Tool Use
    ‣ When the user asks a data-related query, use the provided tool to convert their natural language query into SQL.
    ‣ Only use the tool when it's needed — do not rely on it for casual conversation or irrelevant queries.
    Result Presentation
    ‣ When tool results are returned:
    Provide a brief natural language explanation of what the data shows.
    Optionally include a summary or insights""")
    response=model.invoke([prompt]+state["messages"])
    return {"messages":[response]}

def shouldContinue(state: AgentState)-> AgentState:
    print("Checking..")
    messages=state["messages"]
    last_message=messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


graph=StateGraph(AgentState)
graph.add_node("agent",agent)
graph.add_node("tools",ToolNode(tools))
graph.add_edge(START,"agent")
graph.add_edge("tools","agent")
graph.add_conditional_edges(
    "agent",
    shouldContinue,
    {
        "end":END,
        "continue":"tools"
    }
)

app=graph.compile()


def getAgent(inputs):
    results=app.invoke(inputs)
    print("-"*100)
    print(results["messages"][-2])
    print("-"*100)
    print(results["messages"][-1])
    return results
    
# inputs={"messages" : [HumanMessage(content="Get the average number of delivery attempts per stop for a company id company_1246")]}
# inputs={"messages" : [HumanMessage(content="Shows the earliest and latest route start dates for each company.")]}
inputs={"messages" : [HumanMessage(content="List all the stops for vehicle veh_1280")]}
# inputs={"messages" : [HumanMessage(content="Hii")]}
# getAgent(inputs)