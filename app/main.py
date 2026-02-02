from fastapi import FastAPI
from .routers import users, auth, products, cart



app = FastAPI(title="FastAPI Shopping App")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)

