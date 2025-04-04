import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.v1.endpoints import auth, cart, users, products, categories, cart_items, orders, admin, order_items, \
    shippings, reviews
from app.core.config import settings
from app.services.caches.rate_limiter import RateLimiterMiddleware

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
# app.include_router(cart_items.router, prefix="/cart_items", tags=["CartItem"])
app.include_router(order_items.router, prefix="/order_items", tags=["OrderItem"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

app.include_router(shippings.router, prefix="/shipping", tags=["Shipping"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])




def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ElectroStore API",
        version="1.0.0",
        description="Документація API для магазину електроніки",
        routes=app.routes,
    )
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"] = {
        "type": "oauth2",
        "flows": {
            "password": {
                "tokenUrl": "/auth/token",
                "scopes": {},
            }
        },
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(RateLimiterMiddleware)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)
