"""Abaqus Workspace & Active Recording Auto-Detection Module.

Provides a multi-tier detection pipeline to discover active Abaqus/CAE sessions:
1. Process CWD Inspection: Queries running Abaqus/CAE processes (ABQcae.exe) via Win32 PEB.
2. Window Title Parsing: Extracts project directories from open Abaqus/CAE database titles.
3. Heuristic Directory Scanning: Scans candidate directories (C:\\temp, cwd, user home) for recent abaqus.rpy files.
"""

import os
import sys
import glob
from pathlib import Path
from typing import Optional, List, Dict, Any

# Windows API constants for PEB reading
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010


def get_process_cwd(pid: int) -> Optional[str]:
    """Retrieves the Current Working Directory (CWD) of a Windows process via its PEB."""
    if sys.platform != "win32":
        return None

    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        ntdll = ctypes.windll.ntdll

        # 64-bit PROCESS_BASIC_INFORMATION structure
        class PROCESS_BASIC_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("ExitStatus", ctypes.c_ulonglong),
                ("PebBaseAddress", ctypes.c_void_p),
                ("AffinityMask", ctypes.c_ulonglong),
                ("BasePriority", ctypes.c_ulonglong),
                ("UniqueProcessId", ctypes.c_ulonglong),
                ("InheritedFromUniqueProcessId", ctypes.c_ulonglong),
            ]

        h_proc = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        if not h_proc:
            return None

        try:
            pbi = PROCESS_BASIC_INFORMATION()
            return_length = ctypes.c_ulonglong()
            status = ntdll.NtQueryInformationProcess(
                h_proc, 0, ctypes.byref(pbi), ctypes.sizeof(pbi), ctypes.byref(return_length)
            )
            if status != 0 or not pbi.PebBaseAddress:
                return None

            # In 64-bit Windows PEB, RTL_USER_PROCESS_PARAMETERS pointer is at PebBaseAddress + 0x20
            params_ptr = ctypes.c_void_p()
            read_bytes = ctypes.c_size_t()
            if not kernel32.ReadProcessMemory(
                h_proc,
                ctypes.c_void_p(pbi.PebBaseAddress + 0x20),
                ctypes.byref(params_ptr),
                ctypes.sizeof(params_ptr),
                ctypes.byref(read_bytes),
            ) or not params_ptr.value:
                return None

            # In RTL_USER_PROCESS_PARAMETERS, CurrentDirectory.DosPath (UNICODE_STRING) starts at params_ptr + 0x38
            # UNICODE_STRING: USHORT Length (0x38), USHORT MaxLength (0x3A), PWSTR Buffer (0x40)
            buffer_len = ctypes.c_ushort()
            kernel32.ReadProcessMemory(
                h_proc,
                ctypes.c_void_p(params_ptr.value + 0x38),
                ctypes.byref(buffer_len),
                2,
                ctypes.byref(read_bytes),
            )

            buf_ptr = ctypes.c_void_p()
            kernel32.ReadProcessMemory(
                h_proc,
                ctypes.c_void_p(params_ptr.value + 0x40),
                ctypes.byref(buf_ptr),
                ctypes.sizeof(buf_ptr),
                ctypes.byref(read_bytes),
            )

            if not buf_ptr.value or buffer_len.value == 0:
                return None

            char_count = buffer_len.value // 2
            buf = ctypes.create_unicode_buffer(char_count)
            if kernel32.ReadProcessMemory(
                h_proc, buf_ptr, buf, buffer_len.value, ctypes.byref(read_bytes)
            ):
                return buf.value.rstrip("\\/")
        finally:
            kernel32.CloseHandle(h_proc)
    except Exception:
        return None
    return None


def get_running_abaqus_processes() -> List[Dict[str, Any]]:
    """Enumerates running Abaqus processes and discovers their working directories."""
    if sys.platform != "win32":
        return []

    results = []
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32
        TH32CS_SNAPPROCESS = 0x00000002

        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.c_void_p),
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", ctypes.c_wchar * 260),
            ]

        h_snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if h_snap == -1:
            return []

        pe = PROCESSENTRY32()
        pe.dwSize = ctypes.sizeof(PROCESSENTRY32)

        target_names = {"abqcae.exe", "abqcaek.exe", "abqcaeg.exe", "abaqus.exe"}

        if kernel32.Process32FirstW(h_snap, ctypes.byref(pe)):
            while True:
                exe_name = pe.szExeFile.lower()
                if exe_name in target_names or "abqcae" in exe_name:
                    pid = int(pe.th32ProcessID)
                    cwd = get_process_cwd(pid)
                    results.append({
                        "pid": pid,
                        "name": pe.szExeFile,
                        "cwd": cwd,
                    })
                if not kernel32.Process32NextW(h_snap, ctypes.byref(pe)):
                    break
        kernel32.CloseHandle(h_snap)
    except Exception:
        pass
    return results


