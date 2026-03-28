from fastapi import APIRouter, FastAPI
from router import router as main_router


app = FastAPI(
    title="Pokestral AI API",
    description="API for interacting with the Pokestral AI.",
    version="1.0.0"
)

router = APIRouter(prefix="/api/agents")
router.include_router(main_router)

app.include_router(router)