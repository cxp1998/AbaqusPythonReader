# AbaqusPythonReader

<p align="center">
  <img src="abaqus_python_reader/resources/icon_256.png" width="96" height="96" alt="AbaqusPythonReader" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python" />
  <img src="https://img.shields.io/badge/GUI-PySide6-green.svg" alt="PySide6" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6.svg" alt="Windows" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT" />
</p>

<p align="center">
  <b><a href="#english">English</a> | <a href="#chinese">简体中文</a></b>
</p>

---

<a id="english"></a>
## English

A real-time HUD desktop tool for monitoring the Abaqus/CAE command stream (`abaqus.rpy`), designed for Abaqus Python scripting and parametric modeling.

### Features

- **Syntax Highlighting & Themes**: Real-time Python syntax highlighting with dark and light themes.
- **Noise Filtering**: Automatically hides viewport manipulations (pan, rotate, zoom, fitView, etc.), and strips them when copying or saving code.
- **Auto-Detect Abaqus Workspace**: Automatically probes running Abaqus/CAE processes to detect the active working directory and bind its latest `abaqus.rpy` on the fly.
- **In-line Functional Block Partitioning**: Intelligently segments code flow into clear functional stages (Part, Assembly, Material/Section, Step, Interaction, Load/BC, Mesh, Job) with contextual lookahead support for alternating back-and-forth modeling workflows.
- **Export Standalone Python Scripts**: Automatically wraps the cleaned journal into an executable script with complete standard imports (`caeModules`, `abaqusConstants`) and model saving boilerplate, ready for batch execution via `abaqus cae noGUI=...`.
- **Floating Search & Font Zoom**: Press `Ctrl + F` to invoke a lightweight floating search bar with match counter, and use `Ctrl + MouseWheel` for instant smooth code font zooming.
- **Non-blocking Monitoring**: Shared read-only polling that never locks or conflicts with Abaqus journal writes.
- **HUD Floating Window**: Always-on-top, configurable opacity, frameless window, right-click dragging, and smooth edge resizing.
- **Geometry Recording Modes**: Quick switching between Coordinate (`COORDINATE`), Index (`INDEX`), and Mask (`COMPRESSEDINDEX`) modes, with support for persisting to `~/abaqus_v6.env` as startup default.
- **Abaqus API Tooltips (Hover Docs)**: Hover over any Abaqus function, class, or constant (e.g. `BaseSolidExtrude`, `seedPart`, `StaticStep`, `THREE_D`) to view instant signatures, parameter descriptions, and docstrings.
- **Multilingual Support (i18n)**: English (default) and Simplified Chinese with instant runtime switching.

### Getting Started

Download `AbaqusPythonReader.exe` from [Releases](https://github.com/cxp1998/AbaqusPythonReader/releases) and run directly, or launch from source (Python 3.10+):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

By default, the app automatically detects the running Abaqus working directory or monitors `abaqus.rpy` in the current folder. Click the file badge on the top bar to manually switch target files.

For development, testing, and packaging, see [CONTRIBUTING.md](CONTRIBUTING.md).

### Acknowledgments

- **Dr. Jiao** ([ck436@126.com](mailto:ck436@126.com)): Original ABAQUS-PythonReader (2010), archived under [`legacy/`](legacy/).
- **Hailin Wang** ([abqpy](https://github.com/haiiliin/abqpy)): Source of Abaqus Python API signatures and docstrings used for offline hover documentation.

### License

[MIT](LICENSE)

---

<a id="chinese"></a>
## 简体中文

实时查看 Abaqus/CAE 命令流（`abaqus.rpy`）的桌面 HUD 工具，用于 Abaqus 脚本开发和参数化建模。

### 功能特性

- **语法高亮与主题**：Python 语法高亮，支持深色/浅色专业工程主题。
- **视图噪声过滤**：自动隐藏视图操作（平移、旋转、缩放、fitView 等），复制和导出时自动净化去除。
- **自动探测 Abaqus 工作目录**：自动识别正在运行的 Abaqus/CAE 进程并定位当前活动工作目录，一键极速重定向至最新 `abaqus.rpy`。
- **代码按功能模块行内分区**：智能识别建模阶段（Part 零件、Assembly 装配、Material/Section 截面材料、Step 分析步、Interaction 接触/相互作用、Load/BC 载荷边界、Mesh 网格、Job 作业等），具有上下文前瞻能力，完美支持来回穿插建模场景。
- **导出为可独立运行脚本**：自动补齐标准模块引用（`from caeModules import *` 等）与 `mdb.saveAs` 保存逻辑，导出的 `.py` 可直接通过 `abaqus cae noGUI=script.py` 进行批处理或参数化驱动。
- **悬浮快捷搜索与字号缩放**：支持 `Ctrl + F` 呼出轻量悬浮搜索条（实时定位并高亮匹配项），支持 `Ctrl + 滚轮` 平滑快速缩放代码字号。
- **只读非阻塞监控**：只读共享轮询文件，不冲突且不影响 Abaqus 写入日记。
- **HUD 悬浮窗**：置顶、透明度无级调节、无边框现代设计、鼠标右键拖动、边缘自由缩放。
- **几何录制模式切换**：支持坐标（`COORDINATE`）、索引（`INDEX`）、掩码（`COMPRESSEDINDEX`）模式快速切换，并可写入用户目录下的 `abaqus_v6.env` 设为启动默认。
- **Abaqus API 悬停文档速查**：鼠标悬停在任意 Abaqus 函数、类或符号常量（如 `BaseSolidExtrude`、`seedPart`、`StaticStep`、`THREE_D` 等）上，即刻弹出参数签名与官方用法文档。
- **多语言支持（i18n）**：默认英文，支持中英文实时无缝切换。

### 使用方法

从 [Releases](https://github.com/cxp1998/AbaqusPythonReader/releases) 下载 `AbaqusPythonReader.exe` 直接运行，或从源码启动（Python 3.10+）：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

默认监控当前目录下的 `abaqus.rpy`，点击顶栏的文件名即可更换监控文件。

开发、测试和打包说明请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 致谢

- **焦博士**（[ck436@126.com](mailto:ck436@126.com)）：2010 年原版 ABAQUS-PythonReader 作者，代码归档于 [`legacy/`](legacy/)。
- **Hailin Wang**（[abqpy](https://github.com/haiiliin/abqpy)）：本项目离线 API 悬停文档所使用的 Abaqus Python 签名与接口文档来源。

### 许可证

[MIT](LICENSE)
