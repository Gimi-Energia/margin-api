from ninja import NinjaAPI, Redoc

from apps.icms.api import icms_router

api = NinjaAPI(
    csrf=False,
    title="Margin API",
    version="1.0.0",
    description="This is a API to manage profit margin data",
)

api.add_router("/icms", icms_router, tags=["ICMS"])
