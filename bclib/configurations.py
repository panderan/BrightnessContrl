#!/usr/bin/env python


from ctypes import *


class conf_brightness:
    def __init__(self):
        self.__brightness_values = (0, 0, 0)

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


class conf_contrast:
    def __init__(self):
        self.__contrast_values = (0, 0, 0)

    @property
    def contrast(self):
        min_contrast = wintypes.DWORD(0)
        cur_contrast = wintypes.DWORD(0)
        max_contrast = wintypes.DWORD(0)
        windll.Dxva2.GetMonitorContrast.restype = wintypes.BOOL
        if not windll.Dxva2.GetMonitorContrast(self.handle, byref(min_contrast), byref(cur_contrast), byref(max_contrast)):
            print("Failed to get contrast info")
        self.__contrast_values = (min_contrast.value, cur_contrast.value, max_contrast.value)
        return self.__contrast_values
    @contrast.setter
    def contrast(self, val):
        if self.__contrast_values[-1] >= val >= self.__contrast_values[0]:
            windll.Dxva2.SetMonitorContrast.restype = wintypes.BOOL
            if not windll.Dxva2.SetMonitorContrast(self.handle, wintypes.DWORD(val)):
                print("Failed to set contrast")
        else:
            print("Brightness value is out of range, must be between [%d, %d]"%(self.__contrast_values[0], self.__contrast_values[-1]))