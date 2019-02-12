from pluggy import HookspecMarker
from pyredux.store import Store
from yapsy.IPlugin import IPlugin

spec = HookspecMarker("rpack")


class StoreSpec(IPlugin):
    @spec(firstresult=True)
    def get_reducer(self):
        """
        Returns @singledispatch function - decorate reducers with @reducer.register(EventType)
        :return: function
        """
        pass

    @spec(firstresult=True)
    def get_store(self):
        """
        The single redux store
        :return: store
        """
        pass

    @spec
    def middleware_hook(self, store: Store, action):
        """
        All middleware hooks are called whenever an event is raised on the store
        :param store:
        :param action:
        :return:
        """
        pass
