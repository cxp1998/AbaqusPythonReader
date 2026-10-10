# 贡献指南

## 开发环境

```bash
git clone https://github.com/example/AbaqusPythonReader.git
cd AbaqusPythonReader
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

## 运行与测试

```bash
python run.py
python -m unittest discover tests
```

CI 使用上面的 unittest 命令；也可以直接运行 `pytest`。

## 打包

```bash
pyinstaller AbaqusPythonReader.spec
```

输出为 `dist/AbaqusPythonReader.exe`。推送 `v*` 标签后，GitHub Actions 会自动打包并发布到 Releases。

## 代码结构

| 模块 | 职责 |
| --- | --- |
| `file_monitor.py` | 轮询文件，读取新增内容 |
| `cleaner.py` | 按语句拆分代码，过滤视图操作 |
| `app.py` | 主窗口、菜单、主题 |
| `editor.py` / `highlighter.py` | 编辑器、行号、语法高亮 |
| `abaqus_mode.py` | 录制模式与 `abaqus_v6.env` 配置 |
| `icons.py` | 内嵌 SVG 图标 |
| `config.py` | 用户配置读写 |

## 提交 PR

1. 从 `main` 创建分支，如 `fix/mask-parser`。
2. 遵循 PEP 8。界面文字使用中文，保持简洁。
3. 修改过滤、配置或文件监控逻辑时，在 `tests/` 中补充测试。
4. 运行程序会改写 `abaqus_python_reader/config.json`，提交前不要带上这类改动。
5. 在 PR 中说明改动内容和测试情况。
