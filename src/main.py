from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .modules.users.router import router as users_router
from .modules.auth.router import router as auth_router
from .modules.dev.router import router as dev_router

app = FastAPI(title="Aunary API")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(dev_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "service": "Aunary API", "version": "0.1.0"}
