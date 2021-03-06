from abc import ABCMeta, abstractmethod
import librosa
import numpy as np


class FeatureExtractor():
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract(self):
        pass


class LibrosaFeatureExtractor(FeatureExtractor):
    DefaultNumMfcc = 13
    DefaultDeltaMfcc = True
    DefaultDelta2Mfcc = True

    def __init__(self, features):
        self.features = features

    def _feature_to_function(self, feature):
        mapping = {
            'mfcc': self._mfcc,
            'chroma': self._chroma
        }
        return mapping[feature]

    def load(self, audio_path, **kwargs):
        return librosa.load(audio_path, **kwargs)

    def extract(self, audio_path, **kwargs):
        y, sr = self.load(audio_path, **kwargs.get('load_kwargs', {}))

    def _mfcc(self, y, sr, **kwargs):
        print(kwargs)
        S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
        log_S = librosa.amplitude_to_db(S, ref=np.max)
        mfcc = librosa.feature.mfcc(
            S=log_S, n_mfcc=kwargs.get('num_mfccs', self.DefaultNumMfcc))
        output = mfcc.copy()

        if kwargs.get('delta_mfccs', self.DefaultDeltaMfcc):
            output = np.concatenate(
                    (output, librosa.feature.delta(mfcc)), axis=0)
        if kwargs.get('delta2_mfccs', self.DefaultDelta2Mfcc):
            output = np.concatenate(
                    (output, librosa.feature.delta(mfcc, order=2)), axis=0)

        return output

    def _chroma(self):
        pass
