#!/bin/bash

# 创建目标目录
mkdir -p images

# 1. 复制正文主要部分 0001-1766.png
# 注意：0000.png 通常为封面或空白页，也会一并复制
echo "Copying main body images (0000-1766)..."
cp xiandai/docs/images/*.png images/

# 2. 复制 A0001-A0006 -> images/ (原名)
echo "Processing A0001-A0006..."
for i in $(seq 1 6); do
	src=$(printf "xiandai/docs/extra/A%04d.png" $i)
	cp "$src" images/
done

# 3. 复制 A0007-A0020 -> images/B0001-B0014
echo "Processing B0001-B0014..."
for i in $(seq 7 20); do
	src=$(printf "xiandai/docs/extra/A%04d.png" $i)
	target=$(printf "images/B%04d.png" $((i - 6)))
	cp "$src" "$target"
done

# 4. 复制 A0021-A0094 -> images/C0001-C0074
echo "Processing C0001-C0074..."
for i in $(seq 21 94); do
	src=$(printf "xiandai/docs/extra/A%04d.png" $i)
	target=$(printf "images/C%04d.png" $((i - 20)))
	cp "$src" "$target"
done

# 5. 复制 C0034-C0037 -> images/D0001-D0004
echo "Processing D0001-D0004..."
for i in $(seq 34 37); do
	src=$(printf "xiandai/docs/extra/C%04d.png" $i)
	target=$(printf "images/D%04d.png" $((i - 33)))
	cp "$src" "$target"
done

# 6. 复制 C0001-C0033 -> images/1767.png-1799.png
echo "Processing 1767-1799..."
for i in $(seq 1 33); do
	src=$(printf "xiandai/docs/extra/C%04d.png" $i)
	target=$(printf "images/%04d.png" $((i + 1766)))
	cp "$src" "$target"
done

echo "Done! All images are now in the 'images/' directory and properly indexed."
