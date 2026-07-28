# SharpSplat

图形化的 [SHARP](https://github.com/apple/ml-sharp) 3D Gaussian Splatting 生成与浏览工具。

SHARP（Shape Reconstruction via Learned Pixel-wise Signed Distance Functions）是 Apple 提出的 3DGS 方法，通过学习像素级有符号距离函数（SDF）从单张或多张图片重建 3D 场景。SharpSplat 在此基础上提供了一个 Gradio Web 界面，让你无需手动操作命令行即可完成图像上传、SHARP 处理、PLY 文件管理与 3D 预览。

## 功能

- **上传图像** — 拖拽上传单张或多张图片，一键触发 SHARP 推理
- **可视化进度** — 实时查看每个任务的完成状态（done / failed / timeout）
- **3D 预览** — 内嵌基于 Three.js 的 3D 查看器，支持旋转、缩放、平移
- **结果管理** — 自动保存 PLY 点云文件至 `outputs/` 目录，可重复查看

## 环境要求

- Python >= 3.13

## 安装

```bash
git clone https://github.com/mejiro-rin/SharpSplat.git
cd SharpSplat
uv venv
uv sync
```

`sharp` 依赖在 `pyproject.toml` 中通过 `[tool.uv.sources]` 声明为 Git 依赖，`uv sync` 会自动从 [apple/ml-sharp](https://github.com/apple/ml-sharp) 拉取并安装。

## 使用

```bash
# 方式一：Windows
start.bat
# macOS
start.sh

# 方式二：直接运行
uv run python src/sharpsplat/app.py

# 可选参数
uv run python src/sharpsplat/app.py --port 7860 --share
```

启动后浏览器打开 `http://localhost:7860`。

1. **Process 标签** — 上传图片，点击 Start，等待推理完成后查看每张图片的处理状态
2. **3D Viewer 标签** — 从下拉列表选择已完成的 PLY，点击 View in 3D 在浏览器中查看点云

## 项目结构

```
SharpSplat/
├── src/sharpsplat/
│   ├── app.py          # 入口，组装所有组件
│   ├── config.py       # 路径与设置
│   ├── predictor.py    # 调用 sharp CLI 执行推理
│   ├── repository.py   # 上传与结果管理
│   ├── ui.py           # Gradio Web 界面
│   └── viewer.py       # 内嵌 3D 查看器 HTTP 服务
├── static/spark/       # Three.js + PLY 查看器前端资源
├── uploads/            # 上传的图片缓存
├── outputs/            # SHARP 生成的 PLY 点云文件
├── pyproject.toml
└── start.bat / start.sh
```

## 参考

- [apple/ml-sharp](https://github.com/apple/ml-sharp) — Sharp Monocular View Synthesis in Less Than a Second
<!-- - [SHARP 论文](https://machinelearning.apple.com/research/sharp) — Apple Machine Learning Research -->
- [sparkjsdev/spark](https://github.com/sparkjsdev/spark) — ✨ An advanced 3D Gaussian Splatting renderer for THREE.js

## 许可

本项目仅作学习与研究用途。底层 SHARP 模型版权归 Apple 所有，请遵守 [ml-sharp](https://github.com/apple/ml-sharp) 仓库的许可条款。
