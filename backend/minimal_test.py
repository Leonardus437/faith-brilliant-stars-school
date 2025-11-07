from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.user import User
import uvicorn

app = FastAPI()

@app.post("/test-login")
async def test_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        print(f"Attempting login for: {form_data.username}")
        user = db.query(User).filter(User.email == form_data.username).first()
        
        if not user:
            print("User not found")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        print(f"User found: {user.email}, Active: {user.is_active}")
        
        if not verify_password(form_data.password, user.hashed_password):
            print("Password verification failed")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
        
        print("Password verified successfully")
        
        if not user.is_active:
            print("User is inactive")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
        
        access_token = create_access_token({"sub": str(user.id), "role": user.role})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role
            }
        }
    except Exception as e:
        print(f"Error in login: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)