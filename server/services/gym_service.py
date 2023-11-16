import api as api
from services import db_service
import numpy as np
from random import randrange


class Gyms:

    def __init__(self, db: db_service.Database):
        self.db = db

    def push_gym(self, gym: api.Gym):
        """Push a gym."""
        return self.db.insert_gym(gym)

    def push_gym_param(self, gym_param: api.GymParam):
        """Push a gym param."""
        if self.db.get_gym_param(gym_param["id"]):
            self.db.update_gym_param(gym_param)
        else:
            self.db.insert_gym_param(gym_param)

    def get_gym(self, gym_id: str) -> api.Gym:
        """Get a gym."""
        # TODO load from self.db
        gym = api.Gym(id=gym_id, name="xyz", code="import xyz")
        return gym

    def get_gyms(self) -> [api.Gym]:
        """Get all gyms."""
        return self.db.get_gyms()

    def delete_gym(self, gym_id: str) -> bool:
        """Delete a gym."""
        return self.db.delete_gym(gym_id)

    def probe_space(self, space: api.Space) -> api.SpaceProbe:
        """Probe observation or action space."""
        try:
            if space["type"] == "box":
                return {
                    "value": np.random.uniform(
                        low=eval(space["low"]),
                        high=eval(space["high"]),
                        size=(space["size"],)
                    ).tolist()
                }
            elif space["type"] == "discrete":
                return {
                    "value": randrange(int(space["size"]))
                }
        except:
            return {
                "value": None
            }
