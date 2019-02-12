from system import Composer
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()


def main():
    composer = Composer()
    composer.collect_plugins()
    composer.activate_plugins()

    composer.pm.hook.config_update(conf={"env": dotenv_values()})
    print(composer.pm.hook.get_store().state)


if __name__ == "__main__":
    main()
