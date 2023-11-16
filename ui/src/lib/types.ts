export class Thing {
    id: number;
    name: string;
};

export class GymParam {
    id: string;
    gym_id: string;
    name: string;
    description: string;
    type: string;
    created_on: Date;
};

export class Module {
    id: string;
    gym_id: string;
    type: string;
    module: string;
    submodules: string;
};

export class Space {
    type: string;
    low: string;
    high: string;
    size: number;
};

export class SpaceProbe {
    value: number[] | number;
}

export class Gym {
    id: string;
    name: string;
    step: string;
    reset: string;
    custom: string;
    code: string;
    visualization: string;
    params: GymParam[];
    modules: Module[];
    spaces: {
        observation: Space;
        action: Space;
    };
    created_on: Date;
};

export class CatalogGym {
    id: string;
    gym_id: string;
    category_id: string;
    email: string;
    created_on: Date;
};

export class Catalog {
    title: string;
    categories: Category[];
};

export class Category {
    id: string;
    code: string;
    title: string;
    categories: Category[];
    gyms: CatalogGym[]
};

export class Configuration {
    id: string;
    name: string;
    metric_id: string;
    models: string[];
    n_jobs: number;
    n_episodes: number;
    n_agents: number;
    n_generations: number;
    created_on: Date;
};

export class Metric {
    id: string;
    name: string;
    description: string;
};

export class Model {
    id: string;
    name: string;
    description: string;
};

export class Tuner {
    id: string;
    name: string;
    description: string;
};

export class RunModelLog {
    id: string
    run_model_id: string
    phase: string
    epoch: number
    iteration: number
    severity: string
    log: string
    state: string
    action: string
    score: string
    reward: number
    created_on: Date
};

export class RunModel {
    id: string;
    run_id: string;
    model_id: string;
    hyperparameters: string;
    policy: string;
    status: string;
    logs: RunModelLog[];
    created_on: Date;
}

export class RunLog {
    id: string;
    run_id: string;
    phase: string;
    severity: string;
    log: string;
    created_on: Date;
};

export class RunGymParams {
    id: string;
    run_id: string;
    gym_param_id: string;
    value: string;
    default: string;
    created_on: Date;
};

export class Run {
    id: string;
    status: string;
    gym_id: string;
    configuration_id: string;
    created_on: Date;
    gym_params: RunGymParams[];
    logs: RunLog[];
    models: RunModel[];
};

export class Trajectory {
    action: string;
    state: string;
    score: string;
};

export class UserStudySessionScores {
    score: number;
    time: Date;
};

export class UserStudySession {
    id: string;
    scores: UserStudySessionScores[];
};


