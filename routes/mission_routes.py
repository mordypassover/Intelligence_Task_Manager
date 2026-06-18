from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from logs.logger_config import logger

a = AgentDB()
m=MissionDB()

router =APIRouter()

@router.post("/missions",status_code=201)
def create_mission(data:dict):
    logger.info("start create mission")
    try:
        title = data["title"]
        description =data["description"]
        location =data["location"]
        difficulty =data["difficulty"]
        importance =data["importance"]

        if 0 > importance >10 or 0 > difficulty >10:
            logger.error("not valid nums")
            raise HTTPException(status_code= 400 ,detail="importance and risk_level must be between 1 and 10 ")

        return m.create_mission({"title":title,
                        "description":description,
                          "location":location,
                          "difficulty": difficulty,
                          "importance":importance})
    except KeyError:
        logger.error("a key ore more is missing")
        raise HTTPException(status_code=422, detail="missing data to create mission")

@router.get("/missions")
def get_all_missions():
    return m.get_all_missions()

@router.get("/missions{id}")
def get_mission_by_id(id:int):
    logger.info(f"getting mission {id}")
    return m.get_mission_by_id(id)

@router.put("/missions{id}/assign/{agent_id}")
def assign_agent_to_missions(id:int, agent_id:int):
    logger.info(f"started to assign mission {id} to {agent_id}")
    mission = m.get_mission_by_id(id)
    agent = a.get_agent_by_id(agent_id)
    if not agent :
        logger.error(f"agent {agent_id} dose not exist")
        raise HTTPException(status_code=404, detail= f"agent {agent_id} dose not exist")
    if not mission:
        logger.error(f"mission {id} dose not exist")
        raise HTTPException(status_code=404, detail=f"mission {id} dose not exist")
    if mission["status"] != "NEW":
        logger.error(f"cant start status not NEW")
        raise HTTPException(status_code=400, detail=f"cant start status not NEW")
    if not agent["is_active"]:
        logger.error(f"agent {agent_id} not active")
        raise HTTPException(status_code=400, detail=f"agent {agent_id} not active")
    if len(m.get_open_missions_by_agent( agent_id)) >=3 :
        logger.error(f"agent hase 3 ore more missions")
        raise HTTPException(status_code=400, detail=f"agent hase 3 ore more missions")
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        logger.error("cant assign agent, rank not Commander")
        raise HTTPException(status_code=400, detail=f"cant assign agent, rank not Commander")
    logger.info("assign mission {id} to {agent_id} successfully" )
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