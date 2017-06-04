import os
import yaml

from cartography.models import (MidiParamClass, MidiParamType, Experiment)


class SqlExperimentHandler(object):
    def __init__(self):
        self.delegate = None

    def create_from_config(self, config_file):
        assert os.path.isfile(config_file), \
            "config file {} not found".format(config_file)
        config = yaml.load(open(config_file, 'r').read())
        self.delegate = Experiment.create(description=config.get('description', ''))

    def load_existing(self, experiment_id):
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


class SqlParamHandler:
    def create_from_file(self, param_file):
        for param in ParamFileLoader(param_file).load():
            if 'param_class' in param:
                param_class, _ = MidiParamClass.get_or_create(name=param['param_class'])
                param['param_class'] = param_class
            MidiParamType.get_or_create(**param)
