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
        }),
})


def get_config(argv: Any = None) -> Any:
    """

    Parameters
    ----------
    argv

    Returns
    -------

    """
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH,
    )
    options = ap.parse_args(argv)

    return commandline.config_from_options(options, CONFIG_TRAFARET)


def init_config_app(app: web.Application, *, config: Optional[List[str]] = None) -> None:
    """

    Parameters
    ----------
    app
    config

    Returns
    -------

    """
    app['config'] = get_config(config or ['-c', DEFAULT_CONFIG_PATH.as_posix()])


def get_config_default() -> Any:
    """

    Returns
    -------

    """
    return get_config(['-c', DEFAULT_CONFIG_PATH.as_posix()])