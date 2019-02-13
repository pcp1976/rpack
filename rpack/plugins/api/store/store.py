from pluggy import HookspecMarker
from pyredux.store import Store
from yapsy.IPlugin import IPlugin

spec = HookspecMarker("rpack")


class StoreSpec(IPlugin):
    @spec(firstresult=True)
    def get_store(self):
        """
        The single redux store
        :return: store
        """
        pass

    @spec
    def get_middleware(self):
        """
        :return:  Middleware-decorated function
        """
        pass

    @spec
    def get_reducer(self):
        """
        :return: the default reducer for a store
        """

    @spec
    def raise_event(self, type, payload):
        """
        :param action:
        :param payload:
        :return:
        """
        pass

    @spec
    def subscribe(self):
        """
        :return: callback
        """
        pass

    @spec
    def unsubscribe(self, callback):
        """
        :param callback:
        :return:
        """
        pass
