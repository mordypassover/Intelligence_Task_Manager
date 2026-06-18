from fastapi import APIRouter, HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB

m = MissionDB()
a = AgentDB()

router =APIRouter()

@router.get("/reports/summary")
def get_summery():
    return {"active_agents_count": a.count_active_agents(),
            "total_missions": m.count_all_missions(),
            "open_missions": m.count_open_missions(),
            "completed_missions": m.count_by_status("COMPLETED"),
            "failed_missions": m.count_by_status("FAILED"),
            "critical_missions": m.count_critical_missions()}
