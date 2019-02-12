"""
To receive an update when config changes, apply middleware which listens for action.type == CONFIG_UPDATED events.
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
from pyredux import create_typed_action_creator, create_action_type
from pyredux.store import Store
from pyrsistent import pmap
from pyredux.utils import compose
from yapsy.IPlugin import IPlugin

impl = HookimplMarker("rpack")


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
        event = self.Event(type="CONFIG_UPDATED")
        self.store.dispatch(event)
        self.reducer = None

    def activate(self):
        self.reducer = self.pm.hook.get_reducer()
        self.store = self.pm.hook.get_store()

        UpdateConfig, creator_func = create_typed_action_creator("UpdateConfig")
        self._config_update = compose(self.store.dispatch, creator_func)

        self.Event = create_action_type("Event")

        @self.reducer.register(UpdateConfig)
        def _(action, state):
            # TODO refactor this mess!
            def parse_val(_v):
                if isinstance(_v, dict):
                    for k, v in _v.items():
                        _v[k] = parse_val(v)
                    return _v
                elif isinstance(_v, list):
                    new_list = [parse_val(x) for x in _v]
                    return new_list
                else:
                    if _v.lower() in ("yes", "y", "true", "t"):
                        return True
                    elif _v.lower() in ("no", "n", "false", "f"):
                        return False
                    else:
                        try:
                            return int(_v)
                        except:
                            return _v

            new_state = pmap(
                state.update(
                    {
                        "config": {
                            key: parse_val(value)
                            for key, value in action.payload.items()
                        }
                    }
                )
            )
            return new_state
