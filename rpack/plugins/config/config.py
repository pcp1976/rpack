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
from pyredux import create_typed_action_creator, default_reducer
from pyredux.store import Store
from pyrsistent import pmap, plist
from pyredux.utils import compose
from yapsy.IPlugin import IPlugin
from functools import singledispatch
import os

impl = HookimplMarker("rpack")


@default_reducer
def config(action, state=pmap({})):
    return state


class Config(IPlugin):
    pm: PluginManager = None

    def __init__(self):
        super().__init__()
        self.reducer = None
        self.store: Store = None
        self._config_update = None
        self.Event = None

    @impl
    def config_update(self, conf: dict):
        self._config_update(conf)
        if "directory_change" in self.store.state["config"].keys():
            self.pm.hook.raise_event(
                type="ConfigDirectoryUpdated",
                payload=self.store.state["config"]["directory_change"],
            )
            self.pm.hook.config_update(conf={})

    @impl
    def get_reducer(self):
        return config

    def activate(self):
        self.store = self.pm.hook.get_store()

        UpdateConfig, creator_func = create_typed_action_creator("UpdateConfig")
        self._config_update = compose(self.store.dispatch, creator_func)

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
                state.update(
                    {key: sorting_hat(value) for key, value in action.payload.items()}
                )
            )
            if old_state != new_state:
                if files:
                    new_state = pmap(new_state.update({"directory_change": files}))
            else:
                new_state = pmap(new_state.remove("directory_change"))
            return new_state
