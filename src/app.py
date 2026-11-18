
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.rag.query_rag import load_rag_assets, rag_answer


index_state = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global index_state

    print("=== Загрузка RAG-системы ===")
    index_state = load_rag_assets()
    print("=== Система успешно загружена ===")

    yield

    print("=== Остановка сервера ===")


app = FastAPI(title="Doc Assistant", lifespan=lifespan)


class Query(BaseModel):
    question: str = Field(..., description="Вопрос к базе документов")
    k: int = Field(default=3, ge=1, le=10)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(q: Query):
    if not q.question.strip():
        raise HTTPException(status_code=400, detail="Пустой вопрос")

    start_time = time.time()

    answer, sources = rag_answer(
        q.question,
        index_state,
        k=q.k
    )

    elapsed_time = time.time() - start_time

    print(f"Запрос обработан за {elapsed_time:.4f} сек.")

    return {
        "answer": answer,
        "sources": sources,
        "metrics": {
            "execution_time_seconds": round(elapsed_time, 2)
        }
    }
