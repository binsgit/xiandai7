#!/bin/bash

# =================================================================
# 现代汉语词典第7版 - 图片生成脚本
# =================================================================

JP2_DIR="现代汉语词典（Modern Chinese Dictionary）_jp2"
OUT_DIR="./images"
mkdir -p "$OUT_DIR"

get_jp2_idx() {
	local fname=$1
	if [[ $fname =~ ^A([0-9]{4})\.png$ ]]; then
		n=$((10#${BASH_REMATCH[1]}))
		[ "$n" -le 6 ] && echo $((n - 1))
	elif [[ $fname =~ ^B([0-9]{4})\.png$ ]]; then
		n=$((10#${BASH_REMATCH[1]}))
		[ "$n" -le 14 ] && echo $((n + 5))
	elif [[ $fname =~ ^C([0-9]{4})\.png$ ]]; then
		n=$((10#${BASH_REMATCH[1]}))
		[ "$n" -le 74 ] && echo $((n + 19))
	elif [[ $fname =~ ^([0-9]{4})\.png$ ]]; then
		n=$((10#${BASH_REMATCH[1]}))
		[ "$n" -ge 1 ] && [ "$n" -le 1799 ] && echo $((n + 93))
	elif [[ $fname =~ ^D([0-9]{4})\.png$ ]]; then
		n=$((10#${BASH_REMATCH[1]}))
		[ "$n" -le 4 ] && echo $((n + 1892))
	fi
}

# 检查 JP2_DIR 是否存在
if [ ! -d "$JP2_DIR" ]; then
	echo -e "\033[31m[ERROR] 找不到图片源目录或链接: $JP2_DIR\033[0m"
	echo "请检查路径是否正确，或者是否已建立软连接。"
	exit 1
fi

echo -e "原文件名 (JP2)\t\t\t\t\t | 现文件名 | 原尺寸 -> 现尺寸 | 原大小 -> 现大小 | 比例 | 模式"
echo "------------------------------------------------------------------------------------------------------------------------"

for prefix in A B C "" D; do
	case $prefix in
	A) range=$(seq -f "A%04g.png" 1 6) ;;
	B) range=$(seq -f "B%04g.png" 1 14) ;;
	C) range=$(seq -f "C%04g.png" 1 74) ;;
	"") range=$(seq -f "%04g.png" 1 1799) ;;
	D) range=$(seq -f "D%04g.png" 1 4) ;;
	esac

	for filename in $range; do
		idx=$(get_jp2_idx "$filename")
		jp2_name=$(printf "现代汉语词典（Modern Chinese Dictionary）_%04d.jp2" $idx)
		jp2_path="$JP2_DIR/$jp2_name"
		[ ! -f "$jp2_path" ] && continue

		is_special=false
		# 默认正文缩放参数
		resize_param="1880x1880"

		# 匹配特殊文件（包含 A1-6 和 D2-4）
		case "$filename" in
		A0001.png | A0002.png | A0003.png | A0004.png | A0005.png | A0006.png | D0002.png | D0003.png | D0004.png)
			is_special=true
			;;
		esac

		# === 缩放逻辑 ===
		if [ "$is_special" = true ]; then
			mode_tag="Special"
			out_file="${filename%.png}.jpg"

			# 定义缩放参数，自动匹配长边并等比例缩放
			resize_cmd="-resize 1880x1880"

			case "$filename" in
			A0005.png | A0006.png)
				# 文字类特殊页：灰度 JPG
				convert "$jp2_path" -strip $resize_cmd -units PixelsPerInch -density 96 -colorspace Gray -quality 85 -interlace Plane -strip "$OUT_DIR/$out_file"
				;;
			*)
				# 彩色类特殊页：sRGB JPG
				convert "$jp2_path" -strip $resize_cmd -units PixelsPerInch -density 96 -sampling-factor 4:2:0 -quality 85 -interlace Plane -strip "$OUT_DIR/$out_file"
				;;
			esac
		else
			mode_tag="Text"
			out_file="$filename"
			# 使用高效 PNG8 策略
			convert "$jp2_path" \
				-strip \
				-filter Lanczos \
				-resize $resize_param \
				-units PixelsPerInch \
				-density 96 \
				-colorspace Gray \
				-unsharp 1.5x1.2+1.5+0.02 \
				-level 10%,90% \
				-depth 8 \
				-colors 256 \
				-strip \
				png8:"$OUT_DIR/$out_file"
		fi

		# 统计部分
		old_dim=$(identify -format "%wx%h" "$jp2_path")
		new_dim=$(identify -format "%wx%h" "$OUT_DIR/$out_file")
		old_size=$(du -k "$jp2_path" | cut -f1)
		new_size=$(du -k "$OUT_DIR/$out_file" | cut -f1)
		ratio=$(awk "BEGIN {if ($old_size>0) printf \"%.2f\", $new_size/$old_size; else print \"0.00\"}")

		printf "%-40s | %-8s | %-11s -> %-11s | %4dKB -> %4dKB | %s | %s\n" \
			"$jp2_name" "$out_file" "$old_dim" "$new_dim" "$old_size" "$new_size" "${ratio}x" "$mode_tag"
	done
done
