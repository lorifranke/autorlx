CREATE TABLE catalog
(
    `id`               varchar(255) NOT NULL,
    `naics_code_2022`  varchar(255) NOT NULL,
    `naics_title_2022` varchar(255) NOT NULL,
    `created_on`       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)

CREATE TABLE gyms
(
    `id`               varchar(255) NOT NULL,
    `name`             varchar(255) NOT NULL,
    `reset`            text NULL,
    `step`             text NULL,
    `custom`           text NULL,
    `code`             text         NOT NULL,
    `visualization`    text NULL,
    `observation_type` varchar(255) NULL,
    `observation_size` int NULL,
    `observation_low`  text NULL,
    `observation_high` text NULL,
    `action_type`      varchar(255) NULL,
    `action_size`      int NULLABLE,
    `action_low`       text NULL,
    `action_high`      text NULL,
    `created_on`       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
);

CREATE TABLE catalog_gym
(
    `id`          varchar(255) NOT NULL,
    `category_id` varchar(255) NOT NULL,
    `gym_id`      varchar(255) NOT NULL,
    `email`       varchar(255) NOT NULL,
    `created_on`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`gym_id`) REFERENCES `gyms` (`id`),
    FOREIGN KEY (`catalog_id`) REFERENCES `catalog` (`id`)
);

CREATE TABLE gym_params
(
    `id`          varchar(255) NOT NULL,
    `gym_id`      varchar(255) NOT NULL,
    `name`        varchar(255) NOT NULL,
    `description` text         NOT NULL,
    `type`        enum('str', 'int', 'float', 'bool') NOT NULL,
    `default`     varchar(255) NULL,
    `created_on`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`gym_id`) REFERENCES `gyms` (`id`)
)

CREATE TABLE gym_modules
(
    `id`         varchar(255) NOT NULL,
    `gym_id`     varchar(255) NOT NULL,
    `type`       varchar(255) NOT NULL,
    `module`     varchar(255) NOT NULL,
    `submodules` varchar(255) NOT NULL,
    `created_on` timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`gym_id`) REFERENCES `gyms` (`id`)
)

