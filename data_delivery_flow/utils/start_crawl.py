import asyncio
import logging
from concurrent.futures import Executor
from typing import Optional

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

logger = logging.getLogger("start_crawl")


async def start_parse_process(executor: Executor,
                              spider_name: str) -> Optional[asyncio.Future.result, str]:
    """ Handle crawl process in a separate process.

    :param executor: ProcessPoolExecutor
    :param spider_name: spider name
    :return: result or string
    """
    logger.info('start_parse_process started')
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor,
                                   start_crawl,
                                   spider_name)
    except Exception as e:
        print(e.with_traceback(e.__traceback__))


def start_crawl(spider_name: str) -> None:
    """ Start crawl process.

    :param spider_name: spider name
    :return: None
    """
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(spider_name)

    logger.info('start_crawl started')
    process.start(stop_after_crawl=True)
