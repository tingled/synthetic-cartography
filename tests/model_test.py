import os

from shutil import rmtree
from unittest import TestCase
from peewee import Database

from cartography.models import BaseModel


class MidiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = 'tests/tmp/'
        if not os.path.isdir(cls.tmp_dir):
            os.mkdir(cls.tmp_dir)

        cls.test_sqlite_path = os.path.join(cls.tmp_dir, 'test.db')

    def tearDown(self):
        if os.path.isfile(self.test_sqlite_path):
            os.remove(self.test_sqlite_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(cls.tmp_dir):
            rmtree(cls.tmp_dir)

    def test_init_db(self):
        self.assertTrue(BaseModel._meta.database.deferred)
        BaseModel.init_db(':memory:')
        self.assertFalse(BaseModel._meta.database.deferred)
        self.assertIsInstance(BaseModel._meta.database, Database)
