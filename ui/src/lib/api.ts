import {
    Thing,
    Gym,
    Configuration,
    Run,
    Model,
    UserStudySession,
    Metric,
    Tuner,
    Trajectory,
    Catalog,
    CatalogGym,
    Space, SpaceProbe
} from "$lib";

export class API {
    constructor(
        private api_url: string
    ) {
    }

    pushGym = async (gym: Gym): Promise<any> =>
        fetch(`${this.api_url}/api/gyms`, {
            method: 'POST',
            body: JSON.stringify(gym),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then(response => response.json());

    deleteGym = async (gym_id: string): Promise<any> =>
        fetch(`${this.api_url}/api/gyms/${gym_id}`, {method: 'DELETE'}).then(response => response.json());

    getGyms = async (): Promise<Gym[]> =>
        fetch(`${this.api_url}/api/gyms`).then(async gyms => await gyms.json());

    probeSpace = async (space: Space): Promise<SpaceProbe> =>
        fetch(`${this.api_url}/api/gyms/probe_space`, {
            method: 'POST',
            body: JSON.stringify(space),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then(response => response.json());

    pushConfiguration = async (configuration: Configuration): Promise<any> =>
        fetch(`${this.api_url}/api/configurations`, {
            method: 'POST',
            body: JSON.stringify(configuration),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then(response => response.json());

    deleteConfiguration = async (configuration_id: string): Promise<any> =>
        fetch(`${this.api_url}/api/configurations/${configuration_id}`, {method: 'DELETE'}).then(response => response.json());

    getConfigurations = async (): Promise<Configuration[]> =>
        fetch(`${this.api_url}/api/configurations`).then(async configurations => await configurations.json());

    getMetrics = async (): Promise<Metric[]> =>
        fetch(`${this.api_url}/api/metrics`).then(async metrics => await metrics.json());

    getModels = async (): Promise<Model[]> =>
        fetch(`${this.api_url}/api/models`).then(async models => await models.json());

    getTuners = async (): Promise<Tuner[]> =>
        fetch(`${this.api_url}/api/tuners`).then(async tuners => await tuners.json());

    getRuns = async (): Promise<Run[]> =>
        fetch(`${this.api_url}/api/runs`).then(async runs => await runs.json());

    run = async (run: Run): Promise<any> =>
        fetch(`${this.api_url}/api/runs`, {
            method: 'POST',
            body: JSON.stringify(run),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then(response => response.json());

    deleteRun = async (run_id: string): Promise<any> =>
        fetch(`${this.api_url}/api/runs/${run_id}`, {method: 'DELETE'}).then(response => response.json());

    pushUserStudySession = async (session: UserStudySession): Promise<any> =>
        fetch(`${this.api_url}/api/user_study_session`, {
            method: 'POST',
            body: JSON.stringify(session),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then(response => response.json());

    getTrajectory = async (run_model_id: string, epoch: number, iteration: number): Promise<Trajectory> =>
        fetch(`${this.api_url}/api/trajectory/${run_model_id}/${epoch}/${iteration}`).then(async trajectory => await trajectory.json());

    getCatalog = async (): Promise<Catalog> =>
        fetch(`${this.api_url}/api/catalog`).then(async catalog => await catalog.json());

    pushCatalogGym = async (catalog_gym: CatalogGym): Promise<any> =>
        fetch(`${this.api_url}/api/catalog`, {
            method: 'POST',
            body: JSON.stringify(catalog_gym),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then(response => response.json());

    deleteCatalogGym = async (gymId: number): Promise<any> =>
        fetch(`${this.api_url}/api/catalog/${gymId}`, {method: 'DELETE'})

    getThings = async (): Promise<Thing[]> =>
        fetch(`${this.api_url}/api/test/get`).then(async things => await things.json())

    deleteThing = async (id: number): Promise<any> =>
        fetch(`${this.api_url}/api/test/delete/${id}`, {method: 'DELETE'})

    pushThing = async (some: Thing): Promise<any> =>
        fetch(`${this.api_url}/api/test/push`, {
            method: 'POST',
            body: JSON.stringify(some),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }).then(response => response.json())

}