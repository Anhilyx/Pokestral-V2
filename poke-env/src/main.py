from fastapi import APIRouter, FastAPI
from routers import create, look, act
from scalar_fastapi import get_scalar_api_reference


# Initialize FastAPI app
app = FastAPI(
    title="PokeEnv API",
    description="API used in Pokestral to bridge between the AI and Pokemon Showdown.",
    version="1.0.0",

    docs_url="/api/poke-env/docs/swagger",
    redoc_url="/api/poke-env/docs/redoc",
    openapi_url="/api/poke-env/docs.json"
)

# Define API routes
router = APIRouter(prefix="/api/poke-env")
router.include_router(create.router)
router.include_router(look.router)
router.include_router(act.router)

# Define docs
@router.get("/docs", include_in_schema=False)
@router.get("/docs/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url="/api/poke-env/docs.json")

# Start the app
app.include_router(router)