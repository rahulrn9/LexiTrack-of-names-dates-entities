from fastapi import FastAPI, UploadFile, File
from fastapi import Body
from fastapi.responses import JSONResponse
from typing import Optional
import pandas as pd
from pathlib import Path
from .models import TextPayload, ExtractionResponse
from .ner import extract_entities
from .db import insert_rows

OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs"
CSV_PATH = OUTPUTS_DIR / "results.csv"

app = FastAPI(title="Xorstack Gen-AI Pipeline", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

def _persist(filename: str, rows):
    # DB
    if rows:
        insert_rows(rows)
    # CSV
    if rows:
        df = pd.DataFrame(rows)
        if CSV_PATH.exists():
            df.to_csv(CSV_PATH, mode="a", header=False, index=False)
        else:
            df.to_csv(CSV_PATH, index=False)

@app.post("/extract", response_model=ExtractionResponse)
async def extract(file: Optional[UploadFile] = File(None), payload: Optional[TextPayload] = Body(None)):
    if file is None and payload is None:
        return JSONResponse(status_code=400, content={"error": "Provide either a file or a JSON body with text."})

    if file is not None:
        content = (await file.read()).decode("utf-8", errors="ignore")
        filename = file.filename or "uploaded.txt"
    else:
        content = payload.text
        filename = payload.filename or "payload.txt"

    result = extract_entities(content, filename)
    _persist(filename, result["rows"])

    return ExtractionResponse(filename=filename, people=result["people"], dates=result["dates"])
