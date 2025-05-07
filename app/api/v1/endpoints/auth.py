from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.auth import Token, UserCreate, User,UserResponse
from app.models.user import User as UserModel
from app.db.session import get_db
from app.api.v1.dependencies import get_current_user  # Update the import path
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User  # Ensure this is the SQLAlchemy model
import bcrypt
from typing import List

from app.schemas import user as user_schema
from app.models import user as user_model

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
            db: AsyncSession = Depends(get_db),
            form_data: OAuth2PasswordRequestForm = Depends()
        ):
    # Step 1: Retrieve the user from the database using the username    
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    
    # Step 2: Verify the password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 3: Generate an access token
    access_token = create_access_token(data={"sub": user.username})
    
    # Step 4: Return the access token
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def hash_password(password: str) -> str:
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Return the hashed password as a string
    return hashed_password.decode('utf-8')

def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    print("Tests")
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,  # Use the hashed password here
        is_active=True,
        is_superuser=False,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[user_schema.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Use SQLAlchemy's select statement
    stmt = select(user_model.User).offset(skip).limit(limit)
    
    # Execute the statement asynchronously
    result = await db.execute(stmt)
    
    # Fetch all products from the result
    users = result.scalars().all()
    
    return users