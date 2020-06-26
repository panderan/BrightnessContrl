from ctypes import wintypes, windll, byref
from bclib.configurations import conf_brightness, conf_contrast

class physical_monitor_ctrl(conf_brightness, conf_contrast):
    def __init__(self, handle, description, mccs_ver, vcp):
        self.handle = handle
        self.description = description
        self.mccs_ver = mccs_ver
        self.vcp = vcp


    def show_info(self):
        retstr = ""
        retstr = retstr + "description:%s\n"%self.description
        retstr = retstr + "mccs_ver:%s\n"%self.mccs_ver
        retstr = retstr + "vcp:%s\n"%self.vcp
        return retstr
