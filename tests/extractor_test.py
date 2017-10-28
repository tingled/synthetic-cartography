import numpy as np
from unittest import TestCase

from cartography.extractor import LibrosaFeatureExtractor


def gen_signal(dur, sr, freq):
    return np.pi * 2 * freq * np.arange(dur * sr) / float(sr)


class TestLibrosaFeatureExtractor(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dur = 2
        cls.test_freq = 440
        cls.test_sr = 22050
        cls.test_signal = gen_signal(cls.test_dur, cls.test_sr, cls.test_freq)

    def test_mfcc(self):
        extractor = LibrosaFeatureExtractor(None)

        num_mfccs = 13
        mfccs_kwargs = {
                'num_mfccs': num_mfccs,
                'delta_mfccs': False,
                'delta2_mfccs': False
        }
        expected_columns = 13
        got = extractor._mfcc(self.test_signal, self.test_sr, **mfccs_kwargs)
        self.assertEqual(expected_columns, got.shape[0])
