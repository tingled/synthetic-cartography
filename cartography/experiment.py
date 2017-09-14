from abc import ABCMeta, abstractmethod
import os
import yaml

from cartography.models import Experiment


class ExperimentHandler(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def load_config(self):
        assert os.path.isfile(self.config_file), \
            "config file {} not found".format(self.config_file)

        self.config = yaml.load(open(self.config_file, 'r').read())


class SqlExperimentHandler(ExperimentHandler):
    def __init__(self, config_file):
        super(SqlExperimentHandler, self).__init__(config_file)
        self.delegate = None
        self.config = None

    def create_experiment(self):
        self.delegate = Experiment.create(description=self.config.get('description', ''))

    def load_experiment(self, experiment_id):
        self.delegate = Experiment.get(Experiment.id == experiment_id)


class ParamHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def active_params(self):
        pass


class SqlParamHandler:
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id

    def active_params(self):
        pass
