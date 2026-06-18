import uvicorn
from fastapi import FastAPI
from routes import (report_routes,
                    agent_routes,
                    mission_routes)


app = FastAPI()
app.include_router(report_routes.router)
app.include_router(agent_routes.router)
app.include_router(mission_routes.router)

if __name__ == "__main__":
    uvicorn.run(app = "main:app", reload=True)