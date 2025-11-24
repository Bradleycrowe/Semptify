from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import aiofiles
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

templates = Jinja2Templates(directory=TEMPLATES_DIR)

app = FastAPI(title='Semptify (FastAPI prototype)')
# Only mount static if the directory exists (avoids import-time errors in dev)
static_dir = os.path.join(BASE_DIR, 'static')
if os.path.isdir(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    # Use TemplateResponse so templates can access `request` and url_for
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/module/{name}', response_class=HTMLResponse)
async def module_view(request: Request, name: str):
    safe = name.replace('..', '')
    candidates = [f'law_notes/{safe}.html', f'modules/{safe}.html']
    for c in candidates:
        path = os.path.join(TEMPLATES_DIR, c)
        if os.path.exists(path):
            return templates.TemplateResponse(c, {'request': request})
    raise HTTPException(status_code=404, detail='Module not found')


@app.post('/api/upload')
async def upload(file: UploadFile = File(...)):
    uploads_dir = os.path.join(BASE_DIR, '..', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    out_path = os.path.join(uploads_dir, file.filename)
    # Write in chunks to avoid large memory usage
    async with aiofiles.open(out_path, 'wb') as f:
        while True:
            chunk = await file.read(1024 * 64)
            if not chunk:
                break
            await f.write(chunk)
    return {'status': 'ok', 'filename': file.filename}


@app.get('/resources', response_class=HTMLResponse)
async def resources(request: Request):
    return templates.TemplateResponse('resources.html', {'request': request})


@app.get('/health')
async def health():
    from . import db
    status = db.test_connection()
    if status.get('ok'):
        return {'status': 'ok', 'db': status}
    return {'status': 'degraded', 'db': status}

