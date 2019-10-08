import argparse
import asyncio
import logging
from concurrent.futures.process import ProcessPoolExecutor

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

parser = argparse.ArgumentParser()

parser.add_argument(
    '--spider_name',
    dest='spider_name',
    metavar='NAME',
    help='Spider name',
    required=True)


async def start_parse_process(spider_name):
    executor = ProcessPoolExecutor()
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor, start_crawl, spider_name)
    finally:
        executor.shutdown()


def start_crawl(spider_name):
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(spider_name)
    process.start(stop_after_crawl=True)


if __name__ == '__main__':
    args = parser.parse_args()
    start_crawl(args.spider_name)
