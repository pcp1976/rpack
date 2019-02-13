from pluggy import PluginManager, HookimplMarker
from yapsy.IPlugin import IPlugin
from pyredux import middleware
import os

impl = HookimplMarker("rpack")


@middleware
def dirs(store, next_middleware, action):
    if action.type == "ConfigDirectoryUpdated":
        for directory in action.payload:
            try:
                os.makedirs(directory)
            except FileExistsError:
                pass  # don't care
    return next_middleware(action)


class Directory(IPlugin):
    pm: PluginManager = None

    @staticmethod
    @impl
    def get_middleware():
        return dirs
