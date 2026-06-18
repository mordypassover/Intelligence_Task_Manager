from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
import mysql.connector.errors

a = AgentDB()

router =APIRouter()


@router.post("/agents", status_code=201)
def create_agent(data:dict):
    try:
        name = data["name"]
        specialty = data["specialty"]
        agent_rank = data["agent_rank"]
        if agent_rank not in {"Junior", "Senior", "Commander"}:
            raise HTTPException(status_code=400, detail="rank not valid")
        return a.create_agent({"name":name, "specialty":specialty, "agent_rank":agent_rank})
    except KeyError:
        raise HTTPException(status_code=422, detail="missing data to create agent")


@router.get("/agents")
def get_all_agents():
    return a.get_all_agents()

@router.get("/agents/{id}")
def get_agent_by_id(id:int):
    return a.get_agent_by_id(id)

@router.put("/agents/{id}")
def update_agent(id:int, data:dict):
    for i in data.keys():
        if i not in {"name", "specialty", "is_active", "completed_missions", "failed_missions", "agent_rank"}:
            raise HTTPException(status_code=422, detail=f"field {i} not valid")
        if i == "agent_rank" and data["agent_rank"] not in {"Junior", "Senior", "Commander"}:
            raise HTTPException(status_code=400, detail="rank not valid")
    return a.update_agent(id, data)

@router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):

    return a.deactivate_agent(id)

@router.get("/agents/{id}/performance")
def get_agent_performance(id:int):
    return a.get_agent_performance(id)
