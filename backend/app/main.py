from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.data_loader.load_data import load_all_data
from backend.graph.graph_builder import build_graph
from backend.llm.query_engine import handle_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load once at startup
data = load_all_data()
graph = build_graph(data)


@app.get("/")
def root():
    return {"message": "ERP Graph System Running"}


@app.get("/query")
def query(q: str):
    result = handle_query(q, graph)
    return result

@app.get("/graph")
def get_graph():
    return {
        "nodes": graph.nodes,
        "edges": graph.edges
    }