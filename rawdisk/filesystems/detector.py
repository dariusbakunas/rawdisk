class FilesystemDetector(object):
    def __init__(self):
        # 2 dimensional array of fs_id : [list of plugins]
        self.mbr_plugins = {}
        # 2 dimensional array of fs_guid : [list of plugins]
        self.gpt_plugins = {}
    
    def add_mbr_plugin(self, fs_id, plugin):
        if fs_id in self.mbr_plugins:
            self.mbr_plugins.get(fs_id).append(plugin)
        else:
            self.mbr_plugins[fs_id] = [plugin,]

    def add_gpt_plugin(self, fs_guid, plugin):
        if fs_guid in self.gpt_plugins:
            self.gpt_plugins.get(fs_guid).append(plugin)
        else:
            self.gpt_plugins[fs_guid] = [plugin,]

    def detect_mbr(self, filename, offset, fs_id):
        if not fs_id in self.mbr_plugins:
            return None
        else:
            plugins = self.mbr_plugins.get(fs_id)
            for plugin in plugins:
                if plugin.detect(filename, offset):
                    return plugin.get_volume_object()
        return None

    def detect_gpt(self, filename, offset, fs_guid):
        if not fs_guid in self.gpt_plugins:
            return None
        else:
            plugins = self.gpt_plugins.get(fs_guid)
            for plugin in plugins:
                if plugin.detect(filename, offset):
                    return plugin.get_volume_object()

        return None

class FilesystemDetectorSingleton(object):
    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton can't be created twice !")

    @classmethod
    def get(self):
        if self.__instance is None:
            self.__instance = FilesystemDetector()
        
        return self.__instance