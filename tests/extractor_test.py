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

    def test_mfcc_no_deltas(self):
        extractor = LibrosaFeatureExtractor(None)

        num_mfccs = 13
        input_params = [
                {
                    'num_mfccs': num_mfccs,
                    'delta_mfccs': False,
                    'delta2_mfccs': False
                },
                {
                    'num_mfccs': num_mfccs,
                    'delta_mfccs': True,
                    'delta2_mfccs': False
                },
                {
                    'num_mfccs': num_mfccs,
                    'delta_mfccs': True,
                    'delta2_mfccs': True
                }
        ]
        expected = [num_mfccs, num_mfccs*2, num_mfccs*3]

        for mfcc_kwargs, expected_rows in zip(input_params, expected):
            got = extractor._mfcc(self.test_signal, self.test_sr,
                    **mfcc_kwargs)
            self.assertEqual(expected_rows, got.shape[0])
