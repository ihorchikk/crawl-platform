from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class DataDeliveryFlowItem(Item):
    title = Field(required=True)
    content = Field(required=True)
    source_data = Field(required=True)
    image_url = Field()


class DataDeliveryFlowLoader(ItemLoader):
    default_output_processor = TakeFirst()
    content_in = MapCompose(str.strip)
    content_out = Join()
