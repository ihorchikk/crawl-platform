import argparse
import os
import pathlib
from typing import Any, Optional, List

import trafaret
from aiohttp import web
from trafaret_config import commandline

PATH = pathlib.Path(__file__).parent.parent
settings_file = os.environ.get('SETTINGS_FILE', 'dev.yml')
DEFAULT_CONFIG_PATH = PATH / 'config' / settings_file


CONFIG_TRAFARET = trafaret.Dict({
    trafaret.Key('app'):
        trafaret.Dict({
            'host': trafaret.String(),
            'port': trafaret.Int(),
        }),
    trafaret.Key('redis'):
        trafaret.Dict({
            'host': trafaret.String(),
            'port': trafaret.Int(),
            'db': trafaret.Int(),
        }),
    trafaret.Key('rabbitmq'):
        trafaret.Dict({
            'host': trafaret.String(),
            'port': trafaret.Int(),
            'queue': trafaret.String(),
            'exchange_name': trafaret.String(),
            'exchange_type': trafaret.String(),
            'routing_key': trafaret.String(),
        }),
})


def get_config(argv: Any = None) -> Any:
    """ Main function of config. Get default config or custom and
    verification them by trafaret scheme.

    :param argv: Any
    :return: Any
    """
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH,
    )
    options = ap.parse_args(argv)

    return commandline.config_from_options(options, CONFIG_TRAFARET)


def init_config_app(app: web.Application, *, config: Optional[List[str]] = None) -> None:
    """ Save config to application for using in future.

    :param app: web application
    :param config: config
    :return: None
    """
    app['config'] = get_config(config or ['-c', DEFAULT_CONFIG_PATH.as_posix()])


def get_config_default() -> Any:
    """ Get default config.

    :return: Any
    """
    return get_config(['-c', DEFAULT_CONFIG_PATH.as_posix()])
