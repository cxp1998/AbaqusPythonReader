import os
import time
import tempfile
import unittest
from abaqus_python_reader.abaqus_detector import (
    find_latest_rpy_in_directory,
    detect_active_abaqus_workspace,
    get_process_cwd,
    get_running_abaqus_processes,
)


class TestAbaqusDetector(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_latest_rpy_in_empty_directory(self):
        result = find_latest_rpy_in_directory(self.temp_dir.name)
        self.assertIsNone(result)

    def test_find_latest_rpy_nonexistent_directory(self):
        result = find_latest_rpy_in_directory("Z:\\NonExistent_Dir_12345")
        self.assertIsNone(result)

    def test_find_latest_rpy_picks_newest_mtime(self):
        dir_path = self.temp_dir.name

        # Create older abaqus.rpy
        old_rpy = os.path.join(dir_path, "abaqus.rpy")
        with open(old_rpy, "w") as f:
            f.write("# old session\n")
        # Backdate mtime
        os.utime(old_rpy, (time.time() - 100, time.time() - 100))

        # Create newer abaqus.rpy.1
        new_rpy = os.path.join(dir_path, "abaqus.rpy.1")
        with open(new_rpy, "w") as f:
            f.write("# new session\n")
        os.utime(new_rpy, (time.time() - 10, time.time() - 10))

        result = find_latest_rpy_in_directory(dir_path)
        self.assertIsNotNone(result)
        self.assertEqual(os.path.abspath(result["rpy_path"]), os.path.abspath(new_rpy))
        self.assertEqual(os.path.abspath(result["work_dir"]), os.path.abspath(dir_path))
        self.assertGreater(result["mtime"], 0)

    def test_detect_active_abaqus_workspace_with_candidate(self):
        dir_path = self.temp_dir.name
        test_rpy = os.path.join(dir_path, "abaqus.rpy")
        with open(test_rpy, "w") as f:
            f.write("# active session\n")

        detected = detect_active_abaqus_workspace(extra_candidates=[dir_path])
        self.assertIsNotNone(detected)
        self.assertIn("rpy_path", detected)
        self.assertIn("work_dir", detected)

    def test_get_process_cwd_safe_on_invalid_pid(self):
        # Invalid PID should return None gracefully without raising
        result = get_process_cwd(99999999)
        self.assertIsNone(result)

    def test_get_running_abaqus_processes_returns_list(self):
        procs = get_running_abaqus_processes()
        self.assertIsInstance(procs, list)


if __name__ == "__main__":
    unittest.main()