def find_latest_rpy_in_directory(dir_path: str) -> Optional[Dict[str, Any]]:
    """Finds the most recently modified abaqus.rpy or abaqus.rpy.* file in dir_path."""
    if not dir_path or not os.path.isdir(dir_path):
        return None

    try:
        patterns = [
            os.path.join(dir_path, "abaqus.rpy"),
            os.path.join(dir_path, "abaqus.rpy.*"),
        ]
        candidates = []
        for p in patterns:
            candidates.extend(glob.glob(p))

        if not candidates:
            return None

        # Filter out non-files and sort by mtime descending
        file_stats = []
        for f in candidates:
            if os.path.isfile(f):
                try:
                    st = os.stat(f)
                    file_stats.append((f, st.st_mtime, st.st_size))
                except OSError:
                    continue

        if not file_stats:
            return None

        file_stats.sort(key=lambda item: item[1], reverse=True)
        newest_file, mtime, size = file_stats[0]

        return {
            "rpy_path": os.path.abspath(newest_file),
            "work_dir": os.path.abspath(dir_path),
            "mtime": mtime,
            "size": size,
        }
    except Exception:
        return None


def detect_abaqus_window_workdir() -> Optional[str]:
    """Extracts project directory from active Abaqus/CAE window titles containing [.cae]."""
    if sys.platform != "win32":
        return None

    try:
        import ctypes
        user32 = ctypes.windll.user32
        found_dir = None

        def enum_cb(hwnd, _):
            nonlocal found_dir
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    title = buff.value
                    if "abaqus" in title.lower() and ".cae" in title.lower():
                        import re
                        m = re.search(r'\[(.*\.cae)\]', title, re.IGNORECASE)
                        if m:
                            cae_path = m.group(1).strip()
                            if os.path.exists(cae_path):
                                found_dir = os.path.dirname(os.path.abspath(cae_path))
                                return False
            return True

        LPARAM = ctypes.c_ssize_t
        HWND = ctypes.c_void_p
        BOOL = ctypes.c_bool
        WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
        user32.EnumWindows.argtypes = [WNDENUMPROC, LPARAM]
        user32.EnumWindows.restype = BOOL
        user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
        return found_dir
    except Exception:
        return None


def detect_active_abaqus_workspace(extra_candidates: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """
    Executes the multi-tier detection pipeline to discover the active Abaqus session.

    Returns a dict with:
        - "rpy_path": str (path to monitored file)
        - "work_dir": str (Abaqus working directory)
        - "source": "process" | "window" | "heuristic"
        - "mtime": float
        - "process_name": Optional[str]
    Or None if no Abaqus recording file is discovered.
    """
    # -------------------------------------------------------------
    # Tier 1: Process CWD Inspection (Most accurate)
    # -------------------------------------------------------------
    procs = get_running_abaqus_processes()
    for proc in procs:
        cwd = proc.get("cwd")
        if cwd and os.path.isdir(cwd):
            info = find_latest_rpy_in_directory(cwd)
            if info:
                info["source"] = "process"
                info["process_name"] = proc.get("name")
                return info
            # If no .rpy in CWD yet, the CWD itself is still valid
            potential_rpy = os.path.join(cwd, "abaqus.rpy")
            return {
                "rpy_path": potential_rpy,
                "work_dir": cwd,
                "source": "process",
                "process_name": proc.get("name"),
                "mtime": 0,
                "size": 0,
            }

    # -------------------------------------------------------------
    # Tier 2: Window Title [.cae] Inspection
    # -------------------------------------------------------------
    win_dir = detect_abaqus_window_workdir()
    if win_dir and os.path.isdir(win_dir):
        info = find_latest_rpy_in_directory(win_dir)
        if info:
            info["source"] = "window"
            return info

    # -------------------------------------------------------------
    # Tier 3: Heuristic Candidate Directories Scan
    # -------------------------------------------------------------
    candidate_dirs = []
    if extra_candidates:
        candidate_dirs.extend([c for c in extra_candidates if c and os.path.isdir(c)])

    # Add common Abaqus directories
    candidate_dirs.append(os.getcwd())
    for common in ["C:\\temp", "C:\\tmp", os.path.expanduser("~")]:
        if os.path.isdir(common) and common not in candidate_dirs:
            candidate_dirs.append(common)

    job_dir = os.environ.get("ABAQUS_JOB_DIR")
    if job_dir and os.path.isdir(job_dir) and job_dir not in candidate_dirs:
        candidate_dirs.append(job_dir)

    temp_dir = os.environ.get("TEMP")
    if temp_dir and os.path.isdir(temp_dir) and temp_dir not in candidate_dirs:
        candidate_dirs.append(temp_dir)

    all_matches = []
    for d in candidate_dirs:
        info = find_latest_rpy_in_directory(d)
        if info:
            info["source"] = "heuristic"
            all_matches.append(info)

    if all_matches:
        # Sort by mtime descending
        all_matches.sort(key=lambda item: item["mtime"], reverse=True)
        return all_matches[0]

    return None
