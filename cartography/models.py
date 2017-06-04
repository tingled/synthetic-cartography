import datetime

from peewee import (
    Model, CharField, IntegerField, ForeignKeyField,
    FloatField, DateTimeField, SqliteDatabase
)


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(None)  # defer until runtime

    @staticmethod
    def init_db(database, **connection_kwargs):
        BaseModel._meta.database.init(database, **connection_kwargs)


# classes to store a set of midi parameters and values used to generate a sound
class MidiParamClass(BaseModel):
    # i.e. mfccs, chroma
    name = CharField


class MidiParamType(BaseModel):
    name = CharField()
    channel = IntegerField()
    max_val = IntegerField(default=127)  # some controller params have different ranges, [0-max_val]
    param_class = ForeignKeyField(MidiParamClass, default=None)


class Experiment(BaseModel):
    datetime = DateTimeField(default=datetime.datetime.now)
    description = CharField(default=None)


class ExperimentParam(BaseModel):
    """ a mapping of the MidiParams that are enabled for a given
    experiment
    """
    experiment = ForeignKeyField(Experiment)
    midi_param_type = ForeignKeyField(MidiParamType)

    # when randomly selecting midi values, what is the smallest
    # interval of values are we interested in 8 means (0, 7, 15, ...)
    sample_interval = IntegerField()


class MidiSetting(BaseModel):
    pass


class MidiParamSetting(BaseModel):
    midi_setting = ForeignKeyField(MidiSetting)
    midi_param_type = ForeignKeyField(MidiParamType)
    value = IntegerField()


class AudioFeature(BaseModel):
    name = CharField()


# classes to store the resulting audio features of a given sound
class AudioFeatureType(BaseModel):
    name = CharField()
    # sample_rate = FloatField()


class AudioFeatureResult(BaseModel):
    datetime = DateTimeField(default=datetime.datetime.now)


class AudioFeatureResultValue(BaseModel):
    audio_feature_result = ForeignKeyField(AudioFeatureResult)
    audio_feature_type = ForeignKeyField(AudioFeatureType)
    value = FloatField()
