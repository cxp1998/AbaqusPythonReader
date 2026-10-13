import unittest
from abaqus_python_reader.i18n import (
    tr, set_language, get_language, get_guide_html, DEFAULT_LANGUAGE
)
from abaqus_python_reader.abaqus_mode import (
    get_mode_info, MODE_COORDINATE, MODE_INDEX, MODE_COMPRESSED
)


class TestI18n(unittest.TestCase):
    def setUp(self):
        set_language(DEFAULT_LANGUAGE)

    def tearDown(self):
        set_language(DEFAULT_LANGUAGE)

    def test_default_language_is_en(self):
        self.assertEqual(DEFAULT_LANGUAGE, "en")
        self.assertEqual(get_language(), "en")
        self.assertEqual(tr("btn_filter"), "Filter")

    def test_switch_language_to_zh(self):
        set_language("zh")
        self.assertEqual(get_language(), "zh")
        self.assertEqual(tr("btn_filter"), "过滤")
        self.assertEqual(tr("btn_copy"), "复制")

        set_language("en")
        self.assertEqual(get_language(), "en")
        self.assertEqual(tr("btn_filter"), "Filter")
        self.assertEqual(tr("btn_copy"), "Copy")

    def test_tr_with_formatting(self):
        set_language("en")
        msg = tr("toast_saved", filename="test.py")
        self.assertEqual(msg, "Saved test.py")

        set_language("zh")
        msg_zh = tr("toast_saved", filename="test.py")
        self.assertEqual(msg_zh, "已保存 test.py")

    def test_tr_fallback(self):
        # Non-existent key should fall back to the key string
        result = tr("non_existent_key_12345")
        self.assertEqual(result, "non_existent_key_12345")

    def test_mode_info_localization(self):
        info_en = get_mode_info(MODE_COORDINATE, lang="en")
        self.assertEqual(info_en["badge"], "Coordinate")
        self.assertEqual(info_en["tag"], "Recommended")

        info_zh = get_mode_info(MODE_COORDINATE, lang="zh")
        self.assertEqual(info_zh["badge"], "坐标")
        self.assertEqual(info_zh["tag"], "推荐")

    def test_new_feature_translations(self):
        set_language("en")
        self.assertEqual(tr("menu_find"), "Find")
        self.assertEqual(tr("search_placeholder"), "Find in editor...")
        self.assertEqual(tr("search_no_results"), "No results")
        self.assertIn("Export Standalone Script", tr("menu_export_standalone"))
        self.assertEqual(tr("toast_font_size", size=12), "Font size: 12pt")

        set_language("zh")
        self.assertEqual(tr("menu_find"), "查找")
        self.assertEqual(tr("search_placeholder"), "在编辑器中查找...")
        self.assertEqual(tr("search_no_results"), "无匹配结果")
        self.assertIn("导出为独立运行脚本", tr("menu_export_standalone"))
        self.assertEqual(tr("toast_font_size", size=12), "字体大小：12pt")


if __name__ == "__main__":
    unittest.main()

