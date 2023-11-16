import ARLO.logger
from ARLO.tuner import TunerGenetic, TunerOptuna
from ARLO.input_loader.input_loader import LoadSameEnv
from ARLO.block import ModelGenerationMushroomOnlineDQN
from ARLO.block import ModelGenerationMushroomOnlineDDPG
from ARLO.block import ModelGenerationMushroomOnlinePPO
from ARLO.block import ModelGenerationMushroomOnlineSAC
from ARLO.block import ModelGenerationMushroomOnlineGPOMDP
from ARLO.block import AutoModelGeneration
from ARLO.metric import DiscountedReward, TDError, TimeSeriesRollingAverageDiscountedReward
from ARLO.rl_pipeline import OnlineRLPipeline
import requests
import os

import math
import numpy as np
from ARLO.environment import BaseEnvironment
from mushroom_rl.utils.spaces import Discrete, Box


class Arlo:
    def __init__(self):
        self.logger = ARLO.logger.Logger
        self.log_mode = 'console'
        self.dir_chkpath = './'

    def run(self, run_id: str, code: str, metric_id: str, tuner_id: str, models: [str], n_jobs, n_episodes, n_agents,
            n_generations, gym_params):
        print(run_id + ": Optimization process initialized.")
        print(metric_id)
        print(tuner_id)
        print(str(n_jobs) + " jobs")
        print(str(n_episodes) + " episodes")
        print(str(n_agents) + " agents")
        print(str(n_generations) + " generations")
        print(gym_params)

        n_trials = 100

        # make an instance of the gym
        for param in gym_params:
            code = code.replace(param, gym_params[param])
        gym = compile(code, 'gym', 'exec')
        exec(gym)
        env = eval("AutoRLXEnv()")

        if metric_id == "discounted":
            metric = DiscountedReward(
                obj_name='discounted_metric',
                n_episodes=n_episodes,
                batch=False,
                log_mode="console",
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )
        elif metric_id == "td_error":
            metric = TDError(
                obj_name='tderror_metric',
                n_episodes=n_episodes,
                batch=False,
                log_mode="console",
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )
        elif metric_id == "tsradiscounted":
            metric = TimeSeriesRollingAverageDiscountedReward(
                obj_name='tsradiscounted_metric',
                n_episodes=n_episodes,
                batch=False,
                log_mode="console",
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )

        input_loader_online = LoadSameEnv(obj_name='input_loader_online_default', n_jobs=n_jobs)

        ddpg = ModelGenerationMushroomOnlineDDPG(
            eval_metric=metric, obj_name='ddpg_generation', log_mode=self.log_mode, algo_params=None, n_jobs=n_jobs
        )
        dqn = ModelGenerationMushroomOnlineDQN(
            eval_metric=metric, obj_name='dqn_generation', log_mode=self.log_mode, algo_params=None, n_jobs=n_jobs
        )
        ppo = ModelGenerationMushroomOnlinePPO(
            eval_metric=metric, obj_name='ppo_generation', log_mode=self.log_mode, algo_params=None, n_jobs=n_jobs
        )
        sac = ModelGenerationMushroomOnlineSAC(
            eval_metric=metric, obj_name='sac_generation', log_mode=self.log_mode, algo_params=None, n_jobs=n_jobs
        )
        gpomdp = ModelGenerationMushroomOnlineGPOMDP(
            eval_metric=metric, obj_name='gpomdp_generation', log_mode=self.log_mode, algo_params=None,
            n_jobs=n_jobs
        )

        tuner_dict = {}
        if "ddpg" in models and tuner_id == "genetic":
            tuner_dict['ddpg_mushroom_genetic'] = TunerGenetic(
                block_to_opt=ddpg,
                n_agents=n_agents,
                n_generations=n_generations,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='ddpg_tuner_genetic',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )
        if "ddpg" in models and tuner_id == "optuna":
            tuner_dict['ddpg_mushroom_optuna'] = TunerOptuna(
                block_to_opt=ddpg,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='ddpg_tuner_optuna',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs,
                n_trials=n_trials
            )
        if "dqn" in models and tuner_id == "genetic":
            tuner_dict['dqn_mushroom_genetic'] = TunerGenetic(
                block_to_opt=dqn,
                n_agents=n_agents,
                n_generations=n_generations,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='dqn_tuner_genetic',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )
        if "dqn" in models and tuner_id == "optuna":
            tuner_dict['dqn_mushroom_optuna'] = TunerOptuna(
                block_to_opt=dqn,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='dqn_tuner_optuna',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs,
                n_trials=n_trials
            )
        if "ppo" in models and tuner_id == "genetic":
            tuner_dict['ppo_mushroom_genetic'] = TunerGenetic(
                block_to_opt=ppo,
                n_agents=n_agents,
                n_generations=n_generations,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='ppo_tuner_genetic',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )
        if "ppo" in models and tuner_id == "optuna":
            tuner_dict['ppo_mushroom_optuna'] = TunerOptuna(
                block_to_opt=ppo,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='ppo_tuner_optuna',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs,
                n_trials=n_trials
            )
        if "sac" in models and tuner_id == "genetic":
            tuner_dict['sac_mushroom_genetic'] = TunerGenetic(
                block_to_opt=sac,
                n_agents=n_agents,
                n_generations=n_generations,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='sac_tuner_genetic',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )
        if "sac" in models and tuner_id == "optuna":
            tuner_dict['sac_mushroom_optuna'] = TunerOptuna(
                block_to_opt=sac,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='sac_tuner_optuna',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs,
                n_trials=n_trials
            )
        if "gpomdp" in models and tuner_id == "genetic":
            tuner_dict['gpomdp_mushroom_genetic'] = TunerGenetic(
                block_to_opt=gpomdp,
                n_agents=n_agents,
                n_generations=n_generations,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='gpomdp_tuner_genetic',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs
            )
        if "gpomdp" in models and tuner_id == "optuna":
            tuner_dict['gpomdp_mushroom_optuna'] = TunerOptuna(
                block_to_opt=gpomdp,
                eval_metric=metric,
                input_loader=input_loader_online,
                obj_name='gpomdp_tuner_optuna',
                checkpoint_log_path=self.dir_chkpath,
                n_jobs=n_jobs,
                n_trials=n_trials
            )

        auto_generation = AutoModelGeneration(
            tuner_blocks_dict=tuner_dict,
            eval_metric=metric,
            obj_name='auto_generation',
            log_mode="console",
            checkpoint_log_path=self.dir_chkpath,
            n_jobs=n_jobs
        )

        pipeline = OnlineRLPipeline(
            list_of_block_objects=[auto_generation],
            eval_metric=metric,
            obj_name='online_pipeline',
            log_mode="console",
            n_jobs=n_jobs,
            checkpoint_log_path=self.dir_chkpath
        )
        out = pipeline.learn(env=env)
        print(out)

        run_payload = {
            "id": run_id,
            "configuration_id": None,
            "gym_id": None,
            "gym_params": [],
            "status": "finished",
            "created_on": None
        }
        requests.post(os.getenv("AUTORL_X_SERVER_URL", "http://localhost:8000") + "/api/runs", json=run_payload)

    # Create an instance of the AutoModelGeneration class
    # auto_model_gen_1 = ModelGenerationMushroomOnlineDQN(
    #     eval_metric=DiscountedReward(obj_name='discounted_rew_auto_model_gen', n_episodes=10,
    #                                  batch=False, n_jobs=1, job_type='process',
    #                                  log_mode=self.log_mode, checkpoint_log_path=self.dir_chkpath),
    #     obj_name='auto_model_gen', log_mode=self.log_mode)

    # auto_model_gen = AutoModelGeneration(
    #     eval_metric=DiscountedReward(obj_name='discounted_rew_auto_model_gen', n_episodes=10,
    #                                  batch=False, n_jobs=1, job_type='process',
    #                                  log_mode=self.log_mode, checkpoint_log_path=self.dir_chkpath),
    #     obj_name='auto_model_gen', log_mode=self.log_mode)

    # Create a pipeline with the auto_model_gen block

    # # This runs the PPO model
    # def run_ppo(self):
    #     my_env = MyEnv()
    #
    #     # Create an instance of the AutoModelGeneration class
    #     auto_model_gen = ModelGenerationMushroomOnlinePPO(
    #         eval_metric=DiscountedReward(obj_name='discounted_rew_auto_model_gen', n_episodes=10,
    #                                      batch=False, n_jobs=1, job_type='process',
    #                                      log_mode=self.log_mode, checkpoint_log_path=self.dir_chkpath),
    #         obj_name='auto_model_gen', log_mode=self.log_mode)
    #
    #     # Create a pipeline with the auto_model_gen block
    #     my_pipeline = OnlineRLPipeline(list_of_block_objects=[auto_model_gen],
    #                                    eval_metric=DiscountedReward(obj_name='pipeline_metric', n_episodes=10,
    #                                                                 batch=True,
    #                                                                 log_mode=self.log_mode,
    #                                                                 checkpoint_log_path=self.dir_chkpath),
    #                                    obj_name='OnlinePipeline', log_mode=self.log_mode,
    #                                    checkpoint_log_path=self.dir_chkpath)
    #
    #     # Use the pipeline to learn and get the result
    #     out = my_pipeline.learn(env=my_env)
    #     print(out)
    #
    # # This runs the DDPG model
    # def run_ddpg(self):
    #     my_env = MyEnv()
    #
    #     # Create an instance of the AutoModelGeneration class
    #     auto_model_gen = ModelGenerationMushroomOnlineDDPG(
    #         eval_metric=DiscountedReward(obj_name='discounted_rew_auto_model_gen', n_episodes=10,
    #                                      batch=False, n_jobs=1, job_type='process',
    #                                      log_mode=self.log_mode, checkpoint_log_path=self.dir_chkpath),
    #         obj_name='auto_model_gen', log_mode=self.log_mode)
    #
    #     # Create a pipeline with the auto_model_gen block
    #     my_pipeline = OnlineRLPipeline(list_of_block_objects=[auto_model_gen],
    #                                    eval_metric=DiscountedReward(obj_name='pipeline_metric', n_episodes=10,
    #                                                                 batch=True,
    #                                                                 log_mode=self.log_mode,
    #                                                                 checkpoint_log_path=self.dir_chkpath),
    #                                    obj_name='OnlinePipeline', log_mode=self.log_mode,
    #                                    checkpoint_log_path=self.dir_chkpath)
    #
    #     # Use the pipeline to learn and get the result
    #     out = my_pipeline.learn(env=my_env)
    #     print(out)
    #
    # # This runs the SAC model
    # def run_sac(self):
    #     my_env = MyEnv()
    #
    #     # Create an instance of the AutoModelGeneration class
    #     auto_model_gen = ModelGenerationMushroomOnlineSAC(
    #         eval_metric=DiscountedReward(obj_name='discounted_rew_auto_model_gen', n_episodes=10,
    #                                      batch=False, n_jobs=1, job_type='process',
    #                                      log_mode=self.log_mode, checkpoint_log_path=self.dir_chkpath),
    #         obj_name='auto_model_gen', log_mode=self.log_mode)
    #
    #     # Create a pipeline with the auto_model_gen block
    #     my_pipeline = OnlineRLPipeline(list_of_block_objects=[auto_model_gen],
    #                                    eval_metric=DiscountedReward(obj_name='pipeline_metric', n_episodes=10,
    #                                                                 batch=True,
    #                                                                 log_mode=self.log_mode,
    #                                                                 checkpoint_log_path=self.dir_chkpath),
    #                                    obj_name='OnlinePipeline', log_mode=self.log_mode,
    #                                    checkpoint_log_path=self.dir_chkpath)
    #
    #     # Use the pipeline to learn and get the result
    #     out = my_pipeline.learn(env=my_env)
    #     print(out)
    #
    # # This runs the GPOMDP model
    # def run_gpomdp(self):
    #     my_env = MyEnv()
    #
    #     # Create an instance of the AutoModelGeneration class
    #     auto_model_gen = ModelGenerationMushroomOnlineGPOMDP(
    #         eval_metric=DiscountedReward(obj_name='discounted_rew_auto_model_gen', n_episodes=10,
    #                                      batch=False, n_jobs=1, job_type='process',
    #                                      log_mode=self.log_mode, checkpoint_log_path=self.dir_chkpath),
    #         obj_name='auto_model_gen', log_mode=self.log_mode)
    #
    #     # Create a pipeline with the auto_model_gen block
    #     my_pipeline = OnlineRLPipeline(list_of_block_objects=[auto_model_gen],
    #                                    eval_metric=DiscountedReward(obj_name='pipeline_metric', n_episodes=10,
    #                                                                 batch=True,
    #                                                                 log_mode=self.log_mode,
    #                                                                 checkpoint_log_path=self.dir_chkpath),
    #                                    obj_name='OnlinePipeline', log_mode=self.log_mode,
    #                                    checkpoint_log_path=self.dir_chkpath)
    #     # Use the pipeline to learn and get the result
    #     out = my_pipeline.learn(env=my_env)
    #     print(out)
    #
    # # Configuring an Agent with Hyperparameters in ARLO
    # def configure_model_generation(self, eval_metric, obj_name, **kwargs):
    #     print("MODEL GEN")
    #     self.model_gen = ModelGeneration(eval_metric, obj_name, **kwargs)
    #     if self.model_gen:
    #         self.logger.info("ModelGeneration block configured successfully.")
    #     else:
    #         self.logger.error("Error in configuring ModelGeneration block.")
    #     return
    #
    # def set_policy(self, policy, regressor_type, approximator=None):
    #     if self.model_gen:
    #         self.policy = self.model_gen.construct_policy(policy, regressor_type, approximator)
    #         if self.policy:
    #             self.logger.info("Policy set successfully.")
    #         else:
    #             self.logger.error("Error in setting policy.")
    #     else:
    #         self.logger.error("ModelGeneration block not configured. Please configure it first.")
    #
    # def start_training(self, train_data=None, env=None):
    #     if not self.model_gen:
    #         self.logger.error("ModelGeneration block not configured. Please configure it first.")
    #         return
    #     if not self.policy:
    #         self.logger.error("Policy not set. Please set the policy first.")
    #         return
    #
    #     # Use provided train_data and env or use existing ones.
    #     train_data = train_data or self.train_data
    #     env = env or self.env
    #
    #     output = self.model_gen.learn(train_data, env)
    #     if output:
    #         self.logger.info("Training started successfully.")
    #     else:
    #         self.logger.error("Error in starting training.")
    #
    # def get_params(self):
    #     if self.model_gen:
    #         return self.model_gen.get_params()
    #     else:
    #         self.logger.error("ModelGeneration block not configured. Please configure it first.")
    #         return None
    #
    # def set_params(self, params):
    #     if self.model_gen:
    #         return self.model_gen.set_params(params)
    #     else:
    #         self.logger.error("ModelGeneration block not configured. Please configure it first.")
    #         return None
