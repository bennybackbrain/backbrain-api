from fastapi import FastAPI, Query
from search_handler import search_files

app = FastAPI()

@app.get("/search-files")
def search_files_route(query: str = Query(...)):
    results = search_files(query)
    return {"results": results}