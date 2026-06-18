from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB

a = AgentDB()
m=MissionDB()

router =APIRouter()

@router.post("/missions",status_code=201)
def create_mission(data:dict):
    try:
        title = data["title"]
        description =data["description"]
        location =data["location"]
        difficulty =data["difficulty"]
        importance =data["importance"]

        if 0 > importance >10 or 0 > difficulty >10:
            raise HTTPException(status_code= 400 ,detail="importance and risk_level must be between 1 and 10 ")
        return m.create_mission({"title":title,
                        "description":description,
                          "location":location,
                          "difficulty": difficulty,
                          "importance":importance})
    except KeyError:
        raise HTTPException(status_code=422, detail="missing data to create mission")

@router.get("/missions")
def get_all_missions():
    return m.get_all_missions()

@router.get("/missions{id}")
def get_mission_by_id(id:int):
    return m.get_mission_by_id(id)

@router.put("/missions{id}/assign/{agent_id}")
def assign_agent_to_missions(id:int, agent_id:int):
    mission = m.get_mission_by_id(id)
    agent = a.get_agent_by_id(agent_id)
    if not agent :
        raise HTTPException(status_code=404, detail= f"agent {agent_id} dose not exist")
    if not mission:
        raise HTTPException(status_code=404, detail=f"mission {id} dose not exist")
    if mission["status"] != "NEW":
        raise HTTPException(status_code=400, detail=f"cant start status not NEW")
    if not agent["is_active"]:
        raise HTTPException(status_code=400, detail=f"agent not active")
    if len(m.get_open_missions_by_agent( agent_id)) >=3 :
        raise HTTPException(status_code=400, detail=f"agent hase 3 ore more missions")
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        raise HTTPException(status_code=400, detail=f"cant assign agent, rank not Commander")
    return m.assign_mission(id, agent_id)


@router.put("/missions{id}/start")
def start_mission(id:int):
    mission = m.get_mission_by_id(id)
    if mission["status"]!= "ASSIGNED":
        raise HTTPException(status_code=400, detail=f"cant start mission if status not ASSIGNED")
    m.update_mission_status(id, "IN_PROGRESS")


@router.put("/missions{id}/complete")
def complete_mission(id:int):
    mission = m.get_mission_by_id(id)
    if mission["status"] != "IN_PROGRESS":
        raise HTTPException(status_code=400, detail=f"cant complete mission if status not IN_PROGRESS")
    a.increment_completed(mission["assigned_agent_id"])
    return m.update_mission_status(id, "COMPLETED")

@router.put("/missions{id}/fail")
def fail_mission(id:int):
    mission = m.get_mission_by_id(id)
    if mission["status"] != "IN_PROGRESS":
        raise HTTPException(status_code=400, detail=f"cant fail mission if status not IN_PROGRESS")
    a.increment_failed(mission["assigned_agent_id"])
    return m.update_mission_status(id, "FAILED")

@router.put("/missions{id}/cancel")
def cancel_mission(id:int):
    mission = m.get_mission_by_id(id)
    if mission["status"] != {'NEW','ASSIGNED'}:
        raise HTTPException(status_code=400, detail=f"cant cancel mission if status not NEW ore ASSIGNED")