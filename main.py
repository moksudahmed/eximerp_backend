from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth
#from app.api.v1.endpoints import products, sales, auth, inventory_logs, cash_register, transaction, general_ledger,cash_flow, enum_type, account, journal_entry, vendor, purchase_orders

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the POS API"}


# ------------------------------
# For Local Testing
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
