# 现代汉语词典（第7版）数字制作指南

本指南介绍如何将开源的《现代汉语词典》第7版扫描件制作成标准的 MDict 格式（`.mdx`, `.mdd`）。

## 环境准备

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 制作流程

### 1. 获取制作文件

克隆本项目仓库以获取转换脚本与扫描资源：

```bash
git clone https://github.com/dictkit/xiandai.git
```

### 2. 图像资源准备

【方案一】从 [xiandai](https://github.com/dictkit/xiandai.git) Repo 中复制

[直接下载](https://github.com/binsgit/xiandai7/releases/tag/v20260508)

运行 `cp_img.sh` 脚本，自动从仓库中提取、重命名并归档图片至 `images/` 目录：

```bash
bash cp_img.sh
```

【方案二】从原始 JP2 扫描文件转换成 JPG 和 PNG 图片
需预先安装 `imagemagick` 包，以使用 `convert` 等命令

```bash
bash generate_images.sh 
```

### 3. 同步 TOC 配置

为了对齐非正文部分的页码与图片映射，需覆盖原始 `toc.json`：

```bash
cp toc.json xiandai/docs/data/
```

### 4. 生成词典源文件

执行脚本生成包含索引的 MDict 文本源文件：

```bash
python3 generate_xiandai7.py
```

### 5. 构建词典主文件 (MDX)

使用 `mdict-utils` 打包词典索引及元数据：

```bash
mdict -a xiandai7.txt \
      --description xiandai7_description.html \
      --title xiandai7_title.txt \
      xiandai7.mdx
```

### 6. 构建资源包 (MDD)

将 `images/` 目录下的图片打包为资源文件：

```bash
mdict -a ./images/ xiandai7.mdd
```

---

## 使用说明

*   **样式调整**：图片比例可调整 `xiandai7.css` 文件设置，默认设置横向占比约 100%。
*   **同名原则**：确保 `xiandai7.mdx` 与 `xiandai7.mdd` 文件名完全一致，并置于同一目录下。
*   **致谢**：本项目基于 [dictkit/xiandai](https://github.com/dictkit/xiandai/) 的开源数据制作。
*   **测试验证**：Windows: [GoldenDict-ng](https://xiaoyifang.github.io/goldendict-ng/)，iOS: [MDict](https://apps.apple.com/us/app/mdict/id389083586)

## 资源链接

*   **在线版**：[《现代汉语词典》在线版](https://dictkit.github.io/xiandai/)
*   **原始 JP2 扫描件**：[Archive.org 下载地址](https://archive.org/details/modern-chinese-dictionary_7th-edition)
*   **词典文件下载**：[Releases](https://github.com/binsgit/xiandai7/releases)

