import api
from subprocess import Popen
import json
import os
from services import db_service, log_service


class Run:
    def __init__(self, db: db_service.Database, log: log_service.Logger):
        self.db = db
        self.log = log

    def launch_run(self, run: api.RunLaunch):
        run_id = self.db.insert_run(run)
        gym = self.db.get_gym(run["gym_id"])
        configuration = self.db.get_configuration(run["configuration_id"])
        self.log.info("train", run_id, "Launching AutoRL process...")
        self.log.info("train", run_id, "run_id=" + run_id)
        self.log.info("train", run_id, "metric_id=" + str(configuration["metric_id"]))
        self.log.info("train", run_id, "tuner_id=" + str(configuration["tuner_id"]))
        self.log.info("train", run_id, "models=" + str(configuration["models"]))
        self.log.info("train", run_id, "n_jobs=" + str(configuration["n_jobs"]))
        self.log.info("train", run_id, "n_episodes=" + str(configuration["n_episodes"]))
        self.log.info("train", run_id, "n_agents=" + str(configuration["n_agents"]))
        self.log.info("train", run_id, "n_generations=" + str(configuration["n_generations"]))
        gym_params = {}
        for param in run["gym_params"]:
            gym_param = self.db.get_gym_param(param["gym_param_id"])
            gym_params["%" + gym_param["name"].upper().replace(" ", "_")] = str(param["value"])
            self.log.info(
                "train", run_id, "%" + gym_param["name"].upper().replace(" ", "_") + "=" + str(param["value"])
            )
        job = {
            "run_id": run_id,
            "code": gym["code"],
            "metric_id": configuration["metric_id"],
            "tuner_id": configuration["tuner_id"],
            "models": configuration["models"],
            "n_jobs": configuration["n_jobs"],
            "n_episodes": configuration["n_episodes"],
            "n_agents": configuration["n_agents"],
            "n_generations": configuration["n_generations"],
            "gym_params": gym_params
        }
        Popen(['nohup', 'python', 'run.py', json.dumps(job)])
        return run_id
