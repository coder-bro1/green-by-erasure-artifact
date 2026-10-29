"""Run a Python script at below-normal CPU priority (Windows), so reviewer checks cannot slow GPU runs whose
test executions have a 5 s limit. Usage: python review/low_priority.py <script.py> [args...]"""
import ctypes
import os
import runpy
import sys

if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    if not kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), 0x4000):
        raise OSError('SetPriorityClass failed')
script, sys.argv = sys.argv[1], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
runpy.run_path(script, run_name='__main__')
