from fastapi import FastAPI
from fastapi import Request, UploadFile, Body, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from opensearch import OpenSearchConnection
import tempfile
from traceback import format_exc
import time
from bitahoycloud import get_auth_token, poll_blocked_domains
import asyncio


app = FastAPI(docs_url=None)



templates = Jinja2Templates(directory="html")


@app.get("/")
async def home(request: Request):
	return templates.TemplateResponse("landing.html",{"request":request, "title": "Integrations", "bitahoy": app.counter[0]})

@app.post("/bitahoy")
async def bitahoy(email: str = Form(), password: str = Form(), action: str = Form()):
    print(f"{email} {password} {action}")
    if action == "start":
        token = await get_auth_token(email, password)
        app.task = asyncio.create_task(poll_blocked_domains(token, app.opensearchconnection, app.counter))
        def callback(t):
            print("task cancelled")
            app.task = None
            app.counter = [0]
        app.task.add_done_callback(callback)
    if action == "stop":
        if app.task:
            app.task.cancel()
            app.task = None
            app.counter = [0]
    return RedirectResponse(url="/", status_code=302)

@app.post("/upload/pcap")
async def upload_pcap(request: Request, file: UploadFile, index: str = Body()):
    success = True
    try:
        import imports
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(file.file.read())
            fp.seek(0)
            result = await imports.Imports(app.opensearchconnection).importFromPcap(fp.name, f"{index}-{int(time.time())}")
    except:
        result = format_exc()
        success = False
    return templates.TemplateResponse("upload_pcap.html",{"request":request, "filename":file.filename  + " -> " + f"{index}-{int(time.time())}", "title": "Upload PCAP", "output": result, "success": success})


@app.post("/upload/csv")
async def upload_csv(request: Request, file: UploadFile, index: str = Body()):
    success = True
    try:
        import imports
        result = await imports.Imports(app.opensearchconnection).importFromCsv(file.file.read().decode(), f"{index}-{int(time.time())}")
    except:
        result = format_exc()
        success = False
    return templates.TemplateResponse("upload_pcap.html",{"request":request, "filename":file.filename  + " -> " + f"{index}-{int(time.time())}", "title": "Upload CSV", "output": result, "success": success})


@app.on_event("startup")
async def startup():
    app.counter = [None]
    app.opensearchconnection = OpenSearchConnection('https://admin:admin@opensearch-cluster-master:9200/')
    app.task = None
    
    print("Finished startup co-routine")