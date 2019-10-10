import asyncio
from concurrent.futures import Executor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


async def start_parse_process(executor: Executor,
                              spider_name: str) \
        -> asyncio.Future.result or str:
    """

    Parameters
    ----------
    executor
    spider_name

    Returns
    -------

    """
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(executor,
                                   start_crawl,
                                   spider_name)
    except Exception as e:
        print(e.with_traceback(e.__traceback__))


def start_crawl(spider_name: str) \
        -> None:
    """

    Parameters
    ----------
    spider_name

    Returns
    -------

    """
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(spider_name)
    process.start(stop_after_crawl=True)
