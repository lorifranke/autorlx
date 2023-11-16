from datetime import datetime
from pydantic import BaseModel
import numpy as np
from typing import *


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash(self.json())

    @classmethod
    def validate(cls, v: np.ndarray):
        return v


class Thing(HashableBaseModel):
    id: int
    name: str


class GymParam(HashableBaseModel):
    id: str
    gym_id: str
    name: str
    description: str
    type: str
    default: str
    created_on: datetime


class Module(HashableBaseModel):
    id: str
    gym_id: str
    type: str
    module: str
    submodules: str


class Space(HashableBaseModel):
    type: str
    low: str
    high: str
    size: int


class Spaces(HashableBaseModel):
    observation: Space
    action: Space


class Gym(HashableBaseModel):
    id: str
    name: str
    step: str
    reset: str
    custom: str
    code: str
    visualization: str
    params: List[GymParam]
    modules: List[Module]
    spaces: Spaces
    created_on: datetime


class CatalogGym(HashableBaseModel):
    id: str
    gym_id: str
    category_id: str
    email: str
    created_on: datetime


class Category(HashableBaseModel):
    id: str
    code: str
    title: str
    categories: List['Category']
    gyms: List[CatalogGym]


class Catalog(HashableBaseModel):
    title: str
    categories: List[Category]


class Configuration(HashableBaseModel):
    id: str
    name: str
    metric_id: str
    tuner_id: str
    models: List[str]
    n_jobs: int
    n_episodes: int
    n_agents: int
    n_generations: int
    created_on: datetime


class Model(HashableBaseModel):
    id: str
    name: str
    description: str


class Metric(HashableBaseModel):
    id: str
    name: str
    description: str


class Tuner(HashableBaseModel):
    id: str
    name: str
    description: str


class RunLaunchGymParam(HashableBaseModel):
    id: str
    run_id: str
    gym_param_id: str
    value: str
    created_on: datetime


class RunLaunch(HashableBaseModel):
    id: str
    configuration_id: str
    gym_id: str
    gym_params: List[RunLaunchGymParam]
    status: str
    created_on: datetime


class RunLog(HashableBaseModel):
    id: str
    run_id: str
    phase: str
    severity: str
    log: str
    created_on: datetime


class RunModelLog(HashableBaseModel):
    id: str
    run_id: str
    run_model_id: str
    phase: str
    epoch: int
    iteration: int
    severity: str
    log: str
    state: str
    action: str
    score: str
    reward: float
    created_on: datetime


class RunModelLaunch(HashableBaseModel):
    id: str
    run_id: str
    model_id: str
    hyperparameters: str
    policy: str
    status: str
    created_on: datetime


class RunModel(HashableBaseModel):
    id: str
    run_id: str
    model_id: str
    hyperparameters: str
    policy: str
    status: str
    logs: List[RunModelLog]
    created_on: datetime


class RunGymParam(HashableBaseModel):
    id: str
    name: str
    description: str
    type: str
    value: str
    created_on: datetime


class RunInfo(HashableBaseModel):
    id: str
    configuration_id: str
    gym_id: str
    status: str
    gym_params: List[RunGymParam]
    models: List[RunModel]
    logs: List[RunLog]
    created_on: datetime


class Trajectory(HashableBaseModel):
    action: str
    state: str
    score: str


class SpaceProbe(HashableBaseModel):
    value: Union[List[float], float]


class UserStudySessionScore(HashableBaseModel):
    time: datetime
    score: float


class UserStudySession(HashableBaseModel):
    id: str
    scores: List[UserStudySessionScore]
