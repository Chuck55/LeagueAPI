from marshmallow import fields, post_load, pre_load, validate, Schema


class LeagueAccountSchema(Schema):
    username = fields.Str(required=True)
    tagLine = fields.Str(required=True)


class LeagueAccountPUUID(Schema):
    puuid = fields.Str(required=True)
