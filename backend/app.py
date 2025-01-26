from fastapi import FastAPI
from langserve import add_routes
from langgraph.graph import Graph
from langchain_core.runnables import RunnableLambda

from langchain_groq import ChatGroq

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


llm = ChatGroq(temperature=0, model_name= "llama-3.3-70b-versatile")


def chatbot(state: State):
    message = [llm.invoke(state["messages"])]
    return {"messages": message}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
workflow = graph_builder.compile()

app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

add_routes(app, workflow, path="/langgraph")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
