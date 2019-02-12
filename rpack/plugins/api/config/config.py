from pluggy import HookspecMarker
from yapsy.IPlugin import IPlugin

spec = HookspecMarker("rpack")


class ConfigSpec(IPlugin):
    @spec(firstresult=True)
    def config_update(self, conf: dict):
        """
        Call to update config. Ensure the dict passed in looks like {"config_section": {k: v, k: v}}
        ie you must supply a key which will act as a subkey to the "config" key.
        :param conf:
        :return:
        """
        pass
