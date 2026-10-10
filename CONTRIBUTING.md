# 贡献指南 (Contributing Guide)

欢迎为 **PythonReader** 做出贡献！本项目致力于为 ABAQUS 二次开发工程师提供极致流畅的实时命令流监控与辅助体验。

---

## 🛠️ 本地开发环境搭建

1. **克隆仓库**：
   ```bash
   git clone https://github.com/example/PythonReader.git
   cd PythonReader
   ```

2. **创建并激活 Python 虚拟环境（推荐 Python 3.10+）**：
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # Windows CMD
   .\.venv\Scripts\activate.bat
   ```

3. **安装开发依赖**：
   ```bash
   pip install -r requirements-dev.txt
   ```

---

## 🏃 运行程序

- 通过 Python 模块运行：
  ```bash
  python run.py
  ```
- 或者双击运行根目录下的 `run.bat`。

---

## 🧪 运行测试套件

在提交代码前，请确保所有自动化单元测试均通过：

```bash
# 使用内置 unittest
python -m unittest discover tests

# 或使用 pytest（若已安装）
pytest
```

---

## 📦 打包构建 Windows 可执行程序

本项目使用 PyInstaller 独立打包，已预置规格配置文件 `PythonReader_v2.spec`：

```bash
pyinstaller PythonReader_v2.spec
```

生成的独立单文件 exe 位于 `dist/PythonReader_v2.exe`。

---

## 🔀 提交规范 (PR Workflow)

1. Fork 本项目到个人账号。
2. 基于 `main` 分支创建特性分支（例如 `feature/custom-shortcut` 或 `fix/mask-parser`）。
3. 遵循 PEP 8 编码风格，确保代码注释和文档完整。
4. 编写或补充对应的测试用例（位于 `tests/`）。
5. 提交清晰规范的 Commit 消息。
6. 发起 Pull Request 并详细描述变更内容与测试结果。
