from fastapi import FastAPI
from .routers import users, auth, cart, products

app = FastAPI(title="Mana's-commerce API")

# Include routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(products.router)
