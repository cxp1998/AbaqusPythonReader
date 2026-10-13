import unittest
from PySide6.QtWidgets import QApplication
from abaqus_python_reader.editor import CodeEditor

# Ensure QApplication exists for Qt widget testing
app = QApplication.instance() or QApplication([])


class TestEditorFeatures(unittest.TestCase):
    def setUp(self):
        self.editor = CodeEditor(parent=None, theme_name="dark", show_line_numbers=True)

    def tearDown(self):
        self.editor.close()

    def test_font_zoom_and_clamp(self):
        initial_size = self.editor.font().pointSize()
        self.assertEqual(initial_size, 10)

        # Zoom in
        self.editor.zoom_font(1)
        self.assertEqual(self.editor.font().pointSize(), 11)

        # Zoom out
        self.editor.zoom_font(-2)
        self.assertEqual(self.editor.font().pointSize(), 9)

        # Reset zoom
        self.editor.reset_font_zoom()
        self.assertEqual(self.editor.font().pointSize(), 10)

        # Test maximum clamp (24pt)
        self.editor.zoom_font(50)
        self.assertEqual(self.editor.font().pointSize(), 24)

        # Test minimum clamp (7pt)
        self.editor.zoom_font(-50)
        self.assertEqual(self.editor.font().pointSize(), 7)

    def test_search_overlay_matching_and_navigation(self):
        sample_code = (
            "import math\n"
            "p = mdb.models['Model-1'].Part(name='Part-1')\n"
            "p = mdb.models['Model-1'].Part(name='Part-2')\n"
            "mdb.models['Model-1'].Material(name='Steel')\n"
        )
        self.editor.setPlainText(sample_code)

        # Open search overlay
        self.editor.show()
        self.editor.open_search_overlay()
        self.assertFalse(self.editor.search_overlay.isHidden())

        # Set search text: 'Part'
        self.editor.search_overlay.input_field.setText("Part")
        self.editor.perform_search()

        # Should match 'Part', 'Part-1', 'Part', 'Part-2' -> total 4 occurrences of 'Part'
        self.assertEqual(len(self.editor._search_matches), 4)
        self.assertEqual(self.editor._current_match_idx, 0)
        self.assertEqual(self.editor.search_overlay.count_label.text(), "1/4")

        # Test navigation: next match
        self.editor.find_next()
        self.assertEqual(self.editor._current_match_idx, 1)
        self.assertEqual(self.editor.search_overlay.count_label.text(), "2/4")

        # Test navigation: previous match (wraps to last)
        self.editor.find_prev()
        self.assertEqual(self.editor._current_match_idx, 0)
        self.editor.find_prev()
        self.assertEqual(self.editor._current_match_idx, 3)
        self.assertEqual(self.editor.search_overlay.count_label.text(), "4/4")

        # Case sensitivity test: toggle case sensitivity
        self.editor.search_overlay.btn_case.setChecked(True)
        self.editor.search_overlay.input_field.setText("part")  # lowercase 'part'
        self.editor.perform_search()
        self.assertEqual(len(self.editor._search_matches), 0)
        self.assertEqual(self.editor.search_overlay.count_label.text(), "No results")

        # Close search overlay
        self.editor.close_search_overlay()
        self.assertFalse(self.editor.search_overlay.isVisible())
        self.assertEqual(len(self.editor._search_matches), 0)
        self.assertEqual(len(self.editor.extraSelections()), 0)


if __name__ == "__main__":
    unittest.main()
