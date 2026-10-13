import unittest
from PySide6.QtWidgets import QApplication
from abaqus_python_reader.abaqus_milestones import (
    parse_milestones,
    partition_code_by_stages,
    inject_milestone_chapters,
    STAGE_CONFIG,
    STAGE_SKETCH,
    STAGE_PART,
    STAGE_PROPERTY,
    STAGE_ASSEMBLY,
    STAGE_STEP,
    STAGE_LOAD_BC,
    STAGE_MESH,
    STAGE_JOB,
)
from abaqus_python_reader.editor import CodeEditor

# Ensure QApplication exists for Qt testing
app = QApplication.instance() or QApplication([])


SAMPLE_ABAQUS_SCRIPT = """# Abaqus/CAE recorded script
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
s.rectangle(point1=(0.0, 0.0), point2=(10.0, 20.0))
p = mdb.models['Model-1'].Part(name='Beam', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=50.0)
mat = mdb.models['Model-1'].Material(name='Steel')
mat.Elastic(table=((210000.0, 0.3), ))
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(dependent=ON, name='Beam-1', part=p)
a.Instance(dependent=ON, name='Beam-2', part=p)
a.Instance(dependent=ON, name='Beam-3', part=p)
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
mdb.models['Model-1'].DisplacementBC(createStepName='Step-1', name='BC-1')
p.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=2.0)
p.generateMesh()
mdb.Job(model='Model-1', name='Job-Beam')
"""


class TestMilestones(unittest.TestCase):
    def test_stage_parsing(self):
        milestones = parse_milestones(SAMPLE_ABAQUS_SCRIPT, is_dark=True)
        self.assertGreaterEqual(len(milestones), 7)

        # Check detected stages
        stages = [m.stage for m in milestones]
        self.assertIn(STAGE_SKETCH, stages)
        self.assertIn(STAGE_PART, stages)
        self.assertIn(STAGE_PROPERTY, stages)
        self.assertIn(STAGE_ASSEMBLY, stages)
        self.assertIn(STAGE_STEP, stages)
        self.assertIn(STAGE_LOAD_BC, stages)
        self.assertIn(STAGE_MESH, stages)
        self.assertIn(STAGE_JOB, stages)

    def test_partition_code_by_stages_zh(self):
        result = partition_code_by_stages(SAMPLE_ABAQUS_SCRIPT, lang="zh")
        # Check dividers
        self.assertIn("# ==============================================================================", result)
        self.assertIn("【功能分区】草图绘制 (Sketch)", result)
        self.assertIn("【功能分区】零件建模 (Part: Beam)", result)
        self.assertIn("【功能分区】材料与截面属性 (Property)", result)
        self.assertIn("【功能分区】模型装配 (Assembly)", result)
        self.assertIn("【功能分区】分析步设置 (Step: Step-1)", result)
        self.assertIn("【功能分区】载荷与边界条件 (Load / BC)", result)
        self.assertIn("【功能分区】网格划分 (Mesh)", result)
        self.assertIn("【功能分区】分析作业与求解 (Job: Job-Beam)", result)

        # CRITICAL TEST: 3 consecutive Assembly instances must stay in ONE block!
        # "【功能分区】模型装配 (Assembly)" must appear EXACTLY ONCE!
        assembly_banner_count = result.count("【功能分区】模型装配 (Assembly)")
        self.assertEqual(assembly_banner_count, 1)

    def test_partition_code_by_stages_en(self):
        result = partition_code_by_stages(SAMPLE_ABAQUS_SCRIPT, lang="en")
        self.assertIn("[Block] Sketch & 2D Profile", result)
        self.assertIn("[Block] Part: Beam", result)
        self.assertIn("[Block] Property & Materials", result)
        self.assertIn("[Block] Assembly & Instances", result)
        self.assertIn("[Block] Step: Step-1", result)
        self.assertIn("[Block] Loads & Boundary Conditions", result)
        self.assertIn("[Block] Mesh Seeding & Generation", result)
        self.assertIn("[Block] Job: Job-Beam", result)

        # Exactly one assembly block
        self.assertEqual(result.count("[Block] Assembly & Instances"), 1)

    def test_partition_code_idempotence(self):
        # Partitioning already-partitioned code should not multiply banners
        once = partition_code_by_stages(SAMPLE_ABAQUS_SCRIPT, lang="zh")
        twice = partition_code_by_stages(once, lang="zh")
        self.assertEqual(once.strip(), twice.strip())

    def test_empty_text_returns_empty_milestones(self):
        milestones = parse_milestones("", is_dark=True)
        self.assertEqual(milestones, [])

        res = partition_code_by_stages("", lang="zh")
        self.assertEqual(res, "")

    def test_editor_renders_partitioned_blocks(self):
        editor = CodeEditor(parent=None, theme_name="dark")
        partitioned = partition_code_by_stages(SAMPLE_ABAQUS_SCRIPT, lang="zh")
        editor.setPlainText(partitioned)

        self.assertIn("【功能分区】零件建模", editor.toPlainText())
        self.assertIn("【功能分区】模型装配", editor.toPlainText())

        editor.close()

    def test_back_and_forth_switching(self):
        code = (
            "p = mdb.models['Model-1'].Part(name='Part-1')\n"
            "p.BaseSolidExtrude(depth=10.0)\n"
            "a = mdb.models['Model-1'].rootAssembly\n"
            "p = mdb.models['Model-1'].parts['Part-1']\n"
            "a.Instance(name='Part-1-1', part=p)\n"
            "p = mdb.models['Model-1'].parts['Part-1']\n"
            "p.PartitionCellByPlanePointNormal()\n"
            "a = mdb.models['Model-1'].rootAssembly\n"
            "a.regenerate()\n"
        )
        result = partition_code_by_stages(code, lang="zh")
        # Should have:
        # 1. Part-1 creation block
        # 2. Assembly block (instances)
        # 3. Part-1 modification block (partition)
        # 4. Assembly block (regenerate)
        part_banners = result.count("【功能分区】零件建模 (Part: Part-1)")
        assembly_banners = result.count("【功能分区】模型装配 (Assembly)")
        self.assertEqual(part_banners, 2)
        self.assertEqual(assembly_banners, 2)


if __name__ == "__main__":
    unittest.main()
