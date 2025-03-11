import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints import auth, users, products, categories, cart, orders, admin
from app.core.config import settings
from app.services.caches.rate_limiter import RateLimiterMiddleware

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

app.add_middleware(RateLimiterMiddleware)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)
