from peewee import (
    Model, CharField, IntegerField, ForeignKeyField,
    DateTimeField, SqliteDatabase
)

db = SqliteDatabase('carto.db')


# classes to store a set of midi parameters and values used to generate a sound
class MidiParamClass(Model):
    # i.e. mfccs, chroma
    name = CharField


class MidiParamType(Model):
    name = CharField()
    channel = IntegerField()
    feature_class = ForeignKeyField(MidiParamClass, default=None)


class MidiSetting(Model):
    date = DateTimeField()


class MidiParamSetting(Model):
    midi_setting = ForeignKeyField(MidiSetting)
    midi_param_type = ForeignKeyField(MidiParamType)
    value = IntegerField()


class AudioFeature(Model):
    name = CharField()


# classes to store the resulting audio features of a given sound
class AudioFeatureType(Model):
    name = CharField()
    # sample_rate = FloatField()


class AudioFeatureResult(Model):
    date = DateTimeField()


class AudioFeatureResultValue(Model):
    audio_feature_result = ForeignKeyField(AudioFeatureResult)
    audio_feature_type = ForeignKeyField(AudioFeatureType)
    value = IntegerField()
