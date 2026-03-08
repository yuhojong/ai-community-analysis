from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)  # 'daum', 'naver', 'discord', 'x'
    is_active = Column(Boolean, default=True)
    config = Column(JSON) # Platform-wide settings like API keys or base URLs

class CommunityTarget(Base):
    __tablename__ = "community_targets"
    id = Column(Integer, primary_key=True, index=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    name = Column(String(100)) # Cafe Name or Discord Server Name
    target_url = Column(String(255))
    is_active = Column(Boolean, default=True)

    channels = relationship("Channel", back_populates="target")

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("community_targets.id"))
    name = Column(String(100)) # Board Name or Discord Channel Name
    identifier = Column(String(100)) # Board ID or Channel ID
    language = Column(String(10)) # 'ko', 'en', etc.
    is_private = Column(Boolean, default=False)

    target = relationship("CommunityTarget", back_populates="channels")
    collected_data = relationship("CollectedData", back_populates="channel")

class CollectedData(Base):
    __tablename__ = "collected_data"
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    author = Column(String(100))
    content = Column(Text)
    external_id = Column(String(100)) # Post ID or Message ID
    posted_at = Column(DateTime)
    collected_at = Column(DateTime, server_default=func.now())
    metadata_json = Column(JSON)

    channel = relationship("Channel", back_populates="collected_data")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True) # Date of the report analysis
    language = Column(String(10))
    content_markdown = Column(Text)
    google_sheet_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
