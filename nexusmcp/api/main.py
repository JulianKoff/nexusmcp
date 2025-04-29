from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
from datetime import datetime

from ..agents.protocol_agent import ProtocolAwareAgent, ProtocolState, CrossChainRoute

app = FastAPI(
    title="NexusForge API",
    description="Next-Generation Cross-Chain AI Agent Platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory agent store (replace with database in production)
agents: Dict[str, ProtocolAwareAgent] = {}

class AgentConfig(BaseModel):
    """Configuration for creating a new agent."""
    name: str
    description: str
    chains: Dict[str, str]  # chain_id -> rpc_url
    protocols: Dict[str, List[str]]  # chain_id -> list of protocol addresses

class CrossChainOperation(BaseModel):
    """Parameters for a cross-chain operation."""
    source_chain: int
    target_chain: int
    operation_type: str
    params: Dict[str, Any]

@app.post("/agents/create")
async def create_agent(config: AgentConfig):
    """Create a new protocol-aware agent."""
    agent_id = f"agent_{datetime.now().timestamp()}"
    agent = ProtocolAwareAgent(agent_id, config.dict())
    await agent.initialize()
    agents[agent_id] = agent
    return {"agent_id": agent_id, "status": "created"}

@app.get("/agents/{agent_id}/protocols/{chain_id}/{protocol}")
async def get_protocol_state(
    agent_id: str,
    chain_id: int,
    protocol: str
) -> ProtocolState:
    """Get the current state of a protocol."""
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    state = agent.get_protocol_state(chain_id, protocol)
    if not state:
        raise HTTPException(status_code=404, detail="Protocol state not found")
    
    return state

@app.post("/agents/{agent_id}/cross-chain/route")
async def find_cross_chain_route(
    agent_id: str,
    operation: CrossChainOperation
) -> CrossChainRoute:
    """Find the optimal route for a cross-chain operation."""
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    route = await agent.find_optimal_route(
        operation.source_chain,
        operation.target_chain,
        operation.operation_type
    )
    return route

@app.post("/agents/{agent_id}/cross-chain/execute")
async def execute_cross_chain_operation(
    agent_id: str,
    operation: CrossChainOperation
) -> Dict[str, Any]:
    """Execute a cross-chain operation."""
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    route = await agent.find_optimal_route(
        operation.source_chain,
        operation.target_chain,
        operation.operation_type
    )
    
    result = await agent.execute_cross_chain_operation(route, operation.params)
    return result

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents_count": len(agents)
    }

if __name__ == "__main__":
    uvicorn.run("nexusforge.api.main:app", host="0.0.0.0", port=8000, reload=True) 