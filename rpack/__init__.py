from system import Composer
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()


def main():
    composer = Composer()
    composer.collect_plugins()
    composer.activate_plugins()

    # quick test funcs
    composer.pm.hook.config_update(conf={"dotenv": dotenv_values()})
    composer.pm.hook.raise_event(type="LoggerCtrl", payload="start")
    composer.pm.hook.config_update(conf={"ini": {"geoff": "bill"}})


if __name__ == "__main__":
    main()
