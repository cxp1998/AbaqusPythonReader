"""Abaqus Modeling Milestones & Stage Bookmarking Engine.

Analyzes recorded Python statements and identifies key FEA modeling lifecycle milestones:
- Part & Sketch geometry definition
- Material properties & Section assignments
- Assembly instances & orientations
- Analysis Steps & Output requests
- Interactions, Contacts & Ties
- Loads & Boundary Conditions (BCs)
- Mesh seeding & generation
- Job creation & execution
- Visualization & ODB post-processing
"""

import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

# Stage definitions
STAGE_SKETCH = "SKETCH"
STAGE_PART = "PART"
STAGE_PROPERTY = "PROPERTY"
STAGE_ASSEMBLY = "ASSEMBLY"
STAGE_STEP = "STEP"
STAGE_INTERACTION = "INTERACTION"
STAGE_LOAD_BC = "LOAD_BC"
STAGE_MESH = "MESH"
STAGE_JOB = "JOB"
STAGE_ODB = "ODB"


@dataclass
class Milestone:
    stage: str
    name: str
    label: str
    line_number: int  # 1-indexed
    statement_idx: int
    color: str
    snippet: str


STAGE_CONFIG = {
    STAGE_SKETCH: {
        "color_dark": "#818cf8",   # Indigo
        "color_light": "#4f46e5",
        "badge_zh": "草图",
        "badge_en": "Sketch",
    },
    STAGE_PART: {
        "color_dark": "#38bdf8",   # Sky
        "color_light": "#0284c7",
        "badge_zh": "零件",
        "badge_en": "Part",
    },
    STAGE_PROPERTY: {
        "color_dark": "#f472b6",   # Pink
        "color_light": "#db2777",
        "badge_zh": "属性",
        "badge_en": "Property",
    },
    STAGE_ASSEMBLY: {
        "color_dark": "#c084fc",   # Purple
        "color_light": "#9333ea",
        "badge_zh": "装配",
        "badge_en": "Assembly",
    },
    STAGE_STEP: {
        "color_dark": "#fb923c",   # Orange
        "color_light": "#ea580c",
        "badge_zh": "分析步",
        "badge_en": "Step",
    },
    STAGE_INTERACTION: {
        "color_dark": "#facc15",   # Yellow
        "color_light": "#ca8a04",
        "badge_zh": "接触",
        "badge_en": "Interaction",
    },
    STAGE_LOAD_BC: {
        "color_dark": "#f87171",   # Rose
        "color_light": "#dc2626",
        "badge_zh": "载荷约束",
        "badge_en": "Load/BC",
    },
    STAGE_MESH: {
        "color_dark": "#34d399",   # Emerald
        "color_light": "#059669",
        "badge_zh": "网格",
        "badge_en": "Mesh",
    },
    STAGE_JOB: {
        "color_dark": "#22d3ee",   # Cyan
        "color_light": "#0891b2",
        "badge_zh": "作业",
        "badge_en": "Job",
    },
    STAGE_ODB: {
        "color_dark": "#94a3b8",   # Slate
        "color_light": "#64748b",
        "badge_zh": "后处理",
        "badge_en": "Results",
    },
}

