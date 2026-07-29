# SharpSplat

图形化的 [SHARP](https://github.com/apple/ml-sharp) 3D Gaussian Splatting 生成与浏览工具。

SHARP（Shape Reconstruction via Learned Pixel-wise Signed Distance Functions）是 Apple 提出的 3DGS 方法，通过学习像素级有符号距离函数（SDF）从单张或多张图片重建 3D 场景。SharpSplat 在此基础上提供了一个 Gradio Web 界面，让你无需手动操作命令行即可完成图像上传、SHARP 处理、PLY 文件管理与 3D 预览。

## 功能

- **上传图像** — 拖拽上传单张或多张图片，一键触发 SHARP 推理
- **可视化进度** — 实时查看每个任务的完成状态（done / failed / timeout）
- **3D 预览** — 内嵌基于 Three.js 的 3D 查看器，支持旋转、缩放、平移
- **结果管理** — 自动保存 PLY 点云文件至 `outputs/` 目录，可重复查看

## 环境要求

- uv
- Python >= 3.13

## 安装

```bash
git clone https://github.com/mejiro-rin/SharpSplat.git
cd SharpSplat
uv sync
```

若你的电脑支持cuda，并希望使用cuda加速的pytorch运行程序，请在上述 `uv sync` 运行结束后执行以下命令替换默认的cpu版pytorch与相关组件

```bash
uv pip install torch torchvision torchaudio --reinstall --index-url https://download.pytorch.org/whl/cu130
```

`ml-sharp` 已经在 `pyproject.toml` 中通过 `[tool.uv.sources]` 声明为 Git 依赖，`uv sync` 会自动从 [apple/ml-sharp](https://github.com/apple/ml-sharp) 拉取并安装。

## 使用

使用准备好的启动脚本。于终端执行

```bash
# Windows
start.bat

# macOS
start.sh
```

启动后浏览器打开 `http://localhost:7860` 或 `http://127.0.0.1:7860`。

1. **Process 标签** — 上传图片，点击 Start，等待推理完成后查看每张图片的处理状态
2. **3D Viewer 标签** — 从下拉列表选择已完成的 PLY，点击 View in 3D 在浏览器中查看点云。**刚生成完的文件可能需要刷新页面后才会显示在列表中。**

## 项目结构

```text
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

## 日志

- **v0.1.1** 首个发布版本为试用版，ply渲染器有坐标冲突问题，跨越坐标轴正负区域时同时操作鼠标和键盘会发生视角跳转，正在研究解决方案。
- **v0.1.2** 已经解决大部分问题，短期内想不到更多改进点了。希望有人喜欢这个一时兴起制作的小工具。

## 参考

- [apple/ml-sharp](https://github.com/apple/ml-sharp) — Sharp Monocular View Synthesis in Less Than a Second
<!-- - [SHARP 论文](https://machinelearning.apple.com/research/sharp) — Apple Machine Learning Research -->
- [sparkjsdev/spark](https://github.com/sparkjsdev/spark) — ✨ An advanced 3D Gaussian Splatting renderer for THREE.js

## 许可

本项目仅作学习与研究用途。底层 SHARP 模型版权归 Apple 所有，请遵守 [ml-sharp](https://github.com/apple/ml-sharp) 仓库的许可条款。
