import json
import sys
import os
from services import arlo_service

if __name__ == "__main__":
    arlo: arlo_service.Arlo = arlo_service.Arlo()
    job = json.loads(sys.argv[1])
    os.environ["RUN_ID"] = job["run_id"]
    arlo.run(
        run_id=job["run_id"],
        code=job["code"],
        metric_id=job["metric_id"],
        tuner_id=job["tuner_id"],
        models=job["models"],
        n_jobs=job["n_jobs"],
        n_episodes=job["n_episodes"],
        n_agents=job["n_agents"],
        n_generations=job["n_generations"],
        gym_params=job["gym_params"]
    )
