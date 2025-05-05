from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
#from app.api.v1.endpoints import auth products,
from app.api.v1.endpoints import products, sales, auth, inventory_logs, cash_register, transaction, general_ledger,cash_flow, enum_type, account, journal_entry, vendor, purchase_orders

app = FastAPI()
# Set up CORS
# Add CORS middleware
###
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List the allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
####
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["sales"])
app.include_router(inventory_logs.router, prefix="/api/v1/inventory", tags=["inventory"])
app.include_router(cash_register.router, prefix="/api/v1/cash-register", tags=["register"])
app.include_router(transaction.router, prefix="/api/v1/transaction", tags=["transaction"])
app.include_router(general_ledger.router, prefix="/api/v1/general-ledger", tags=["general_ledger"])
app.include_router(journal_entry.router, prefix="/api/v1/journal-entries", tags=["journal_entry"])
app.include_router(cash_flow.router, prefix="/api/v1/cash_flow", tags=["cash_flow"])
app.include_router(enum_type.router, prefix="/api/v1/enum_type", tags=["enum_type"])
app.include_router(account.router, prefix="/api/v1/account", tags=["account"])
app.include_router(vendor.router, prefix="/api/v1/vendor", tags=["vendor"])
app.include_router(purchase_orders.router, prefix="/api/v1/purchase_orders", tags=["purchase_orders"])

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
