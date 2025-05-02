from sqlalchemy import create_engine
# from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
#from app.api.v1.endpoints import products, sales, auth, inventory_logs, cash_register, transaction, general_ledger,cash_flow, enum_type, account, journal_entry, vendor, purchase_orders
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the POS API"}
