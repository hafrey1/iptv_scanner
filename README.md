# iptv_scanner

https://github.com/mzky/checklist   
https://github.com/ssili126/tv

## 🚀 快速开始

### 方法一：直接运行 Python 脚本

1. **安装依赖**

```bash
pip install aiohttp requests eventlet
```

1. **修改配置文件** `config.json`
    - 调整扫描参数
    - 添加或修改 URL 列表
2. **运行程序**

```bash
python iptv_[scanner.py](http://scanner.py)
```

### 方法二：打包成 .exe 可执行文件

1. **安装打包工具**

```bash
pip install pyinstaller
```

1. **执行打包**

```bash
# 方法 A：使用打包脚本
build.bat

# 方法 B：手动打包命令
pyinstaller --onefile --name="IPTV_Scanner" iptv_[scanner.py](http://scanner.py)
```

1. **部署使用**
    - 将生成的 `dist/IPTV_Scanner.exe` 复制到目标目录
    - 将 `config.json` 放在同一目录下
    - 双击运行 `IPTV_Scanner.exe`

## ⚙️ 配置说明

### scan_settings（扫描设置）

| 参数 | 说明 | 默认值 | 建议范围 |
| --- | --- | --- | --- |
| **timeout** | 请求超时时间（秒） | 1.5 | 1.0 - 3.0 |
| **max_concurrent** | 最大并发数 | 500 | 100 - 1000 |
| **test_timeout** | 测速超时时间（秒） | 8 | 5 - 15 |
| **download_segments** | 下载的 TS 片段数 | 3 | 1 - 5 |
| **worker_threads** | 工作线程数 | 10 | 5 - 20 |

### output_settings（输出设置）

- **results_per_channel**：每个频道保留的最佳线路数（建议 1-3）
- **speed_file**：速度测试结果文件名
- **txt_file**：TXT 格式播放列表文件名
- **m3u_file**：M3U 格式播放列表文件名

### name_replacements（名称替换规则）

用于标准化频道名称，可以根据需要添加或修改替换规则。

## 📤 输出文件

运行完成后会生成以下文件：

1. **speed_results.txt**：包含所有频道的测速结果（频道名,URL,速度）
2. **itvlist.txt**：TXT 格式播放列表，按分类组织
3. **itvlist.m3u**：M3U 格式播放列表，兼容各种播放器

## 💡 使用技巧

- **网络环境**：建议在网络稳定的环境下运行
- **扫描时间**：完整扫描可能需要 30 分钟到 2 小时
- **中断恢复**：可以随时按 `Ctrl+C` 中止程序
- **结果筛选**：调整 `results_per_channel` 控制每个频道保留的线路数
- **性能优化**：
    - 增加 `max_concurrent` 可提高扫描速度（但可能增加网络压力）
    - 减少 `download_segments` 可加快测速（但准确性会降低）

## 🔧 故障排除

### 常见问题

**Q: 提示找不到配置文件？**

A: 确保 `config.json` 与程序在同一目录下。

**Q: 扫描不到任何频道？**

A: 检查网络连接，或尝试更新 `scan_urls` 列表。

**Q: 打包后的 .exe 无法运行？**

A: 确保 Windows 系统已安装必要的运行库，或使用 `--hidden-import` 参数重新打包。

**Q: 如何添加更多扫描地址？**

A: 编辑 `config.json`，在 `scan_urls` 数组中添加新的 URL。

## 📝 项目结构

```
iptv_scanner/
├── iptv_[scanner.py](http://scanner.py)    # 主程序
├── config.json        # 配置文件
├── build.bat          # 打包脚本（Windows）
├── speed_results.txt  # 输出：测速结果
├── itvlist.txt        # 输出：TXT 播放列表
└── itvlist.m3u        # 输出：M3U 播放列表
```

## 🎯 改进点

相比原版代码的改进：

✅ **配置分离**：所有参数通过 JSON 文件管理，无需修改代码

✅ **错误处理**：增强的异常处理和用户提示

✅ **可打包性**：优化代码结构，支持打包成独立 .exe

✅ **可维护性**：清晰的代码注释和模块化设计

✅ **用户友好**：详细的进度显示和完成提示

---

*最后更新：2025-10-18*
