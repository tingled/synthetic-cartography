import numpy as np
from numpy.testing import assert_equal
import pandas as pd
from unittest import TestCase

from cartography.virus_utils import VirusPresetGenerator


class TestVirusPresetGenerator(TestCase):
    def test_create_categorical_probs(self):
        preset_vals = [0, 3, 1, 1, 4]
        min_val = 0
        max_val = 4

        got = VirusPresetGenerator._create_categorical_probs(
                preset_vals=preset_vals, min_val=min_val, max_val=max_val)

        expected = np.array([0.2, 0.4, 0, 0.2, 0.2])

        assert_equal(got, expected)

        min_val = 0
        max_val = 3  # should ignore values > 3

        got = VirusPresetGenerator._create_categorical_probs(
                preset_vals=preset_vals, min_val=min_val, max_val=max_val)

        expected = np.array([0.25, 0.5, 0, 0.25])

        assert_equal(got, expected)

    def test_create_categorical_dist(self):
        preset_vals = np.array([1, 1, 1])
        min_val = 0
        max_val = 9

        expected = 1
        got = VirusPresetGenerator._create_categorical_dist(
                preset_vals=preset_vals, min_val=min_val, max_val=max_val)()

        self.assertIsInstance(got, np.int64)
        self.assertEqual(got, expected)

    def test_create_triangular_dist(self):
        preset_vals = np.array([1, 1, 1])
        min_val = 0
        max_val = 9
        n = 1000
        samples = []

        for i in range(n):
            got = VirusPresetGenerator._create_categorical_dist(
                    preset_vals=preset_vals, min_val=min_val, max_val=max_val)()
            self.assertGreaterEqual(got, 0)
            self.assertLessEqual(got, 9)
            samples.append(got)

        self.assertIsInstance(got, np.int64)

        # mean of samples should be less than 5
        self.assertLess(np.array(samples).mean(), 5)

    def test_generate_patch(self):
        preset_data = pd.DataFrame(
            {
                'param1': [0, 0, 0],
                'param2': [100, 112, 123],
            })
        n = 100

        gen = VirusPresetGenerator(preset_data=preset_data, uniq_val_thresh=3)

        samples = []
        for i in range(n):
            patch = gen.generate_patch()
            self.assertEqual(len(patch), 2)
            self.assertEqual(patch[0], 0)
            samples.append(patch[1])

        self.assertGreater(np.array(samples).mean(), 64)
