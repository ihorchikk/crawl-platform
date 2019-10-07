# -*- coding:utf-8 -*-
import asyncio
from typing import Awaitable

from twisted.internet.defer import Deferred


def as_future(d: Deferred) -> asyncio.Future:
    return d.asFuture(asyncio.get_event_loop())


def as_deferred(f: Awaitable) -> Deferred:
    return Deferred.fromFuture(asyncio.ensure_future(f))
