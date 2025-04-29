from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Agent(Base):
    """Database model for AI agents."""
    __tablename__ = "agents"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    operations = relationship("Operation", back_populates="agent")
    protocol_states = relationship("ProtocolState", back_populates="agent")

class ProtocolState(Base):
    """Database model for protocol states."""
    __tablename__ = "protocol_states"

    id = Column(Integer, primary_key=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    chain_id = Column(Integer, nullable=False)
    protocol_address = Column(String, nullable=False)
    health_score = Column(Float)
    metrics = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("Agent", back_populates="protocol_states")

class Operation(Base):
    """Database model for cross-chain operations."""
    __tablename__ = "operations"

    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    source_chain = Column(Integer, nullable=False)
    target_chain = Column(Integer, nullable=False)
    operation_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    params = Column(JSON)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    agent = relationship("Agent", back_populates="operations")
    route = relationship("Route", uselist=False, back_populates="operation")

class Route(Base):
    """Database model for cross-chain routes."""
    __tablename__ = "routes"

    id = Column(String, primary_key=True)
    operation_id = Column(String, ForeignKey("operations.id"))
    bridge_protocol = Column(String, nullable=False)
    estimated_cost = Column(Float)
    estimated_time = Column(Float)
    risk_score = Column(Float)
    steps = Column(JSON)

    # Relationships
    operation = relationship("Operation", back_populates="route")

class Analytics(Base):
    """Database model for analytics data."""
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    metric_type = Column(String, nullable=False)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON) 