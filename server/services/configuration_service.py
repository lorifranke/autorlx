import api as api
from services import db_service


class Configurations:

    def __init__(self, db: db_service.Database):
        self.db = db

    def push_configuration(self, configuration: api.Configuration):
        """Push a configuration."""
        return self.db.insert_configuration(configuration)

    def get_configuration(self, configuration_id: str) -> api.Configuration:
        """Get a configuration."""
        # TODO load from self.db
        configuration = api.Configuration(id=configuration_id, name="xyz", models=["xyz", "abc", "dqn"])
        return configuration

    def get_configurations(self) -> [api.Configuration]:
        """Get all configurations."""
        return self.db.get_configurations()

    def delete_configuration(self, configuration_id: str) -> bool:
        """Delete a configuration."""
        return self.db.delete_configuration(configuration_id)

    def get_metrics(self) -> [api.Metric]:
        """Get all metrics."""
        return self.db.get_metrics()

    def get_models(self) -> [api.Model]:
        """Get all models."""
        return self.db.get_models()

    def get_tuners(self) -> [api.Tuner]:
        """Get all tuners."""
        return self.db.get_tuners()
