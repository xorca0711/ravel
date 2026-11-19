"""Read process peak resident memory without optional dependencies."""
import sys


def peak_memory_bytes():
    if sys.platform == 'win32':
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [('cb', wintypes.DWORD), ('faults', wintypes.DWORD)]+[
                (n, ctypes.c_size_t) for n in ['peak_working', 'working', 'peak_paged', 'paged',
                                               'peak_nonpaged', 'nonpaged', 'pagefile', 'peak_pagefile']]
        counters = Counters(); counters.cb = ctypes.sizeof(counters)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        get = ctypes.WinDLL('psapi', use_last_error=True).GetProcessMemoryInfo
        get.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        get.restype = wintypes.BOOL
        if not get(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        result = counters.peak_working
    else:
        import resource
        result = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    if result > 2*1024**3: raise RuntimeError('Observed process peak exceeded declared 2 GiB bound')
    return result
