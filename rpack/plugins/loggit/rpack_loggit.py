from pluggy import PluginManager, HookimplMarker
from pyredux import middleware
from loguru import logger
from yapsy.IPlugin import IPlugin

impl = HookimplMarker("rpack")


@middleware
def loggit(store, next_middleware, action):
    logger.log("DEBUG", f"{action.type} {action.payload}")
    return next_middleware(action)


class Logging(IPlugin):
    @staticmethod
    @impl
    def get_middleware():
        return loggit
