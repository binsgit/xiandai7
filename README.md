# 现代汉语词典（第7版）数字制作指南

本指南介绍如何将开源的《现代汉语词典》第7版扫描件制作成标准的 MDict 格式（`.mdx`, `.mdd`）。

## 环境准备

```bash
python -m venv venv
source venv/bin/activate
pip install mdict-utils
```

## 制作流程

### 1. 获取制作文件

克隆本项目仓库以获取转换脚本与扫描资源：

```bash
git clone https://github.com/dictkit/xiandai.git
```

### 2. 同步 TOC 配置

为了对齐非正文部分的页码与图片映射，需覆盖原始 `toc.json`：

```bash
cp toc.json xiandai/docs/data/
```

### 3. 图像资源准备

运行 `cp_img.sh` 脚本，自动从仓库中提取、重命名并归档图片至 `images/` 目录：

```bash
bash cp_img.sh
```

### 4. 生成词典源文件

执行主脚本生成包含 7.8 万条索引的 MDict 文本源文件：

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

*   **同名原则**：确保 `xiandai7.mdx` 与 `xiandai7.mdd` 文件名完全一致，并置于同一目录下。
*   **词典图标**：准备一张正方形封面图命名为 `xiandai7.png` 即可显示词典图标。
*   **致谢**：本项目基于 [dictkit/xiandai](https://github.com/dictkit/xiandai/) 的开源数据制作。

## 资源链接

*   **在线版**：[《现代汉语词典》在线版](https://dictkit.github.io/xiandai/)
*   **原始 JP2 扫描件**：[Archive.org 下载地址](https://archive.org/details/modern-chinese-dictionary_7th-edition)
*   `jp2_to_jpg_optimized.py` 文件用于优化原始 JP2 文件，不过显然还有较大优化空间，最终制作时直接使用了优化后的文件

