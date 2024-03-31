import os
import sys
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
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
        "index.html", {"request": request, "prefix": prefix}
    )


@app.get("/favicon.ico", response_class=HTMLResponse)
async def favicon_ico(request: Request):
    return Response(content=b"", media_type="image/x-icon")


@app.get("/logging", response_class=HTMLResponse)
async def uvicorn_logging(request: Request):
    try:
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
        log_file_path = os.path.join(application_path, "Serverlog", "server.log")
        if os.path.exists(log_file_path):
            with open(log_file_path, "rb") as log:
                log_read = log.read()
                return Response(content=log_read, media_type="text/plain")
        else:
            return Response(
                content="Die Serverlog-Datei wurde nicht gefunden.",
                media_type="text/plain",
            )
    except Exception as e:
        return Response(content=str(e), media_type="text/plain")


@app.get("/remove_logging")
async def remove_logging(request: Request):
    try:
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
        log_file_path = os.path.join(application_path, "Serverlog", "server.log")
        if os.path.exists(log_file_path):
            with open(log_file_path, "w"):
                pass
        else:
            return Response(
                content="Die Serverlog-Datei wurde nicht gefunden.",
                media_type="text/plain",
            )
    except Exception as e:
        return Response(content=str(e), media_type="text/plain")


@app.get("/exit")
async def server_exit(request: Request):
    import os
    import signal

    os.kill(os.getpid(), signal.SIGINT)
