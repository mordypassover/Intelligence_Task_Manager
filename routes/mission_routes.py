from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB

a = AgentDB()
m=MissionDB()

router =APIRouter()

@router.post("/missions",status_code=201)
def create_mission(data:dict):
    pass

@router.get("/missions")
def get_all_missions():
    return m.get_all_missions()

@router.get("/missions{id}")
def get_mission_by_id(id:int):
    return m.get_mission_by_id(id)

@router.put("/missions{id}/assign/{agent_id}")
def assign_agent_to_missions(id:int, agent_id:int):
    pass

@router.put("/missions{id}/start")
def start_mission(id:int):
    pass

@router.put("/missions{id}/complete")
def complete_mission(id:int):
    pass

@router.put("/missions{id}/fail")
def fail_mission(id:int):
    pass

@router.put("/missions{id}/cancel")
def cancel_mission(id:int):
    pass