from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# 用户基础信息
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


# 用户创建请求
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


# 用户响应
class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# 用户登录请求
class UserLogin(BaseModel):
    username: str
    password: str


# 令牌数据
class TokenData(BaseModel):
    username: Optional[str] = None


# 令牌响应
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
