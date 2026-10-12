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
- **Non-blocking Monitoring**: Shared read-only polling that never locks or conflicts with Abaqus journal writes.
- **HUD Floating Window**: Always-on-top, configurable opacity, frameless window, right-click dragging, and smooth edge resizing.
- **Geometry Recording Modes**: Quick switching between Coordinate (`COORDINATE`), Index (`INDEX`), and Mask (`COMPRESSEDINDEX`) modes, with support for persisting to `~/abaqus_v6.env` as startup default.
- **Multilingual Support (i18n)**: English (default) and Simplified Chinese with instant runtime switching.

### Getting Started

Download `AbaqusPythonReader.exe` from [Releases](https://github.com/cxp1998/AbaqusPythonReader/releases) and run directly, or launch from source (Python 3.10+):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

By default, the app monitors `abaqus.rpy` in the current working directory. Click the file badge on the top bar to change the target file.

For development, testing, and packaging, see [CONTRIBUTING.md](CONTRIBUTING.md).

### Acknowledgments

Rewritten from the original ABAQUS-PythonReader developed in 2010 by Dr. Jiao ([ck436@126.com](mailto:ck436@126.com)). The legacy application and source code are archived under [`legacy/`](legacy/).

### License

[MIT](LICENSE)

---

<a id="chinese"></a>
## 简体中文

实时查看 Abaqus/CAE 命令流（`abaqus.rpy`）的桌面 HUD 工具，用于 Abaqus 脚本开发和参数化建模。

### 功能特性

- **语法高亮与主题**：Python 语法高亮，支持深色/浅色主题。
- **视图噪声过滤**：自动隐藏视图操作（平移、旋转、缩放、fitView 等），复制和另存为时自动去除。
- **只读非阻塞监控**：只读轮询文件，不影响 Abaqus 写入日记。
- **HUD 悬浮窗**：置顶、透明度调节、无边框设计、鼠标右键拖动、边缘自由缩放。
- **几何录制模式切换**：支持坐标（`COORDINATE`）、索引（`INDEX`）、掩码（`COMPRESSEDINDEX`）模式快速切换，并可写入用户目录下的 `abaqus_v6.env` 设为启动默认。
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

本项目重写自焦博士（[ck436@126.com](mailto:ck436@126.com)）2010 年开发的 ABAQUS-PythonReader。原版程序与源码保存在 [`legacy/`](legacy/)。

### 许可证

[MIT](LICENSE)
