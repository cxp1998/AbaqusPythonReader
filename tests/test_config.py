import tempfile
import unittest
from pathlib import Path
from abaqus_python_reader.config import ConfigManager, DEFAULT_CONFIG


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "test_config.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_config_loading(self):
        cfg = ConfigManager(filepath=self.config_path)
        self.assertEqual(cfg.get("font_family"), DEFAULT_CONFIG["font_family"])
        self.assertEqual(cfg.get("opacity"), DEFAULT_CONFIG["opacity"])
        self.assertEqual(cfg.get("language"), "en")

    def test_set_and_persist(self):
        cfg = ConfigManager(filepath=self.config_path)
        cfg.set("dark_theme", True)
        cfg.set("language", "zh")
        self.assertTrue(cfg.get("dark_theme"))
        self.assertEqual(cfg.get("language"), "zh")

        # Reload from disk
        cfg2 = ConfigManager(filepath=self.config_path)
        self.assertTrue(cfg2.get("dark_theme"))
        self.assertEqual(cfg2.get("language"), "zh")


if __name__ == "__main__":
    unittest.main()
