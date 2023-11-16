import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import api
from typing import *
from services import gym_service, configuration_service, db_service, log_service, run_service

app = FastAPI(
    title="AutoRL X Server",
    description="REST API Server for AutoRL X",
    version="1.0.0",
    terms_of_service="GPL 3.0",
    contact={
        "name": "Loraine Franke",
        "url": "https://mpsych.org/",
        "email": "franke@mpsych.org"
    },
    license_info={
        "name": "GNU GENERAL PUBLIC LICENSE 3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.txt"
    },
    servers=[
        {
            "url": os.getenv("AUTORL_X_SERVER_URL", "http://localhost:8000"),
            "description": "AutoRL X Server URL"
        }
    ],
    redoc_url="/docs",
    docs_url="/try"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

database: db_service.Database = db_service.Database()
gyms: gym_service.Gyms = gym_service.Gyms(database)
configurations: configuration_service.Configurations = configuration_service.Configurations(database)
logger: log_service.Logger = log_service.Logger(database)
run: run_service.Run = run_service.Run(database, logger)


@app.post("/api/gyms", tags=["gyms"])
async def push_gym(gym: api.Gym):
    """Push a gym."""
    return gyms.push_gym(gym)


@app.get("/api/gyms/{gym_id}", tags=["gyms"])
async def get_gym(gym_id: str) -> api.Gym:
    """Get a gym."""
    return gyms.get_gym(gym_id)


@app.get("/api/gyms", tags=["gyms"])
async def get_gyms() -> List[api.Gym]:
    """Get all gyms."""
    return gyms.get_gyms()


@app.delete("/api/gyms/{gym_id}", tags=["gyms"])
async def delete_gym(gym_id: str) -> bool:
    """Delete a gym."""
    return gyms.delete_gym(gym_id)


@app.post("/api/gyms/probe_space", tags=["gyms"])
async def probe_space(space: api.Space) -> api.SpaceProbe:
    """Probe observation or action space."""
    return gyms.probe_space(space)


@app.post("/api/configurations", tags=["configurations"])
async def push_configuration(configuration: api.Configuration):
    """Push a configuration."""
    return configurations.push_configuration(configuration)


@app.get("/api/configurations/{configuration_id}", tags=["configurations"])
async def get_configuration(configuration_id: str) -> api.Configuration:
    """Get a configuration."""
    return configurations.get_configuration(configuration_id)


@app.get("/api/configurations", tags=["configurations"])
async def get_configurations() -> List[api.Configuration]:
    """Get all configurations."""
    return configurations.get_configurations()


@app.delete("/api/configurations/{configuration_id}", tags=["configurations"])
async def delete_configuration(configuration_id: str) -> bool:
    """Delete a configuration."""
    return configurations.delete_configuration(configuration_id)


@app.get("/api/metrics", tags=["configurations"])
async def get_metrics() -> List[api.Metric]:
    """Get all metrics."""
    return configurations.get_metrics()


@app.get("/api/models", tags=["configurations"])
async def get_models() -> List[api.Model]:
    """Get all models."""
    return configurations.get_models()


@app.get("/api/tuners", tags=["configurations"])
async def get_tuners() -> List[api.Tuner]:
    """Get all tuners."""
    return configurations.get_tuners()


@app.post("/api/runs", tags=["runs"])
async def push_run(run_launch: api.RunLaunch):
    """Run a gym optimization or update its status."""
    if database.get_run(run_launch["id"]):
        return database.update_run(run_launch)
    else:
        return run.launch_run(run_launch)


@app.get("/api/runs", tags=["runs"])
async def get_runs() -> List[api.RunInfo]:
    """Get all runs."""
    return database.get_runs()


@app.delete("/api/runs/{run_id}", tags=["runs"])
async def delete_run(run_id: str) -> bool:
    """Delete a run."""
    return database.delete_run(run_id)


@app.post("/api/models", tags=["runs"])
async def push_run_model(model: api.RunModelLaunch) -> str:
    """Push a run model."""
    if database.get_run_model(model["id"]):
        return database.update_run_model(model)
    else:
        return database.insert_run_model(model)


@app.post("/api/logs", tags=["runs"])
async def push_run_model_logs(logs: List[api.RunModelLog]) -> List[str]:
    """Push a list of model logs."""
    return logger.push_run_model_logs(logs)


@app.get("/api/trajectory/{run_model_id}/{epoch}/{iteration}", tags=["runs"])
async def get_trajectory(run_model_id: str, epoch: int, iteration: int) -> api.Trajectory:
    """Get the trajectory of an evaluation."""
    return database.get_trajectory(run_model_id, epoch, iteration)


@app.get("/api/catalog", tags=["catalog"])
async def get_catalog() -> api.Catalog:
    """Get the AutoRL X Gym Catalog based on NAICS 2022 categorization."""
    return database.get_catalog()


@app.post("/api/catalog", tags=["catalog"])
async def push_catalog_gym(catalog_gym: api.CatalogGym) -> str:
    """Publish a gym to the AutoRL X Gym Catalog."""
    return database.insert_catalog_gym(catalog_gym)


@app.delete("/api/catalog/{gym_id}", tags=["catalog"])
async def delete_catalog_gym(gym_id: str) -> bool:
    """Delete a gym from the AutoRL X Gym Catalog."""
    return database.delete_catalog_gym(gym_id)


@app.post("/api/user_study_session", tags=["misc"])
async def push_user_study_session(session: api.UserStudySession) -> str:
    """Push a user study session."""
    return database.push_user_study_session(session)


@app.get("/", tags=["Utils"], deprecated=True, include_in_schema=False)
def root():
    """Redirects to the documentation."""
    return RedirectResponse(url="docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
