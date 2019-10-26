from marshmallow import Schema, fields


class SpiderSchema(Schema):
    name = fields.Str(required=True, allow_none=False)


class StartUrlSchema(SpiderSchema):
    start_urls = fields.List(fields.URL, required=True)
