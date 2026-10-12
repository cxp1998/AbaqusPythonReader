# Contributing Guide / 贡献指南

[English](#english) | [简体中文](#chinese)

---

<a id="english"></a>
## English

### Development Environment

```bash
git clone https://github.com/cxp1998/AbaqusPythonReader.git
cd AbaqusPythonReader
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Running & Testing

```bash
python run.py
python -m unittest discover tests
```

CI runs the above `unittest` command; you can also run `pytest` directly.

### Packaging

```bash
pyinstaller AbaqusPythonReader.spec
```

The output executable is located at `dist/AbaqusPythonReader.exe`. Pushing a `v*` tag triggers GitHub Actions to automatically build and attach the release executable.

### Architecture

| Module | Purpose |
| --- | --- |
| `file_monitor.py` | Polls target file and emits appended content chunks |
| `cleaner.py` | Statement tokenizer; strips viewport operations |
| `app.py` | Main HUD window, menus, themes, resizing |
| `editor.py` / `highlighter.py` | Code editor, line numbers, and Python syntax highlighter |
| `abaqus_mode.py` | Geometry recording modes & `abaqus_v6.env` hook manager |
| `i18n.py` | Internationalization (English default & Chinese support) |
| `icons.py` | Inline Lucide vector SVG icons |
| `config.py` | User configuration manager (`config.json`) |

### Submitting Pull Requests

1. Create a feature branch from `main` (e.g., `fix/mask-parser` or `feat/new-setting`).
2. Follow PEP 8 guidelines. Default UI text, code comments, and docstrings should be in English. Add user-facing localized strings to `i18n.py`.
3. When modifying filtering, configuration, or file monitoring logic, add corresponding unit tests under `tests/`.
4. Running the app locally updates `abaqus_python_reader/config.json`. Avoid committing incidental local configuration changes.
5. Provide a clear description of changes and test results in the PR.

---

<a id="chinese"></a>
## 简体中文

### 开发环境

```bash
git clone https://github.com/cxp1998/AbaqusPythonReader.git
cd AbaqusPythonReader
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 运行与测试

```bash
python run.py
python -m unittest discover tests
```

CI 使用上面的 `unittest` 命令；也可以直接运行 `pytest`。

### 打包

```bash
pyinstaller AbaqusPythonReader.spec
```

输出为 `dist/AbaqusPythonReader.exe`。推送 `v*` 标签后，GitHub Actions 会自动打包并发布到 Releases。

### 代码结构

| 模块 | 职责 |
| --- | --- |
| `file_monitor.py` | 轮询文件，读取新增内容 |
| `cleaner.py` | 按语句拆分代码，过滤视图操作 |
| `app.py` | 主窗口、菜单、主题与悬浮控制 |
| `editor.py` / `highlighter.py` | 编辑器、行号、语法高亮 |
| `abaqus_mode.py` | 录制模式与 `abaqus_v6.env` 配置管理 |
| `i18n.py` | 国际化模块（英文默认，支持简体中文） |
| `icons.py` | 内嵌 Lucide 矢量 SVG 图标 |
| `config.py` | 用户配置读写（`config.json`） |

### 提交 PR

1. 从 `main` 创建分支，如 `fix/mask-parser`。
2. 遵循 PEP 8。代码注释、文档及默认文字以英文为主，用户可见文本需在 `i18n.py` 中补充中英双语。
3. 修改过滤、配置或文件监控逻辑时，在 `tests/` 中补充单元测试。
4. 运行程序会改写 `abaqus_python_reader/config.json`，提交前不要带上附带的本地修改。
5. 在 PR 中说明改动内容和测试情况。
