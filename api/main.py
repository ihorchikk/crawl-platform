import uvloop
from aiohttp import web

from api.app import init_app


def create_app() -> web.Application:
    """ Creating application.

    :return: web application
    """
    import aiohttp_debugtoolbar

    app = init_app()
    aiohttp_debugtoolbar.setup(app, check_host=False)

    return app


def main() -> None:
    """ Main function in web application. Getting config
    and starting application. For local debug.
    In production use gunicorn.

    :return: None
    """
    app = init_app()
    app_settings = app['config']['app']
    uvloop.install()
    web.run_app(
        app,
        host=app_settings['host'],
        port=app_settings['port'],
    )


if __name__ == '__main__':
    main()
