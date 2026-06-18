from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB

a = AgentDB()

router =APIRouter()


@router.post("/agents", status_code=201)
def create_agent(data):
    pass

@router.get("/agents")
def get_all_agents():
    return a.get_all_agents()

@router.get("/agents/{id}")
def get_agent_by_id(id:int):
    return a.get_agent_by_id(id)

@router.put("/agents/{id}")
def update_agent(id:int, data:dict):
    pass

@router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    return a.deactivate_agent(id)

@router.get("/agents/{id}/performance")
def get_agent_performance(id:int):
    return a.get_agent_performance(id)
