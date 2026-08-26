import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.services.advanced_boxscores import AdvancedBoxScoreService, DatasetUnavailableError
from app.data.nba_client import NBADataError
from app.data.processor import DataValidationError

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s: %(message)s")
ROOT=Path(__file__).resolve().parents[1]
app=FastAPI(title="NBA Model Dashboard",version="1.0.0")
app.mount("/static",StaticFiles(directory=ROOT/"frontend/static"),name="static")
templates=Jinja2Templates(directory=ROOT/"frontend/templates")
service=AdvancedBoxScoreService()

@app.get("/")
def root(): return {"application":"NBA Model Dashboard","page":"/advanced-boxscores"}
@app.get("/advanced-boxscores")
def page(request:Request): return templates.TemplateResponse(request,"advanced_boxscores.html")
@app.get("/api/health")
def health(): return {"status":"ok"}
@app.get("/api/advanced-boxscores")
def dataset():
    try:
        df=service.load_data(); metadata=service.load_metadata()
        df=df.where(df.notna(),None)
        return {"metadata":metadata,"data":df.to_dict(orient="records")}
    except DatasetUnavailableError as exc: raise HTTPException(404,str(exc))
@app.get("/api/advanced-boxscores/metadata")
def metadata():
    try: return service.load_metadata()
    except DatasetUnavailableError as exc: raise HTTPException(404,str(exc))
@app.get("/api/advanced-boxscores.csv")
def csv_download():
    try: service.load_data()
    except DatasetUnavailableError as exc: raise HTTPException(404,str(exc))
    return FileResponse(service.config.processed_csv,media_type="text/csv",filename=service.config.processed_csv.name)
@app.post("/api/advanced-boxscores/refresh")
def refresh():
    try: return service.refresh()
    except (NBADataError,DataValidationError) as exc: raise HTTPException(502,f"NBA data refresh failed: {exc}")
