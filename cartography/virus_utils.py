"""
we can inspect the factory installed presets for the access virus
by reading its MIDI sysex dumps.

these messages are formatted: (0, 32, 51, 1, dd, 16, bb, ss, [256 ints], cs)
where dd is the device id, bb is bank, ss is program number, and cs is checksum

we can also use this same fromat to write parameters to the working preset

for more info see page 255 of the virus B manual: https://www.virus.info/downloads
"""

from mido import Message
import numpy as np
from numpy import ndarray
import pandas as pd
from pandas import DataFrame
import random
from typing import Callable, List

VIRUS_SYSEX_HEADER = [0, 32, 51, 1, 0, 16, 0, 127]
VIRUS_SYSEX_CHECKSUM = [0]  # this value seems to be ignored on write
# 241-250 control the title string


def parse_virus_preset_dump(msg: Message) -> List[int]:
    """
    strips sysex header and checksum bits to return list of presets
    """
    data = list(msg.data[len(VIRUS_SYSEX_HEADER): -len(VIRUS_SYSEX_CHECKSUM)])
    assert len(data) == 256
    return data


def create_virus_preset_msg(params: list) -> Message:
    """
    takes a list of 256 parameter values and creates a Mido sysex message
    to update the virus
    """
    assert len(params) == 256, params
    data = VIRUS_SYSEX_HEADER + params + VIRUS_SYSEX_CHECKSUM
    return Message('sysex', data=data)


class VirusPresetGenerator:
    def __init__(
        self,
        preset_path: str = None,
        preset_data: DataFrame = None,
        uniq_val_thresh: int = 10
    ):
        """
        either a path to a csv file or a dataframe must be passed in
        """
        assert (preset_path is not None) or (preset_data is not None)
        if preset_data is None:
            preset_data = self.load_presets_from_csv(preset_path)
        self.preset_data = preset_data
        self.distributions = self.create_distributions(preset_data, uniq_val_thresh)

    def load_presets_from_csv(self, preset_path: str) -> DataFrame:
        return pd.read_csv(preset_path)

    @staticmethod
    def _create_categorical_probs(
        preset_vals: ndarray,
        min_val: int,
        max_val: int,
    ) -> ndarray:
        """
        returns an array x s.t. x[i] is the probability of i occuring in preset_vals

        :arg preset_vals: observed values whose probability density we want to model
        :arg min_val: smallest possible value
        :arg max_val: largest possible value
        """
        counts = dict(zip(*np.unique(preset_vals, return_counts=True)))
        counts = np.array([counts.get(i, 0) for i in range(min_val, max_val+1)])
        return counts / counts.sum()

    @staticmethod
    def _create_categorical_dist(
        preset_vals: ndarray,
        min_val: int = 0,
        max_val: int = 127,
    ) -> Callable[[], int]:
        """
        a large number of Virus parameter values are either categorical
        (eg LFO shape) or have an unusual distribution in the factory
        presets. for these parameters, we want to sample from the
        observed probabilites of each value in the factory presets

        :arg preset_vals: parameter values observed in factory presets. this is the distribution
            we'd like to model.
        :arg min_val: smallest possible value
        :arg max_val: largest possible value
        """
        values = np.arange(min_val, max_val+1)
        probs = VirusPresetGenerator._create_categorical_probs(
                preset_vals, min_val=min_val, max_val=max_val)

        def f():
            return np.random.choice(values, 1, p=probs)[0]

        return f

    @staticmethod
    def _create_triangular_dist(
        preset_vals: ndarray,
        min_val: int = 0,
        max_val: int = 127,
    ) -> Callable[[], int]:
        """
        instead of using a uniform distribution for [0, 127], we'll use a
        triangular distribution to account for the fact that some presets
        will have mode that isn't centered

        :arg preset_vals: parameter values observed in factory presets. this is the distribution
            we'd like to model.
        :arg min_val: smallest possible value
        :arg max_val: largest possible value
        """
        def f():
            return int(np.round(np.random.triangular(0, preset_vals.mean(), 127)))
        return f

    def create_distributions(
        self,
        preset_data: DataFrame,
        uniq_val_thresh: int = 10
    ) -> List[Callable[[], int]]:
        """
        creates a map that maps the index of a virus synth parameter to
        a method that can be used to sample a new value based on that
        parameter's distribution of values in the factory presets

        if a particular paramter has fewer than `uniq_val_thresh` values
        in the 256 factory presets, we assume this to be a categorical
        param, eg LFO shape. for these parameters, we want to only
        sample values observed in the factory presets.
        """
        distributions = []
        for i in preset_data.columns:
            preset_vals = preset_data[i].to_numpy()
            if len(preset_data[i].unique()) < uniq_val_thresh:
                distributions.append(self._create_categorical_dist(preset_vals))
            else:
                distributions.append(self._create_triangular_dist(preset_vals))
        return distributions

    def generate_preset(self) -> List[int]:
        return [d() for d in self.distributions]

    def generate_preset_from_seed(self, seed_id: int, n_diff_params: int = 25):
        """
        creates a new preset based on a stored preset.

        :arg seed_id: id of saved preset (max 255)
        :arg n_diff_params: number of params to randomly vary
        """
        assert seed_id < self.preset_data.shape[0]
        data = list(self.preset_data.loc[seed_id])
        n_total_params = self.preset_data.shape[1]
        params_to_change = random.sample(range(n_total_params), n_diff_params)
        for param_id in params_to_change:
            data[param_id] = self.distributions[param_id]()
        return data
