import unittest
from abaqus_python_reader.cleaner import (
    clean_abaqus_script,
    has_mask_statement,
    is_viewport_statement,
    split_python_statements,
)


class TestAbaqusCleaner(unittest.TestCase):
    def test_split_python_statements(self):
        code = "a = 1\nb = 2\nc = (3 +\n     4)\n"
        stmts = split_python_statements(code)
        self.assertEqual(len(stmts), 3)
        self.assertEqual(stmts[0].strip(), "a = 1")
        self.assertEqual(stmts[1].strip(), "b = 2")
        self.assertIn("3 +", stmts[2])

    def test_is_viewport_statement(self):
        vp_pan = "session.viewports['Viewport: 1'].view.pan(asPercentage=(0.05, -0.02))\n"
        vp_rot = "session.viewports['Viewport: 1'].view.rotate(xAngle=15.0, yAngle=-30.0, zAngle=0.0)\n"
        vp_zoom = "session.viewports['Viewport: 1'].view.zoom(zoomFactor=1.2)\n"
        vp_fit = "session.viewports['Viewport: 1'].view.fitView()\n"
        model_stmt = "p = mdb.models['Model-1'].Part(name='Beam_Part')\n"
        comment = "# session.viewports['Viewport: 1'].view.pan(0, 0)\n"

        self.assertTrue(is_viewport_statement(vp_pan))
        self.assertTrue(is_viewport_statement(vp_rot))
        self.assertTrue(is_viewport_statement(vp_zoom))
        self.assertTrue(is_viewport_statement(vp_fit))
        self.assertFalse(is_viewport_statement(model_stmt))
        self.assertFalse(is_viewport_statement(comment))

    def test_clean_abaqus_script_filter_on(self):
        script = (
            "p = mdb.models['Model-1'].Part(name='Beam_Part')\n"
            "session.viewports['Viewport: 1'].view.rotate(xAngle=15.0)\n"
            "mdb.models['Model-1'].Material(name='Steel')\n"
        )
        cleaned = clean_abaqus_script(script, filter_viewport=True)
        self.assertIn("Beam_Part", cleaned)
        self.assertIn("Steel", cleaned)
        self.assertNotIn("rotate", cleaned)

    def test_clean_abaqus_script_filter_off(self):
        script = (
            "p = mdb.models['Model-1'].Part(name='Beam_Part')\n"
            "session.viewports['Viewport: 1'].view.rotate(xAngle=15.0)\n"
        )
        cleaned = clean_abaqus_script(script, filter_viewport=False)
        self.assertEqual(cleaned, script)

    def test_has_mask_statement(self):
        mask_code = "cells = c.getSequenceFromMask(mask=('[#1 ]', ), )"
        coord_code = "cells = c.findAt(((10.0, 5.0, 0.0), ))"

        self.assertTrue(has_mask_statement(mask_code))
        self.assertFalse(has_mask_statement(coord_code))

    def test_format_standalone_script(self):
        from abaqus_python_reader.cleaner import format_standalone_script
        raw = (
            "session.viewports['Viewport: 1'].view.rotate(xAngle=15.0)\n"
            "p = mdb.models['Model-1'].Part(name='Beam', dimensionality=THREE_D, type=DEFORMABLE_BODY)\n"
        )
        res = format_standalone_script(raw)
        self.assertTrue(res.startswith("# -*- coding: mbcs -*-"))
        self.assertIn("from abaqus import *", res)
        self.assertIn("from abaqusConstants import *", res)
        self.assertIn("from caeModules import *", res)
        self.assertIn("from driverUtils import executeOnCaeStartup", res)
        self.assertIn("executeOnCaeStartup()", res)
        self.assertIn("Beam", res)
        self.assertNotIn("rotate", res)

    def test_format_standalone_script_preserves_existing(self):
        from abaqus_python_reader.cleaner import format_standalone_script
        already_complete = (
            "# -*- coding: utf-8 -*-\n"
            "from abaqus import *\n"
            "from abaqusConstants import *\n"
            "from caeModules import *\n"
            "from driverUtils import executeOnCaeStartup\n"
            "executeOnCaeStartup()\n"
            "print('Hello Abaqus')\n"
        )
        res = format_standalone_script(already_complete)
        self.assertEqual(res.count("from abaqus import *"), 1)
        self.assertEqual(res.count("executeOnCaeStartup()"), 1)
        self.assertEqual(res.count("# -*- coding:"), 1)
        self.assertIn("utf-8", res)
        self.assertIn("Hello Abaqus", res)


if __name__ == "__main__":
    unittest.main()

