import uvicorn
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, cart, users, products, categories, orders, admin, shippings, reviews

from app.core.config import settings
from app.exceptions import TooManyRequestsException
from app.services.caches.rate_limiter import RateLimiterMiddleware

app = FastAPI()

# ✅ Додати CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # або ["*"] для тестів
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimiterMiddleware)

@app.exception_handler(TooManyRequestsException)
async def too_many_requests_handler(request: Request, exc: TooManyRequestsException):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
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


if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)
