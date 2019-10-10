from data_delivery_flow.items import DataDeliveryFlowItem, DataDeliveryFlowLoader
from data_delivery_flow.utils.spiders import BaseSpider


class KorrespondentNetSpider(BaseSpider):
    name = 'start-request:korrespondent.net'
    allowed_domains = ['korrespondent.net']

    def parse(self, response):
        l = DataDeliveryFlowLoader(item=DataDeliveryFlowItem(), response=response)
        l.add_xpath('title', '//h1[@class="post-item__title"]/text()')
        l.add_value('source_data', 'korrespondent.net')
        l.add_xpath('image_url', '//div[@class="post-item__photo clearfix"]/img/@src')
        l.add_xpath('content', '//div[@class="post-item__text"]//text()')
        return l.load_item()
