import os
import api as api
import zlib
import pymysql as db
import jsonpickle


class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.user = os.getenv("DB_USER", "autorlx")
        self.password = os.getenv("DB_PASSWORD", "")
        self.schema = os.getenv("DB_SCHEMA", "autorlx")

    def _connect(self):
        return db.connect(
            host=self.host, port=self.port,
            user=self.user, password=self.password,
            database=self.schema,
            cursorclass=db.cursors.DictCursor,
            ssl_key=os.getenv("DB_KEY"),
            ssl_verify_identity=True
        )

    def get_gyms(self) -> [api.Gym]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `gyms`"
                cursor.execute(sql)
                gyms = cursor.fetchall()
                for gym in gyms:
                    gym["params"] = []
                    gym["modules"] = []
                    gym["spaces"] = {
                        "observation": {
                            "type": gym["observation_type"],
                            "size": gym["observation_size"],
                            "low": gym["observation_low"],
                            "high": gym["observation_high"],
                        },
                        "action": {
                            "type": gym["action_type"],
                            "size": gym["action_size"],
                            "low": gym["action_low"],
                            "high": gym["action_high"]
                        }
                    }
                    del gym["observation_type"]
                    del gym["observation_size"]
                    del gym["observation_low"]
                    del gym["observation_high"]
                    del gym["action_type"]
                    del gym["action_size"]
                    del gym["action_low"]
                    del gym["action_high"]
                sql = "SELECT * FROM `gym_params`"
                cursor.execute(sql)
                gym_params = cursor.fetchall()
                for gym_param in gym_params:
                    for gym in gyms:
                        if gym["id"] == gym_param["gym_id"]:
                            gym["params"].append(gym_param)
                sql = "SELECT * FROM `gym_modules`"
                cursor.execute(sql)
                gym_modules = cursor.fetchall()
                for gym_module in gym_modules:
                    for gym in gyms:
                        if gym["id"] == gym_module["gym_id"]:
                            gym["modules"].append(gym_module)
        return gyms

    def get_gym(self, gym_id: str) -> api.Gym:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `gyms` WHERE id = %s"
                cursor.execute(sql, gym_id)
                gym = cursor.fetchone()
                gym["params"] = []
                gym["modules"] = []
                gym["spaces"] = {
                    "observation": {
                        "type": gym["observation_type"],
                        "size": gym["observation_size"],
                        "low": gym["observation_low"],
                        "high": gym["observation_high"],
                    },
                    "action": {
                        "type": gym["action_type"],
                        "size": gym["action_size"],
                        "low": gym["action_low"],
                        "high": gym["action_high"]
                    }
                }
                del gym["observation_type"]
                del gym["observation_size"]
                del gym["observation_low"]
                del gym["observation_high"]
                del gym["action_type"]
                del gym["action_size"]
                del gym["action_low"]
                del gym["action_high"]
                sql = "SELECT * FROM `gym_params` WHERE gym_id=%s"
                cursor.execute(sql, gym_id)
                gym_params = cursor.fetchall()
                for gym_param in gym_params:
                    gym["params"].append(gym_param)
                sql = "SELECT * FROM `gym_modules` WHERE gym_id=%s"
                cursor.execute(sql, gym_id)
                gym_modules = cursor.fetchall()
                for gym_module in gym_modules:
                    gym["modules"].append(gym_module)
        return gym

    def insert_gym(self, gym: api.Gym) -> str:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `gyms` (`id`, `name`, `reset`, `step`, `custom`, `code`, `visualization`, `observation_type`, `observation_size`, `observation_low`, `observation_high`, `action_type`, `action_size`, `action_low`, `action_high`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    gym["id"], gym["name"], gym["reset"], gym["step"], gym["custom"], gym["code"], gym["visualization"],
                    gym["spaces"]["observation"]["type"], gym["spaces"]["observation"]["size"],
                    gym["spaces"]["observation"]["low"], gym["spaces"]["observation"]["high"],
                    gym["spaces"]["action"]["type"], gym["spaces"]["action"]["size"],
                    gym["spaces"]["action"]["low"], gym["spaces"]["action"]["high"]
                ))
                sql = "INSERT INTO `gym_params` (`id`, `gym_id`, `name`, `description`, `type`, `default`) VALUES (%s, %s, %s, %s, %s, %s)"
                rows = []
                for param in gym["params"]:
                    rows.append((
                        param["id"], param["gym_id"], param["name"], param["description"], param["type"],
                        param["default"]
                    ))
                cursor.executemany(sql, rows)
                sql = "INSERT INTO `gym_modules` (`id`, `gym_id`, `type`, `module`, `submodules`) VALUES (%s, %s, %s, %s, %s)"
                rows = []
                for module in gym["modules"]:
                    rows.append((
                        module["id"], module["gym_id"], module["type"], module["module"], module["submodules"]
                    ))
                cursor.executemany(sql, rows)
            connection.commit()
        return gym["id"]

    def delete_gym(self, gym_id: str) -> bool:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `runs` WHERE `gym_id` = %s"
                cursor.execute(sql, gym_id)
                sql = "DELETE FROM `gym_params` WHERE `gym_id` = %s"
                cursor.execute(sql, gym_id)
                sql = "DELETE FROM `gym_modules` WHERE `gym_id` = %s"
                cursor.execute(sql, gym_id)
                sql = "DELETE FROM `gyms` WHERE `id` = %s"
                cursor.execute(sql, gym_id)
            connection.commit()
        return True

    def insert_configuration(self, configuration: api.Configuration) -> str:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `configurations` (`id`, `metric_id`, `tuner_id`, `name`, `n_jobs`, `n_episodes`, `n_agents`, `n_generations`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    configuration["id"], configuration["metric_id"], configuration["tuner_id"], configuration["name"],
                    configuration["n_jobs"], configuration["n_episodes"],
                    configuration["n_agents"], configuration["n_generations"]
                ))
                for model_id in configuration["models"]:
                    sql = "INSERT INTO `configuration_models` (`configuration_id`, `model_id`) VALUES (%s, %s)"
                    cursor.execute(sql, (configuration["id"], model_id))
            connection.commit()
        return configuration["id"]

    def delete_configuration(self, configuration_id: str) -> bool:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `runs` WHERE `configuration_id` = %s"
                cursor.execute(sql, configuration_id)
                sql = "DELETE FROM `configuration_models` WHERE `configuration_id` = %s"
                cursor.execute(sql, configuration_id)
                sql = "DELETE FROM `configurations` WHERE `id` = %s"
                cursor.execute(sql, configuration_id)
            connection.commit()
        return True

    def get_configurations(self) -> [api.Configuration]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `configurations`"
                cursor.execute(sql)
                result = cursor.fetchall()
                for config in result:
                    config["models"] = []
                sql = "SELECT * FROM `configuration_models`"
                cursor.execute(sql)
                selected_models = cursor.fetchall()
                for model in selected_models:
                    for config in result:
                        if config["id"] == model["configuration_id"]:
                            config["models"].append(model["model_id"])
        return result

    def get_configuration(self, configuration_id: str) -> api.Configuration:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `configurations` WHERE id = %s"
                cursor.execute(sql, configuration_id)
                result = cursor.fetchone()
                result["models"] = []
                sql = "SELECT * FROM `configuration_models` WHERE configuration_id = %s"
                cursor.execute(sql, configuration_id)
                selected_models = cursor.fetchall()
                for model in selected_models:
                    result["models"].append(model["model_id"])
        return result

    def get_models(self) -> [api.Model]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `models`"
                cursor.execute(sql)
                result = cursor.fetchall()
        return result

    def get_metrics(self) -> [api.Metric]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `metrics`"
                cursor.execute(sql)
                result = cursor.fetchall()
        return result

    def get_tuners(self) -> [api.Tuner]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `tuners`"
                cursor.execute(sql)
                result = cursor.fetchall()
        return result

    def insert_run(self, run: api.RunLaunch) -> str:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `runs` (`id`, `configuration_id`, `gym_id`, `status`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (run["id"], run["configuration_id"], run["gym_id"], run["status"]))
                sql = "INSERT INTO `run_gym_params` (`id`, `run_id`, `gym_param_id`, `value`) VALUES (%s, %s, %s, %s)"
                rows = []
                for param in run["gym_params"]:
                    rows.append((
                        param["id"], param["run_id"], param["gym_param_id"], param["value"]
                    ))
                cursor.executemany(sql, rows)
            connection.commit()
        return run["id"]

    def update_run(self, run: api.RunLaunch) -> str:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `runs` SET status=%s WHERE id=%s"
                cursor.execute(sql, (run["status"], run["id"]))
            connection.commit()
        return run["id"]

    def get_runs(self) -> [api.RunInfo]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `runs` ORDER BY `created_on` DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                for run in result:
                    run["models"] = []
                    run["logs"] = []
                    run["gym_params"] = []
                # load run gym params
                sql = "SELECT * FROM `run_gym_params`"
                cursor.execute(sql)
                gym_params = cursor.fetchall()
                for gym_param in gym_params:
                    for run in result:
                        if run["id"] == gym_param["run_id"]:
                            run["gym_params"].append(gym_param)
                # load models
                sql = "SELECT * FROM `run_models` ORDER BY `created_on` DESC"
                cursor.execute(sql)
                models = cursor.fetchall()
                for model in models:
                    model["logs"] = []
                    for run in result:
                        if run["id"] == model["run_id"]:
                            run["models"].append(model)
                # load logs
                sql = "SELECT `id`, `run_id`, `run_model_id`, `phase`, `epoch`, `iteration`, `severity`, `log`, `reward`, `created_on` FROM `run_logs` ORDER BY `epoch` DESC, `iteration` DESC, `run_model_id` ASC"
                cursor.execute(sql)
                logs = cursor.fetchall()
                for log in logs:
                    for run in result:
                        if run["id"] == log["run_id"]:
                            if log["run_model_id"]:
                                for model in run["models"]:
                                    if model["id"] == log["run_model_id"]:
                                        model["logs"].append(log)
                            else:
                                run["logs"].append(log)
        return result

    def get_run(self, run_id: str) -> api.RunInfo:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `runs` WHERE id = %s"
                cursor.execute(sql, run_id)
                run = cursor.fetchone()
                if not run:
                    return None
                run["models"] = []
                run["logs"] = []
                run["gym_params"] = []
                # load run gym params
                sql = "SELECT * FROM `run_gym_params` WHERE run_id = %s"
                cursor.execute(sql, run_id)
                gym_params = cursor.fetchall()
                for gym_param in gym_params:
                    run["gym_params"].append(gym_param)
                # load models
                sql = "SELECT * FROM `run_models` WHERE run_id = %s ORDER BY `created_on` DESC"
                cursor.execute(sql, run_id)
                models = cursor.fetchall()
                for model in models:
                    model["logs"] = []
                    run["models"].append(model)
                # load logs
                sql = "SELECT `id`, `run_id`, `run_model_id`, `phase`, `epoch`, `iteration`, `severity`, `log`, `reward`, `created_on` FROM `run_logs` WHERE run_id = %s ORDER BY `epoch` DESC, `iteration` DESC, `run_model_id` ASC"
                cursor.execute(sql, run_id)
                logs = cursor.fetchall()
                for log in logs:
                    if log["run_model_id"]:
                        for model in run["models"]:
                            if model["id"] == log["run_model_id"]:
                                model["logs"].append(log)
                    else:
                        run["logs"].append(log)
        return run

    def delete_run(self, run_id: str) -> bool:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `run_gym_params` WHERE `run_id` = %s"
                cursor.execute(sql, run_id)
                sql = "DELETE FROM `run_logs` WHERE `run_id` = %s"
                cursor.execute(sql, run_id)
                sql = "DELETE FROM `run_models` WHERE `run_id` = %s"
                cursor.execute(sql, run_id)
                sql = "DELETE FROM `runs` WHERE `id` = %s"
                cursor.execute(sql, run_id)
            connection.commit()
        return True

    def get_run_model(self, run_model_id: str) -> api.RunModelLaunch:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `run_models` WHERE id = %s ORDER BY `created_on` DESC"
                cursor.execute(sql, run_model_id)
                model = cursor.fetchone()
                if model:
                    model["logs"] = []
                    # load logs
                    sql = "SELECT `id`, `run_id`, `run_model_id`, `phase`, `epoch`, `iteration`, `severity`, `log`, `reward`, `created_on` FROM `run_logs` WHERE run_model_id = %s ORDER BY `epoch` DESC, `iteration` DESC, `run_model_id` ASC"
                    cursor.execute(sql, run_model_id)
                    logs = cursor.fetchall()
                    for log in logs:
                        model["logs"].append(log)
        return model

    def insert_run_model(self, model: api.RunModelLaunch) -> str:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `run_models` (`id`, `run_id`, `model_id`, `hyperparameters`, `policy`, `status` ) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    model["id"], model["run_id"], model["model_id"], model["hyperparameters"], model["policy"],
                    model["status"]
                ))
            connection.commit()
        return model["id"]

    def update_run_model(self, model: api.RunModelLaunch) -> str:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `run_models` SET status=%s WHERE id=%s"
                cursor.execute(sql, (model["status"], model["id"]))
            connection.commit()
        return model["id"]

    def insert_run_log(self, log: api.RunLog) -> str:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `run_logs` (`id`, `run_id`, `phase`, `severity`, `log` ) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (log["id"], log["run_id"], log["phase"], log["severity"], log["log"]))
            connection.commit()
        return log["id"]

    def insert_run_model_logs(self, logs: [api.RunModelLog]):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `run_logs` (`id`, `run_id`, `run_model_id`, `epoch`, `iteration`, `phase`, `severity`, `log`, `state`, `action`, `score`, `reward` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                rows = []
                log_ids = []
                for log in logs:
                    rows.append((
                        log["id"], log["run_id"], log["run_model_id"], log["epoch"], log["iteration"], log["phase"],
                        log["severity"], log["log"], log["state"], log["action"], log["score"], log["reward"]
                    ))
                    log_ids.append(log["id"])
                cursor.executemany(sql, rows)
            connection.commit()
        return log_ids

    def get_trajectory(self, run_model_id: str, epoch: int, iteration: int):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT `action`, `state`, `score` FROM `run_logs` WHERE run_model_id = %s AND epoch = %s AND iteration = %s"
                cursor.execute(sql, (run_model_id, epoch, iteration))
                trajectory = cursor.fetchone()
        trajectory["action"] = zlib.decompress(jsonpickle.decode(trajectory["action"])).decode()
        trajectory["state"] = zlib.decompress(jsonpickle.decode(trajectory["state"])).decode()
        trajectory["score"] = zlib.decompress(jsonpickle.decode(trajectory["score"])).decode()
        return trajectory

    def push_user_study_session(self, session: api.UserStudySession):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `user_study_sessions` (`id`, `time`, `score`) VALUES (%s, %s, %s)"
                rows = []
                for row in session["scores"]:
                    rows.append((session["id"], row["time"], row["score"]))
                cursor.executemany(sql, rows)
            connection.commit()
        return session["id"]

    def insert_gym_param(self, gym_param: api.GymParam):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `gym_params` (`id`, `gym_id`, `name`, `description`, `type`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    gym_param["id"], gym_param["gym_id"], gym_param["name"], gym_param["description"], gym_param["type"]
                ))
            connection.commit()
        return gym_param["id"]

    def update_gym_param(self, gym_param: api.GymParam):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `gym_params` SET name=%s, description=%s, type=%s WHERE id=%s"
                cursor.execute(sql, (gym_param["name"], gym_param["description"], gym_param["type"]))
            connection.commit()
        return gym_param["id"]

    def get_gym_param(self, gym_param_id: str):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `gym_params` WHERE id = %s"
                cursor.execute(sql, gym_param_id)
                gym_param = cursor.fetchone()
        return gym_param

    def insert_catalog_gym(self, catalog_gym: api.CatalogGym):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `catalog_gyms` (`id`, `gym_id`, `category_id`, `email`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (
                    catalog_gym["id"], catalog_gym["gym_id"], catalog_gym["category_id"], catalog_gym["email"]
                ))
            connection.commit()
        return catalog_gym["id"]

    def delete_catalog_gym(self, gym_id: str):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `catalog_gyms` WHERE `gym_id` = %s"
                cursor.execute(sql, gym_id)
            connection.commit()
        return True

    def get_catalog(self):
        with self._connect() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `catalog_gyms` cg, `gyms` g WHERE cg.gym_id=g.id"
                cursor.execute(sql)
                gyms = cursor.fetchall()
                for gym in gyms:
                    gym["params"] = []
                    gym["modules"] = []
                    gym["spaces"] = {
                        "observation": {
                            "type": gym["observation_type"],
                            "size": gym["observation_size"],
                            "low": gym["observation_low"],
                            "high": gym["observation_high"],
                        },
                        "action": {
                            "type": gym["action_type"],
                            "size": gym["action_size"],
                            "low": gym["action_low"],
                            "high": gym["action_high"]
                        }
                    }
                    del gym["observation_type"]
                    del gym["observation_size"]
                    del gym["observation_low"]
                    del gym["observation_high"]
                    del gym["action_type"]
                    del gym["action_size"]
                    del gym["action_low"]
                    del gym["action_high"]
                sql = "SELECT * FROM `gym_params`"
                cursor.execute(sql)
                gym_params = cursor.fetchall()
                for gym_param in gym_params:
                    for gym in gyms:
                        if gym["gym_id"] == gym_param["gym_id"]:
                            gym["params"].append(gym_param)
                sql = "SELECT * FROM `gym_modules`"
                cursor.execute(sql)
                gym_modules = cursor.fetchall()
                for gym_module in gym_modules:
                    for gym in gyms:
                        if gym["gym_id"] == gym_module["gym_id"]:
                            gym["modules"].append(gym_module)
                sql = "SELECT * FROM `catalog` ORDER BY `naics_code_2022`"
                cursor.execute(sql)
                items = cursor.fetchall()
                catalog = api.Catalog(
                    title="AutoRL X Catalog",
                    categories=[]
                )
                for item in items:
                    category = api.Category(
                        id=item["id"],
                        code=item["naics_code_2022"],
                        title=item["naics_title_2022"],
                        categories=[],
                        gyms=[]
                    )
                    for gym in gyms:
                        if gym["category_id"] == category.id:
                            category.gyms.append(gym)
                    parent = catalog
                    code = category.code
                    level = 2
                    while level < len(code):
                        for uncle in parent.categories:
                            if uncle.code == code[:level]:
                                parent = uncle
                                break
                        level += 1
                    parent.categories.append(category)
        return catalog
