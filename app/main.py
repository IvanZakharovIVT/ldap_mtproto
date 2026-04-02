from fastapi import FastAPI

from app.core.config import settings

from app.apps.main_app.routers import router as main_router
app = FastAPI(
    title=settings.TITLE,
    root_path='/api',
    docs_url=f'{settings.API_V1}/swagger',
    redoc_url=f'{settings.API_V1}/api-docs',
)

app.include_router(main_router)
