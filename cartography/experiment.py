from abc import ABCMeta, abstractmethod
import os
import yaml

from models import Experiment


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


class ParamFileLoader:
    def __init__(self, param_file, delim='\t'):
        self.param_file = param_file
        self.delim = delim

    def load(self):
        params = []
        with open(self.param_file) as fin:
            fin.readline()  # reads column names
            for line in fin:
                params.append(self._parse_line(line))
        return params

    def _parse_line(self, line):
        channel, name, param_class, max_val = line.strip('\n').split(self.delim)
        return {
            'name': name or None,
            'param_class': param_class or None,
            'channel': int(channel) if channel else None,
            'max_val': int(max_val) if max_val else None
        }


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
