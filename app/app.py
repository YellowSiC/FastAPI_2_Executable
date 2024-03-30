from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(Path(__file__).parent / "../templates")

static_files = StaticFiles(
    directory=(Path(__file__).parent / "../static").resolve(),
    follow_symlink=True,
)
app.mount("/static", static_files, name="static")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    prefix = request.headers.get(
        "X-Forwarded-Prefix", request.scope.get("root_path", "")
    )
    return templates.TemplateResponse(
        request=request, name="index.html", context={"prefix": prefix}
    )


@app.get("/favicon.ico", response_class=HTMLResponse)
async def favicon_ico(request: Request):
    pass


@app.get("/logging", response_class=HTMLResponse)
async def uvicorn_logging(request: Request):
    log_path = Path(__file__).parent / "../server.log"
    with open(log_path, "rb") as log:
        log_read = log.read()
        return log_read


@app.get("/remove_logging")
async def remove_logging(request: Request):
    log_path = Path(__file__).parent / "../server.log"
    with open(log_path, "w"):
        pass
    return Response(content="Inhalt der Datei wurde gelöscht.", media_type="text/plain")
