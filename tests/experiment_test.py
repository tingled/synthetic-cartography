import os

from datetime import datetime, timedelta
from peewee import SqliteDatabase
from playhouse.test_utils import test_database
from unittest import TestCase

from cartography.models import Experiment
from cartography.experiment import (
    ExperimentHandler, SqlExperimentHandler
)
test_db = SqliteDatabase(':memory:')

class TestExperimentHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_dir = 'tests/fixtures/'
        cls.config_file = os.path.join(fixture_dir, 'experiment_config.yaml')
        cls.config_data = {'description': 'test experiment'}

    def test_load_config(self):
        exp = ExperimentHandler(self.config_file)
        exp.load_config()
        self.assertEqual(exp.config, self.config_data)

    def test_iter_params(self):
        pass


class TestSqlExperimentHandler(TestExperimentHandler):
    def test_create_experiment(self):
        with test_database(test_db, (Experiment,)):
            exp = SqlExperimentHandler(self.config_file)
            exp.load_config()
            exp.create_experiment()

            experiments = Experiment.select()
            self.assertEqual(len(experiments), 1)
            exp_row = experiments[0]
            self.assertEqual(exp_row.description, self.config_data.get('description'))
            cur_dt = datetime.now()
            got_dt = exp_row.datetime
            diff_dt = cur_dt - got_dt
            self.assertLess(abs(diff_dt.seconds), 3)