CREATE TABLE models
(
    `id`          varchar(255) NOT NULL,
    `name`        varchar(255) NOT NULL,
    `description` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO models (id, name, description)
VALUES ('dqn', 'Deep Q-Network',
        'A deep learning model that combines Q-learning with deep neural networks to approximate the Q-values.'),
       ('ppo', 'Proximal Policy Optimization',
        'A policy gradient algorithm which uses a surrogate objective to optimize and stabilize training by clipping the policy update.'),
       ('sac', 'Soft Actor Critic',
        'An off-policy actor-critic algorithm that optimizes the entropy-augmented expected reward to improve exploration.'),
       ('ddpg', 'Deep Deterministic Policy Gradient',
        'An algorithm that utilizes deep neural networks to represent actor and critic in continuous action spaces.'),
       ('gpomdp', 'Partially Observable Markov Decision Processes',
        'Simulation-based algorithm for generating a biased estimate of the gradient of the average reward controlled by parameterized stochastic policies.'),
       ('fqi', 'Fitted-Q Iteration',
        'An algorithm that applies supervised learning techniques to estimate the Q-function iteratively.'),
       ('doublefqi', 'Double Fitted-Q Iteration',
        'An enhancement of FQI which reduces overestimation bias by selecting the best action using one set of parameters and evaluating it with another.'),
       ('lspi', 'Least Squares Policy Iteration',
        'A model-free reinforcement learning method that combines the least squares method with policy iteration to optimize policies.');

CREATE TABLE metrics
(
    `id`          varchar(255) NOT NULL,
    `name`        varchar(255) NOT NULL,
    `description` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO metrics (id, name, description)
VALUES ('td_error', 'Temporal Difference Error',
        'Calculates the average squared deviation between predicted and actual rewards in subsequent states, reflecting the accuracy of the value function.'),
       ('discounted', 'Discounted Reward',
        'Evaluates the average of cumulative rewards received over episodes, adjusted by a discount factor to account for the time value of rewards.'),
       ('tsradiscounted', 'Time Series Rolling Average Discounted Reward',
        'Evaluates the average of cumulative rewards received over episodes, adjusted by a discount factor to account for the time value of rewards.');

CREATE TABLE tuners
(
    `id`          varchar(255) NOT NULL,
    `name`        varchar(255) NOT NULL,
    `description` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO tuners (id, name, description)
VALUES ('genetic', 'Genetic',
        'Genetic hyperparameter tuner that evolves a population of model configurations to optimize performance. It uses processes like mutation and selection across generations to find the best hyperparameters for a given evaluation metric.'),
       ('optuna', 'Optuna',
        'Hyperparameter optimization by searching through a predefined space and evaluating model performance. It uses advanced algorithms to determine the best set of parameters with features like trial pruning and parallel execution to speed up the search.');

CREATE TABLE configurations
(
    `id`            varchar(255) NOT NULL,
    `metric_id`     varchar(255) NOT NULL,
    `tuner_id`      varchar(255) NOT NULL,
    `name`          varchar(255) NOT NULL,
    `n_jobs`        int          NOT NULL,
    `n_episodes`    int          NOT NULL,
    `n_agents`      int          NOT NULL,
    `n_generations` int          NOT NULL,
    `created_on`    timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`metric_id`) REFERENCES `metrics` (`id`),
    FOREIGN KEY (`tuner_id`) REFERENCES `tuners` (`id`)
);


CREATE TABLE configuration_models
(
    `configuration_id` varchar(255) NOT NULL,
    `model_id`         varchar(255) NOT NULL,
    PRIMARY KEY (`configuration_id`, `model_id`),
    FOREIGN KEY (`configuration_id`) REFERENCES `configurations` (`id`),
    FOREIGN KEY (`model_id`) REFERENCES `models` (`id`)
);

CREATE TABLE runs
(
    `id`               varchar(255) NOT NULL,
    `configuration_id` varchar(255) NOT NULL,
    `gym_id`           varchar(255) NOT NULL,
    `status`           enum('new', 'running', 'finished', 'error') NOT NULL,
    `created_on`       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`configuration_id`) REFERENCES `configurations` (`id`),
    FOREIGN KEY (`gym_id`) REFERENCES `gyms` (`id`)
);

CREATE TABLE run_gym_params
(
    `id`           varchar(255) NOT NULL,
    `run_id`       varchar(255) NOT NULL,
    `gym_param_id` varchar(255) NOT NULL,
    `value`        varchar(255) NOT NULL,
    `created_on`   timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`run_id`) REFERENCES `runs` (`id`),
    FOREIGN KEY (`gym_param_id`) REFERENCES `gym_params` (`id`)
)

CREATE TABLE run_models
(
    `id`              varchar(255) NOT NULL,
    `run_id`          varchar(255) NOT NULL,
    `model_id`        varchar(255) NOT NULL,
    `hyperparameters` longtext     NOT NULL,
    `policy`          longtext,
    `status`          enum('new', 'running', 'finished', 'error') NOT NULL,
    `created_on`      timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`run_id`) REFERENCES `runs` (`id`),
    FOREIGN KEY (`model_id`) REFERENCES `models` (`id`)
);

CREATE TABLE run_logs
(
    `id`           varchar(255) NOT NULL,
    `run_id`       varchar(255) NOT NULL,
    `run_model_id` varchar(255),
    `phase`        enum('train', 'test'),
    `epoch`        int,
    `iteration`    int,
    `severity`     enum('info', 'warn', 'error'),
    `log`          text,
    `state`        longtext,
    `action`       longtext,
    `score`        text,
    `reward`       decimal(18, 6),
    `created_on`   timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`run_id`) REFERENCES `runs` (`id`),
    FOREIGN KEY (`run_model_id`) REFERENCES `run_models` (`id`)
);

CREATE TABLE user_study_sessions
(
    `id`    varchar(255)   NOT NULL,
    `time`  datetime(3) NOT NULL,
    `score` decimal(18, 6) NOT NULL,
    PRIMARY KEY (`id`, `time`)
);