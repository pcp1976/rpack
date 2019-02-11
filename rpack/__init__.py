from api.plugin_manager import pm
from pyredux import create_typed_action_creator
from pyrsistent import pmap
from pyredux.utils import compose
from dotenv import load_dotenv
import dotenv

load_dotenv()

reducer = pm.hook.get_config_reducer()[0]

store = pm.hook.get_store()[0]
print(store.state)

Boop, creator_func = create_typed_action_creator("Boop")
boop = compose(store.dispatch, creator_func)


@reducer.register(Boop)
def _(action, state):
    def str2bool(_v):
        if _v.lower() in ("yes", "y", "true", "t", "1"):
            return True
        elif _v.lower() in ("no", "n", "false", "f", "0"):
            return False
        else:
            return _v

    new_state = pmap(
        state.update({key: str2bool(value) for key, value in dotenv.dotenv_values().items()})
    )
    return new_state


boop(True)
for k, v in store.state["config"].items():
    print(f"u can haz {k}") if v else print(f"no haz u {k}")
