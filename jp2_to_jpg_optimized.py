import os
import subprocess

# === 配置区 ===
SOURCE_DIR = "现代汉语词典（Modern Chinese Dictionary）_jp2"
TARGET_DIR = "images"
TARGET_HEIGHT = 1750
# 82 是一个黄金平衡点：文字依然清晰，但体积比 90+ 小得多
IMG_QUALITY = 82 

def get_sorted_jp2_files(src_dir):
    """文件名已补零对齐，直接使用标准排序"""
    files = sorted([f for f in os.listdir(src_dir) if f.endswith('.jp2')])
    return [os.path.join(src_dir, f) for f in files]

def convert_image(src_path, target_name):
    """从 JP2 转换为体积优化后的 JPG"""
    target_path = os.path.join(TARGET_DIR, f"{target_name}.jpg")
    
    # -strip: 移除所有内嵌元数据，减小单文件体积
    # -resize x1750: 固定高度，宽度按比例缩放，确保页面对齐
    # -sampling-factor 4:2:0: 降低色度抽样，对黑白文字图片非常有效
    # -interlace Plane: 生成渐进式 JPEG，通常具有更高的压缩率
    cmd = [
        "convert", src_path,
        "-resize", f"x{TARGET_HEIGHT}",
        "-strip",
        "-sampling-factor", "4:2:0",
        "-interlace", "Plane",
        "-quality", str(IMG_QUALITY),
        target_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        # 仅打印文件名，避免日志刷屏
        print(f"Done: {target_name}.jpg")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {src_path}: {e}")

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    all_files = get_sorted_jp2_files(SOURCE_DIR)
    total_files = len(all_files)
    print(f"开始处理，共计 {total_files} 个文件...")
    
    # 按照 A(6) -> B(14) -> C(74) -> p(1799) -> D(4) 逻辑映射
    layout = [
        ('A', 6),
        ('B', 14),
        ('C', 74),
        ('', 1799), 
        ('D', 4)
    ]

    current_idx = 0
    for prefix, count in layout:
        for i in range(1, count + 1):
            if current_idx >= total_files:
                return

            # 根据前缀生成目标文件名
            if prefix == '':
                target_name = f"{i:04d}"
            else:
                target_name = f"{prefix}{i:04d}"

            src_path = all_files[current_idx]
            convert_image(src_path, target_name)
            current_idx += 1

    print(f"\n全部转换完成！文件已存至 {TARGET_DIR} 目录。")

if __name__ == "__main__":
    main()

