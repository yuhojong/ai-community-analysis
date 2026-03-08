from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .database import get_db
from .models import Platform, CommunityTarget, Channel
from .schemas import PlatformResponse, TargetResponse, ChannelResponse, PlatformBase, TargetBase, ChannelBase
from .auth import get_current_user

router = APIRouter(prefix="/config", tags=["config"])

@router.get("/platforms", response_model=List[PlatformResponse])
async def get_platforms(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Platform))
    return result.scalars().all()

@router.post("/platforms", response_model=PlatformResponse)
async def create_platform(platform: PlatformBase, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    new_platform = Platform(**platform.dict())
    db.add(new_platform)
    await db.commit()
    await db.refresh(new_platform)
    return new_platform

@router.get("/targets", response_model=List[TargetResponse])
async def get_targets(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(CommunityTarget))
    return result.scalars().all()

@router.post("/targets", response_model=TargetResponse)
async def create_target(target: TargetBase, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    new_target = CommunityTarget(**target.dict())
    db.add(new_target)
    await db.commit()
    await db.refresh(new_target)
    return new_target

@router.get("/channels", response_model=List[ChannelResponse])
async def get_channels(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Channel))
    return result.scalars().all()

@router.post("/channels", response_model=ChannelResponse)
async def create_channel(channel: ChannelBase, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    new_channel = Channel(**channel.dict())
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    return new_channel
