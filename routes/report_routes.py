from fastapi import APIRouter, HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from logs.logger_config import logger

m = MissionDB()
a = AgentDB()

router =APIRouter()

@router.get("/reports/summary")
def get_summery():
    logger.info("getting summery")
    return {"active_agents_count": a.count_active_agents(),
            "total_missions": m.count_all_missions(),
            "open_missions": m.count_open_missions(),
            "completed_missions": m.count_by_status("COMPLETED"),
            "failed_missions": m.count_by_status("FAILED"),
            "cancelled_missions": m.count_by_status("CANCELLED")}

@router.get("/reports/missions-by-status")
def get_missions_by_status():
    logger.info("geting missions by status")
    return {
        "open": m.count_open_missions(),
        "in_progress": m.count_by_status("IN_PROGRESS"),
        "completed": m.count_by_status("COMPLETED"),
        "failed": m.count_by_status("FAILED")
    }

@router.get("/reports/top-agent")
def get_top_agent():
    logger.info("getting top agent")
    return m.get_top_agent()