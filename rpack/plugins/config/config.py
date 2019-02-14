"""
Config appears as a dict in the store, under the config key:

    {"config":
        {
            "sectionA": {k: v, k: v, [...]},
            "sectionB": {k: v, k: v, [...]},
        }
    }

Updates to config can be made via the hook:

    pm.hook.config_update(conf=dotenv_values())
"""


from pluggy import PluginManager, HookimplMarker
from pyredux import default_reducer, create_action_type
from pyredux.store import Store
from pyrsistent import pmap, plist
from yapsy.IPlugin import IPlugin
from functools import singledispatch
import os

impl = HookimplMarker("rpack")


@default_reducer
def config(action, state=pmap({})):
    return state


UpdateConfig = create_action_type("UpdateConfig")


@config.register(UpdateConfig)
def _(action, state):
    files = []

    @singledispatch
    def sorting_hat(value: str):
        if value.find(":cwd:") > -1:
            val = value.replace(":cwd:", f"{os.getcwd()}{os.path.sep}")
            files.append(val)
            return val.replace("/", os.path.sep)
        elif value.lower() in ("yes", "y", "true", "t"):
            return True
        elif value.lower() in ("no", "n", "false", "f"):
            return False
        else:
            try:
                return int(value)
            except:
                return value

    @sorting_hat.register(dict)
    def _(value: dict):
        return pmap({k: sorting_hat(v) for k, v in value.items()})

    @sorting_hat.register(list)
    def _(value: list):
        return plist([sorting_hat(x) for x in value])

    old_state = state
    new_state = pmap(
        state.update({key: sorting_hat(value) for key, value in action.payload.items()})
    )
    if old_state != new_state and files:
        new_state = pmap(new_state.update({"directory_change": files}))
    else:
        try:
            new_state = pmap(new_state.remove("directory_change"))
        except KeyError:
            pass
    return new_state


class Config(IPlugin):
    pm: PluginManager = None

    @impl
    def config_update(self, conf: dict):
        event = UpdateConfig(payload=conf)
        self.pm.hook.get_store().dispatch(event)
        if "directory_change" in self.pm.hook.get_store().state["config"].keys():
            self.pm.hook.raise_event(
                type="ConfigDirectoryUpdated",
                payload=self.pm.hook.get_store().state["config"]["directory_change"],
            )
            self.pm.hook.config_update(conf={})

    @staticmethod
    @impl
    def get_reducer():
        return config
