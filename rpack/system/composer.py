from yapsy.PluginManager import PluginManager
import os
import pluggy


class Composer:
    def __init__(self):
        self.plugin_places = [os.path.join(os.getcwd(), "plugins")]
        self.simple_plugin_manager = PluginManager()
        self.pm = pluggy.PluginManager("rpack")
        self.plugin_info_list = None

    def collect_plugins(self):
        self.simple_plugin_manager.setPluginPlaces(self.plugin_places)
        self.simple_plugin_manager.collectPlugins()
        self.plugin_info_list = self.simple_plugin_manager.getAllPlugins()

    def activate_plugins(self):
        for pluginInfo in self.plugin_info_list:
            plugin = pluginInfo.plugin_object
            plugin.pm = self.pm
            try:
                self.pm.add_hookspecs(plugin)
            except ValueError as e:
                print(e)
            self.pm.register(plugin)

        # TODO improve this naive implementation
        for pluginInfo in self.plugin_info_list:
            if pluginInfo.name == "rpack_store":
                plugin = pluginInfo.plugin_object
                plugin.activate()

        for pluginInfo in self.plugin_info_list:
            if pluginInfo.name != "rpack_store":
                plugin = pluginInfo.plugin_object
                plugin.activate()

    def deactivate_plugins(self):
        for pluginInfo in self.plugin_info_list:
            plugin = pluginInfo.plugin_object
            plugin.deactivate()
