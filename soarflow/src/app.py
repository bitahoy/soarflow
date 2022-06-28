from fastapi import FastAPI
from fastapi import Request, UploadFile, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from opensearch import OpenSearchConnection
import tempfile
from traceback import format_exc
import time


app = FastAPI(docs_url=None)



templates = Jinja2Templates(directory="html")


@app.get("/")
async def home(request: Request):
	return templates.TemplateResponse("landing.html",{"request":request, "title": "Integrations"})


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


@app.on_event("startup")
async def startup():
    app.opensearchconnection = OpenSearchConnection('https://admin:admin@opensearch-cluster-master:9200/')
    
    print("Finished startup co-routine")