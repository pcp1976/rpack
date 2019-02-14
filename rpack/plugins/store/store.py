from pyredux import (
    create_store,
    apply_middleware,
    middleware,
    create_action_type,
    combine_reducer,
)
from pluggy import HookimplMarker
from pyredux.store import Store
from yapsy.IPlugin import IPlugin
from pluggy import PluginManager

impl = HookimplMarker("rpack")


class StoreBuilder(IPlugin):
    def __init__(self):
        super().__init__()
        self.pm: PluginManager = None
        self.the_store: Store = None
        self.Event = create_action_type("Event")

    def activate(self):
        def unpack(*args, newlist=None):
            if newlist is None:
                newlist = []
            for item in args:
                if isinstance(item, list):
                    unpack(*item, newlist=newlist)
                else:
                    newlist.append(item)
            return tuple(newlist)

        middlewares = unpack(self.pm.hook.get_middleware())
        if middlewares:
            self.the_store = create_store(
                combine_reducer(self.pm.hook.get_reducer()),
                enhancer=apply_middleware(*middlewares),
            )
        else:
            self.the_store = create_store(combine_reducer(self.pm.hook.get_reducer()))

        for sub in self.pm.hook.subscribe():
            self.the_store.subscribe(sub)

    @impl
    def get_store(self):
        return self.the_store

    @impl
    def raise_event(self, type, payload):
        self.the_store.dispatch(self.Event(type=type, payload=payload))

    @impl
    def unsubscribe(self, callback):
        """
        :param callback:
        :return:
        """
        self.the_store.unsubscribe(callback)
