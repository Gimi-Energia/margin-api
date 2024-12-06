from ninja import NinjaAPI, Redoc

api = NinjaAPI(
    csrf=False,
    title="Margin API",
    version="1.0.0",
    description="This is a API to manage profit margin data",
)
