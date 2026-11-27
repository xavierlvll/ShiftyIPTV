from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.backend.db.session import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)  # M3U or individual stream URL
    type = Column(String, default="m3u")  # 'm3u' or 'single'
    enabled = Column(Boolean, default=True)
    last_refresh = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    channels = relationship("Channel", back_populates="provider", cascade="all, delete-orphan")

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    name = Column(String, nullable=False)
    group = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    epg_id = Column(String, nullable=True)
    stream_url = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    last_seen = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    provider = relationship("Provider", back_populates="channels")
    programs = relationship("Program", back_populates="channel", cascade="all, delete-orphan")

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_name = Column(DateTime, nullable=True) # Using end_time in implementation
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    channel = relationship("Channel", back_populates="programs")
