from pyredux import create_store, apply_middleware, middleware
from pluggy import HookimplMarker
from pyrsistent import pmap
from functools import singledispatch
from pyredux.store import Store
from yapsy.IPlugin import IPlugin
from pluggy import PluginManager

impl = HookimplMarker("rpack")


@singledispatch
def default(action, state=pmap({})):
    return state


class StoreBuilder(IPlugin):
    def __init__(self):
        super().__init__()
        self.pm: PluginManager = None
        self.the_store: Store = None

    def activate(self):
        @middleware
        def middleware_decorated(store: Store, next_middleware, action):
            self.pm.hook.middleware_hook(store=store, action=action)
            return next_middleware(action)

        self.the_store = create_store(
            default, enhancer=apply_middleware(middleware_decorated)
        )

    @impl
    def get_reducer(self):
        return default

    @impl
    def get_store(self):
        return self.the_store

    @impl
    def middleware_hook(self, store, action):
        print(action.type)