# Compiled regex patterns for detecting Abaqus API milestone statements
PATTERNS = [
    # 1. Sketch
    (
        STAGE_SKETCH,
        re.compile(r"""\bConstrainedSketch\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: m.group("name") or m.group("name2") or "Sketch",
    ),
    # 2. Part
    (
        STAGE_PART,
        re.compile(r"""\bPart\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: m.group("name") or m.group("name2") or "Part",
    ),
    # 3. Material
    (
        STAGE_PROPERTY,
        re.compile(r"""\bMaterial\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"Mat: {m.group('name') or m.group('name2') or 'Material'}",
    ),
    # 4. Section
    (
        STAGE_PROPERTY,
        re.compile(r"""\b(?P<type>\w*Section)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"Sec: {m.group('name') or m.group('name2') or 'Section'}",
    ),
    # 5. Section Assignment
    (
        STAGE_PROPERTY,
        re.compile(r"""\bSectionAssignment\s*\(""", re.DOTALL),
        lambda m: "SectionAssign",
    ),
    # 5.5 Assembly rootAssembly
    (
        STAGE_ASSEMBLY,
        re.compile(r"""\b(?:rootAssembly|DatumCsysByDefault)\b""", re.DOTALL),
        lambda m: "Assembly",
    ),
    # 6. Assembly Instance
    (
        STAGE_ASSEMBLY,
        re.compile(r"""\bInstance\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"Inst: {m.group('name') or m.group('name2') or 'Instance'}",
    ),
    # 7. Analysis Steps
    (
        STAGE_STEP,
        re.compile(r"""\b(?P<type>(?:Static|Dynamic|Frequency|Buckle|HeatTransfer|CoupledTempDisplacement)\w*Step)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"Step: {m.group('name') or m.group('name2') or 'Step'}",
    ),
    # 8. Interactions & Ties
    (
        STAGE_INTERACTION,
        re.compile(r"""\b(?P<type>Tie|ContactProperty|SurfaceToSurfaceContact\w*|Coupling)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"{m.group('type')}: {m.group('name') or m.group('name2') or 'Int'}",
    ),
    # 9. Boundary Conditions
    (
        STAGE_LOAD_BC,
        re.compile(r"""\b(?P<type>\w*BC)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"BC: {m.group('name') or m.group('name2') or 'BC'}",
    ),
    # 10. Loads
    (
        STAGE_LOAD_BC,
        re.compile(r"""\b(?P<type>ConcentratedForce|Pressure|SurfaceTraction|Moment|BodyForce)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"Load: {m.group('name') or m.group('name2') or 'Load'}",
    ),
    # 11. Mesh
    (
        STAGE_MESH,
        re.compile(r"""\b(?P<act>generateMesh|seedPart|seedEdge|setElementType)\s*\(""", re.DOTALL),
        lambda m: "Mesh",
    ),
    # 12. Job creation & submission
    (
        STAGE_JOB,
        re.compile(r"""\bJob\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", re.DOTALL),
        lambda m: f"Job: {m.group('name') or m.group('name2') or 'Job'}",
    ),
    (
        STAGE_JOB,
        re.compile(r"""\bjobs\[['"](?P<name>[^'"]+)['"]\]\.submit\s*\(""", re.DOTALL),
        lambda m: f"Submit: {m.group('name')}",
    ),
    # 13. Visualization & ODB
    (
        STAGE_ODB,
        re.compile(r"""\b(?:session\.openOdb|displayedObject\s*=\s*odb)""", re.DOTALL),
        lambda m: "ODB Results",
    ),
]


def parse_milestones(text: str, is_dark: bool = True) -> List[Milestone]:
    """
    Parses Abaqus Python script text and returns discovered modeling milestones
    ordered chronologically by line number.
    """
    if not text or not text.strip():
        return []

    lines = text.splitlines()
    milestones: List[Milestone] = []

    # Track line positions of statements
    current_line = 1
    last_milestone_tag = None
    last_milestone_name = None

    for idx, line in enumerate(lines):
        line_num = idx + 1
        clean_line = line.strip()

        # Ignore comments or blanks
        if not clean_line or clean_line.startswith("#"):
            continue

        matched_stage = None
        matched_name = None

        for stage, pattern, name_extractor in PATTERNS:
            m = pattern.search(line)
            if m:
                matched_stage = stage
                matched_name = name_extractor(m)
                break

        if matched_stage and matched_name:
            # Avoid duplicate consecutive milestones
            if matched_stage == last_milestone_tag and matched_name == last_milestone_name:
                continue

            cfg = STAGE_CONFIG.get(matched_stage, {})
            color = cfg.get("color_dark" if is_dark else "color_light", "#38bdf8")
            badge = cfg.get("badge_en", matched_stage)
            label = f"{badge}: {matched_name}" if not matched_name.startswith(f"{badge}:") else matched_name

            milestones.append(
                Milestone(
                    stage=matched_stage,
                    name=matched_name,
                    label=label,
                    line_number=line_num,
                    statement_idx=len(milestones),
                    color=color,
                    snippet=clean_line[:80],
                )
            )
            last_milestone_tag = matched_stage
            last_milestone_name = matched_name

    return milestones


def get_stage_banner(stage: str, name: Optional[str] = None, lang: str = "zh") -> str:
    """Generates an aesthetic section block banner for the given stage."""
    clean_name = name
    if clean_name and ":" in clean_name:
        clean_name = clean_name.split(":", 1)[1].strip()

    zh_titles = {
        STAGE_SKETCH: "草图绘制 (Sketch)",
        STAGE_PART: f"零件建模 (Part: {clean_name})" if clean_name and clean_name != "Part" else "零件建模 (Part)",
        STAGE_PROPERTY: "材料与截面属性 (Property)",
        STAGE_ASSEMBLY: "模型装配 (Assembly)",
        STAGE_STEP: f"分析步设置 (Step: {clean_name})" if clean_name and clean_name != "Step" else "分析步设置 (Step)",
        STAGE_INTERACTION: "相互作用与约束 (Interaction / Contact)",
        STAGE_LOAD_BC: "载荷与边界条件 (Load / BC)",
        STAGE_MESH: "网格划分 (Mesh)",
        STAGE_JOB: f"分析作业与求解 (Job: {clean_name})" if clean_name and clean_name != "Job" else "分析作业与求解 (Job)",
        STAGE_ODB: "后处理与可视化 (Results / ODB)",
    }
    en_titles = {
        STAGE_SKETCH: "Sketch & 2D Profile",
        STAGE_PART: f"Part: {clean_name}" if clean_name and clean_name != "Part" else "Part Modeling",
        STAGE_PROPERTY: "Property & Materials",
        STAGE_ASSEMBLY: "Assembly & Instances",
        STAGE_STEP: f"Step: {clean_name}" if clean_name and clean_name != "Step" else "Analysis Step",
        STAGE_INTERACTION: "Interactions & Constraints",
        STAGE_LOAD_BC: "Loads & Boundary Conditions",
        STAGE_MESH: "Mesh Seeding & Generation",
        STAGE_JOB: f"Job: {clean_name}" if clean_name and clean_name != "Job" else "Job & Submission",
        STAGE_ODB: "Visualization & ODB Results",
    }

    divider = "# " + "=" * 78
    title_text = zh_titles.get(stage, stage) if lang == "zh" else en_titles.get(stage, stage)
    prefix = "【功能分区】" if lang == "zh" else "[Block] "
    return f"{divider}\n# {prefix}{title_text}\n{divider}"


def classify_statement_stage(stmt: str, next_stmts: tuple = ()) -> tuple[Optional[str], Optional[str]]:
    """
    Classifies a statement into its FEA modeling stage and extracts any target name.
    Uses next_stmts lookahead (e.g. to avoid treating `p = parts['...']` as a Part switch
    when it is immediately followed by `a.Instance(..., part=p)` in Assembly).
    """
    clean_stmt = stmt.strip()
    if not clean_stmt or clean_stmt.startswith("#"):
        return None, None

    # 1. Sketch
    m = re.search(r"""\bConstrainedSketch\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_SKETCH, m.group("name") or m.group("name2") or "Sketch"

    # 2. Part creation: Part(name=...)
    m = re.search(r"""\bPart\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_PART, m.group("name") or m.group("name2") or "Part"

    # 3. Property & Materials (checked before generic part operations, since SectionAssignment is called on p)
    m = re.search(r"""\bMaterial\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_PROPERTY, m.group("name") or m.group("name2") or "Material"

    if re.search(r"""\b(?:SectionAssignment|Elastic|Plastic|Expansion|Density|\w*Section)\s*\(""", stmt, re.DOTALL):
        return STAGE_PROPERTY, None

    # 4. Mesh (checked before generic part operations, since seedPart/generateMesh are called on p or a)
    if re.search(r"""\b(?:generateMesh|seedPart|seedEdge|setElementType|setMeshControls)\s*\(""", stmt, re.DOTALL):
        return STAGE_MESH, None

    # 5. Step
    m = re.search(r"""\b(?P<type>(?:Static|Dynamic|Frequency|Buckle|HeatTransfer|CoupledTempDisplacement)\w*Step)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_STEP, m.group("name") or m.group("name2") or "Step"

    # 6. Interaction
    m = re.search(r"""\b(?P<type>Tie|ContactProperty|SurfaceToSurfaceContact\w*|Coupling)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_INTERACTION, m.group("name") or m.group("name2") or "Interaction"

    # 7. Load / BC
    m = re.search(r"""\b(?P<type>\w*BC)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_LOAD_BC, m.group("name") or m.group("name2") or "BC"

    m = re.search(r"""\b(?P<type>ConcentratedForce|Pressure|SurfaceTraction|Moment|BodyForce|Gravity)\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_LOAD_BC, m.group("name") or m.group("name2") or "Load"

    # 8. Job
    m = re.search(r"""\bJob\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m:
        return STAGE_JOB, m.group("name") or m.group("name2") or "Job"

    if re.search(r"""\bjobs\[['"](?P<name>[^'"]+)['"]\]\.submit\s*\(""", stmt, re.DOTALL):
        return STAGE_JOB, None

    # 9. Visualization / ODB
    if re.search(r"""\b(?:session\.openOdb|displayedObject\s*=\s*odb)""", stmt, re.DOTALL):
        return STAGE_ODB, None

    # 10. Assembly operations (a.Instance, a.regenerate, rootAssembly, etc.)
    m_inst = re.search(r"""\bInstance\s*\(\s*(?:.*?name\s*=\s*['"](?P<name>[^'"]+)['"]|['"](?P<name2>[^'"]+)['"])""", stmt, re.DOTALL)
    if m_inst:
        return STAGE_ASSEMBLY, m_inst.group("name") or m_inst.group("name2") or "Instance"

    if re.search(r"""\b(?:rootAssembly|DatumCsysByDefault)\b""", stmt, re.DOTALL):
        return STAGE_ASSEMBLY, None

    if re.search(r"""\ba\.(?:regenerate|translate|rotate|Set|Surface|ReferencePoint|features)\s*\(""", stmt, re.DOTALL):
        return STAGE_ASSEMBLY, None

    if re.search(r"""\bdisplayedObject\s*=\s*a\b|\bassemblyDisplay\.setValues\b""", stmt, re.DOTALL):
        return STAGE_ASSEMBLY, None

    # 11. Part selection / modification:
    m_parts = re.search(r"""(?:parts\[['"](?P<name>[^'"]+)['"]\])""", stmt, re.DOTALL)
    if m_parts:
        part_name = m_parts.group("name")
        # Lookahead: is this immediately followed by a.Instance or an assembly operation?
        is_assembly_helper = False
        for n_stmt in next_stmts[:3]:
            n_clean = n_stmt.strip()
            if not n_clean or n_clean.startswith("#"):
                continue
            if re.search(r"""\ba\.(?:Instance|translate|rotate|regenerate|DatumCsys)\b""", n_clean):
                is_assembly_helper = True
                break
            if re.search(r"""\bp\.(?:Partition\w*|Cut\w*|Base\w*|Solid\w*|Shell\w*|Datum\w*|Round|Chamfer|AttachmentPoints|ReferencePoint|repair\w*|features|cells|edges|faces|vertices)\b""", n_clean):
                is_assembly_helper = False
                break
        if not is_assembly_helper:
            return STAGE_PART, part_name
        else:
            return STAGE_ASSEMBLY, None

    # Operations directly on p: p.Partition..., p.Cut..., p.Datum..., p.Round..., p.cells, etc.
    if re.search(r"""\bp\.(?:Partition\w*|Cut\w*|Base\w*|Solid\w*|Shell\w*|Datum\w*|Round|Chamfer|AttachmentPoints|ReferencePoint|repair\w*|features|cells|edges|faces|vertices)\b""", stmt, re.DOTALL):
        return STAGE_PART, None

    if re.search(r"""\bdisplayedObject\s*=\s*p\b|\bpartDisplay\.setValues\b""", stmt, re.DOTALL):
        return STAGE_PART, None

    return None, None


def partition_code_by_stages(script_text: str, lang: str = "zh") -> str:
    """
    Partitions Python code stream into clear, distinct functional blocks in-line.
    Inserts a bold section banner ONLY when transitioning to a different functional module.
    Consecutive operations in the same stage (e.g. 50 assembly instances) stay in the same block.
    Supports switching back and forth (e.g. Part -> Assembly -> Part -> Assembly).
    """
    if not script_text or not script_text.strip():
        return script_text

    # Strip existing auto-injected banners
    filtered_lines = []
    for line in script_text.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("# ==============================================================================") or \
           trimmed.startswith("# 【功能分区】") or \
           trimmed.startswith("# [Block]") or \
           trimmed.startswith("# [Stage:"):
            continue
        filtered_lines.append(line)

    clean_text = "\n".join(filtered_lines)
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)

    from .cleaner import split_python_statements
    statements = split_python_statements(clean_text)
    if not statements:
        return script_text

    out_parts = []
    current_stage: Optional[str] = None
    current_part_name: Optional[str] = None

    for idx, stmt in enumerate(statements):
        clean_stmt = stmt.strip()
        if not clean_stmt or clean_stmt.startswith("#"):
            out_parts.append(stmt)
            continue

        next_window = tuple(statements[idx+1:idx+4])
        matched_stage, matched_name = classify_statement_stage(stmt, next_window)

        is_stage_switch = False
        if matched_stage is not None:
            if current_stage is None:
                is_stage_switch = True
            elif matched_stage != current_stage:
                is_stage_switch = True
            elif matched_stage == STAGE_PART and matched_name and current_part_name and matched_name != current_part_name:
                is_stage_switch = True

        if is_stage_switch:
            current_stage = matched_stage
            if matched_stage == STAGE_PART and matched_name:
                current_part_name = matched_name
            banner_name = matched_name or (current_part_name if matched_stage == STAGE_PART else None)
            banner = get_stage_banner(matched_stage, banner_name, lang=lang)
            if out_parts and not out_parts[-1].endswith("\n\n"):
                out_parts.append("\n" + banner + "\n")
            else:
                out_parts.append(banner + "\n")

        out_parts.append(stmt)

    result = "".join(out_parts)
    return re.sub(r'\n{3,}', '\n\n', result)


def inject_milestone_chapters(script_text: str, lang: str = "zh") -> str:
    """Backwards-compatible wrapper calling partition_code_by_stages."""
    return partition_code_by_stages(script_text, lang=lang)
