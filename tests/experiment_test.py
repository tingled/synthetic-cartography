import os

from datetime import datetime, timedelta
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from unittest import TestCase

from cartography.models import Experiment
from cartography.experiment import (
    SqlExperimentHandler, ParamFileLoader
)
test_db = SqliteDatabase(':memory:')


class TestSqlExperimentHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_dir = 'tests/fixtures/'
        cls.config_file = os.path.join(fixture_dir, 'experiment_config.yaml')
        cls.config_data = {'description': 'test experiment'}


    def test_create_from_config(self):
        with test_database(test_db, (Experiment,)):
            exp = SqlExperimentHandler()
            exp.create_from_config(self.config_file)

            experiments = Experiment.select()
            self.assertEqual(len(experiments), 1)
            exp_row = experiments[0]
            self.assertEqual(exp_row.description, self.config_data.get('description'))
            cur_dt = datetime.now()
            got_dt = exp_row.datetime
            diff_dt = cur_dt - got_dt
            self.assertLess(abs(diff_dt.seconds), 3)

    def test_load_existing(self):
        with test_database(test_db, (Experiment,)):
            expected_experiment = Experiment.create(**self.config_data)
            expected_experiment_id = 1

            exp = SqlExperimentHandler()
            exp.load_existing(expected_experiment_id)
            self.assertEqual(expected_experiment, exp.delegate)


class TestSqlParamHandler(TestCase):
    pass


class TestParamFileLoader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_param_file = 'tests/fixtures/midi_params.tsv'
        cls.expected_params = [
                {'name': 'osc1 shape', 'channel': 1, 'param_class': 'osc1', 'max_val': None},
                {'name': 'osc1 wave select', 'channel': 2, 'param_class': 'osc1', 'max_val': 63},
                {'name': 'osc balance', 'channel': 3, 'param_class': None, 'max_val': None}
        ]

    def test_load(self):
        param_loader = ParamFileLoader(self.fixture_param_file)
        params = param_loader.load()

        self.assertEqual(len(params), len(self.expected_params))
        for i in range(len(self.expected_params)):
            self.assertEqual(set(params[i].items()), set(self.expected_params[i].items()))
