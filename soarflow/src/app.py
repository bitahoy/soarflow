from fastapi import FastAPI


app = FastAPI(docs_url=None)



@app.get("/", status_code=200)
def status():
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    print("Finished startup co-routine")