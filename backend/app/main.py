from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import attempts, auth, courses, lessons, progress

app = FastAPI(title="FSI English Training MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(attempts.router)
app.include_router(progress.router)


@app.get("/health")
def health():
    return {"ok": True}
