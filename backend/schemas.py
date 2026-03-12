from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class PlatformBase(BaseModel):
    name: str
    is_active: bool = True
    config: Optional[Dict] = None

class PlatformResponse(PlatformBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SystemConfigBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

class SystemConfigResponse(SystemConfigBase):
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TargetBase(BaseModel):
    platform_id: int
    name: str
    target_url: str
    is_active: bool = True

class TargetResponse(TargetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ChannelBase(BaseModel):
    target_id: int
    name: str
    identifier: str
    language: str = "ko"
    is_private: bool = False

class ChannelResponse(ChannelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
