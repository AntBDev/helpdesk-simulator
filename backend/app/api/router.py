from fastapi import APIRouter

from app.api.routes.customers import router as customers_router
from app.api.routes.devices import router as devices_router
from app.api.routes.tickets import router as tickets_router
from app.api.routes.tools import router as tools_router

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(customers_router)
api_router.include_router(devices_router)
api_router.include_router(tickets_router)
api_router.include_router(tools_router)
