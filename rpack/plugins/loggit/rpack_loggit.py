from pluggy import PluginManager, HookimplMarker
from pyredux import middleware
from loguru import logger
from yapsy.IPlugin import IPlugin
import sys

logger.remove()
impl = HookimplMarker("rpack")


@middleware
def logger_ctrl(store, next_middleware, action):
    if action.type == "LoggerCtrl" and str.lower(action.payload) == "start":
        logger.remove()
        logger.add(
            sys.stderr,
            level=store.state["config"]["dotenv"]["LOGGING_LEVEL"],
            format="".join(
                [
                    "<c>{time}</c> ",
                    "<level>|{level: <9}|</level> ",
                    "<light-blue>{extra[action]: <20}:</light-blue> ",
                    "<white>{message}</white>",
                ]
            ),
        )

    return next_middleware(action)


@middleware
def loggit(store, next_middleware, action):
    logger_ctx = logger.bind(action=action.type)
    logger_ctx.debug(action.payload)
    return next_middleware(action)


class Logging(IPlugin):
    @staticmethod
    @impl
    def get_middleware():
        return [loggit, logger_ctrl]
