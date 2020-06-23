from ctypes import wintypes, windll, byref

class physical_monitor_ctrl:
    def __init__(self, handle, description, mccs_ver, vcp):
        self.handle = handle
        self.description = description
        self.mccs_ver = mccs_ver
        self.vcp = vcp

        self.__brightness_values = (0, 0, 0)

    def show_info(self):
        retstr = ""
        retstr = retstr + "description:%s\n"%self.description
        retstr = retstr + "mccs_ver:%s\n"%self.mccs_ver
        retstr = retstr + "vcp:%s\n"%self.vcp
        return retstr

    @property
    def brightness(self):
        min_brightness = wintypes.DWORD(0)
        cur_brightness = wintypes.DWORD(0)
        max_brightness = wintypes.DWORD(0)
        windll.Dxva2.GetMonitorBrightness.restype = wintypes.BOOL
        if not windll.Dxva2.GetMonitorBrightness(self.handle, byref(min_brightness), byref(cur_brightness), byref(max_brightness)):
            print("Failed to get brightness info")
        self.__brightness_values = (min_brightness.value, cur_brightness.value, max_brightness.value)
        return self.__brightness_values
    @brightness.setter
    def brightness(self, val):
        if self.__brightness_values[-1] >= val >= self.__brightness_values[0]:
            windll.Dxva2.SetMonitorBrightness.restype = wintypes.BOOL
            if not windll.Dxva2.SetMonitorBrightness(self.handle, wintypes.DWORD(val)):
                print("Failed to set brightness")
        else:
            print("Brightness value is out of range, must be between [%d, %d]"%(self.__brightness_values[0], self.__brightness_values[-1]))
