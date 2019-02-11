from pyredux import create_store, combine_reducer
from pluggy import HookimplMarker
from pyrsistent import pmap
from pluggy import HookspecMarker, PluginManager
from functools import singledispatch

spec = HookspecMarker("rpack")
impl = HookimplMarker("rpack")


class StoreSpec:
    @spec
    def get_default_reducer(self):
        pass

    @spec
    def get_config_reducer(self):
        pass

    @spec
    def get_store(self):
        pass


@singledispatch
def default(action, state=pmap({})):
    return state


@singledispatch
def config(action, state=pmap({})):
    return state


class StoreImpl:
    the_store = create_store(combine_reducer([default, config]))

    @impl
    def get_default_reducer(self):
        return default

    @impl
    def get_config_reducer(self):
        return config

    @impl
    def get_store(self):
        return self.the_store
