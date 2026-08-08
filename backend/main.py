from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from ml.inference.recommend import officialbaseline_query
from ml.inference.predict_piece import predict_recommendations
import pandas as pd
import numpy as np

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pd.read_csv("data/processed/processed-full.csv")
    yield
    #anything after yield runs on shutdown
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendRequest(BaseModel):
      time_period: str | None = None
      instruments: list[str] = []
      keys: list[str] = []
      mode: str | None = None
      start_year: int | None = None
      end_year: int | None = None
      start_duration: int | None = None
      end_duration: int | None = None

class PredictRequest(BaseModel):
     permlink: str
     top_n: int | None = None

@app.post("/predict")
async def predict_similar(pred: PredictRequest, request: Request):
    target = request.app.state.df[request.app.state.df["Permlink"] == pred.permlink]
    if target.empty:
        raise HTTPException(status_code=404, detail="Item not found")
    target = target.iloc[0]
    results = predict_recommendations(target, request.app.state.df, top_n = pred.top_n)
    return results.replace({np.nan: None}).to_dict(orient="records")

@app.post("/recommend")
async def send_recs(recommendation: RecommendRequest, request: Request):
     df = request.app.state.df
     results = officialbaseline_query(recommendation, request.app.state.df)
     return results.replace({np.nan: None}).to_dict(orient="records")


@app.get("/") 
async def root(request: Request):
    return {"rows": len(request.app.state.df)}