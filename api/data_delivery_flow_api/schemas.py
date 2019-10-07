from marshmallow import Schema, fields


class SpiderSchema(Schema):
    name = fields.Str(required=True, allow_none=False)


class StartUrlSchema(SpiderSchema):
    start_urls = fields.List(fields.URL, required=True)


# class SettingSchema(Schema):
#     spider_name = fields.Str(required=True)
#     name = fields.Str(required=True, allow_none=False)
#     value = fields.Raw(required=True, allow_none=True)
#
#
# class DeleteSettingSchema(Schema):
#     spider_name = fields.Str(required=True)
#     name = fields.Str(required=True, allow_none=False)
#
#
# class AdvertiseSchema(Schema):
#     objects = fields.Nested(SpiderSchema, required=True, allow_none=False, many=True)
#
#
# class CrawlerSchema(Schema):
#     crawler_name = fields.Str(required=True, allow_none=False)
#
#
# class CollectionStatusSchema(Schema):
#     client_id = fields.Str(required=True, allow_none=False)
#     spider = fields.Str(required=True, allow_none=False)
#     scan_time = fields.DateTime(required=True, allow_none=False)
#     check_point_time = fields.DateTime(required=True, allow_none=False)
#
#
# class LimitSchema(Schema):
#     limit = fields.Int(
#         validate=lambda value: value > 0,
#         error_messages={"validator_failed": "value should be greater than 0"},
#     )
#
#
# class CollectionStatsSchema(LimitSchema):
#     id = fields.Str(required=True, allow_none=False)
