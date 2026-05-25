import webbrowser
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api.v1 import sample, users, auth, components
from config.settings import get_settings
from infrastructure.database.connection import init_db

def create_app() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(sample.router, prefix="/api/v1", tags=["sample"])
    # app.include_router(users.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(components.router, prefix="/api/v1")
    # app.include_router(health.router, prefix="/api/v1", tags=["health"])
    # app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    # app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
    
    return app

app = create_app()

@app.on_event("startup")
async def startup_event():
    await init_db()
    # Open Swagger UI automatically
    # webbrowser.open_new("http://127.0.0.1:8080/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
