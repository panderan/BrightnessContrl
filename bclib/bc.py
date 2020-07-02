from ctypes import wintypes, CFUNCTYPE, POINTER, windll, c_int, byref, Structure, c_bool, create_string_buffer
import re

from bclib.physical_monitor_ctrl import physical_monitor_ctrl

all_hmonitors = []
errcode = wintypes.DWORD()
windll.kernel32.GetLastError.restype = wintypes.DWORD


def get_physical_monitors_from_HMONITOR(hmonitor: wintypes.HMONITOR):
    num = wintypes.DWORD()
    windll.Dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, byref(num))

    class PHYSICAL_MONITOER(Structure):
        _fields_ = [
            ("hPhysicalMonitor", wintypes.HANDLE),
            ("szPhysicalMonitorDescription", wintypes.WCHAR*128)
        ]
    phy_monitors_arr = (PHYSICAL_MONITOER * num.value)()
    windll.Dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, num, phy_monitors_arr)
    return list(phy_monitors_arr)

def get_physical_monitor_handles():

    # 获取所有 hmonitor 句柄
    all_hmonitors = []
    @CFUNCTYPE(wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC, POINTER(wintypes.RECT), wintypes.LPARAM)
    def EnumDisplayMonitors_CallBack(hmonitor, hdc, Args3, Args4):
        all_hmonitors.append(hmonitor)
        pass

    windll.user32.EnumDisplayMonitors.restype = wintypes.BOOL
    if not windll.user32.EnumDisplayMonitors(None, None, EnumDisplayMonitors_CallBack, c_int(0)):
        return (True, "Enum Display Monitors Failed. Errcode:%d"%(windll.kernel32.GetLastError()))

    # 获取 hmonitor 中的物理显示器句柄
    physical_monitors = []
    for hmon in all_hmonitors:
        cur_physical_monitors = get_physical_monitors_from_HMONITOR(hmon)
        physical_monitors.extend([i for i in cur_physical_monitors if i.hPhysicalMonitor is not None])

    ret_phymonitors = []
    for phy_mon in physical_monitors:
        # 获取设备信息
        cplen = wintypes.DWORD()
        windll.Dxva2.GetCapabilitiesStringLength.restype = wintypes.BOOL
        if not windll.Dxva2.GetCapabilitiesStringLength(phy_mon.hPhysicalMonitor, byref(cplen)):
            print("Get Caps Len Failed")
            continue
        c_capstr = create_string_buffer(b'\00'*(cplen.value+1))
        windll.Dxva2.CapabilitiesRequestAndCapabilitiesReply.restype = wintypes.BOOL
        if not windll.Dxva2.CapabilitiesRequestAndCapabilitiesReply(phy_mon.hPhysicalMonitor, c_capstr, cplen):
            print("Get Caps Str Failed")
            continue
        capstr = str(c_capstr.value)
        res = re.search('(mccs_ver\()([0-9.]*)(\))', capstr)
        mccs_ver = res[2]
        res = re.search('(vcp\()(([0-9A-F]*(\([0-9A-F ]*\))? ?)*)(\))', capstr)
        vcp = res[2]
        obj = physical_monitor_ctrl(phy_mon.hPhysicalMonitor, phy_mon.szPhysicalMonitorDescription, mccs_ver, vcp)
        ret_phymonitors.append(obj)
    return (False, ret_phymonitors)



