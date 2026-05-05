import json
import os

# === 配置区 ===
DATA_DIR = './xiandai/docs/data/'
OUTPUT_FILE = 'xiandai7.txt'

def format_page_id(page):
    """统一页码格式：数字转为 p0001，非数字(A/B/C/D)保持原样"""
    p_str = str(page).strip()
    if p_str.isdigit():
        return f"p{int(p_str):04d}"
    return p_str

def generate():
    # 1. 加载所有 JSON 数据
    try:
        with open(os.path.join(DATA_DIR, 'toc.json'), 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
        with open(os.path.join(DATA_DIR, 'words.json'), 'r', encoding='utf-8') as f:
            words_data = json.load(f)
        with open(os.path.join(DATA_DIR, 'chars.json'), 'r', encoding='utf-8') as f:
            chars_data = json.load(f)
        with open(os.path.join(DATA_DIR, 'pinyin.json'), 'r', encoding='utf-8') as f:
            pinyin_data = json.load(f)
    except FileNotFoundError as e:
        print(f"错误：找不到文件 - {e}")
        return

    mdx_entries = []

    # === 策略一：构建物理页面全序列 (决定 上一页/下一页 逻辑) ===
    full_sequence = []
    full_sequence += [f"A{i:04d}" for i in range(1, 7)]    # A0001-A0006
    full_sequence += [f"B{i:04d}" for i in range(1, 15)]   # B0001-B0014
    full_sequence += [f"C{i:04d}" for i in range(1, 75)]   # C0001-C0074
    full_sequence += [f"p{i:04d}" for i in range(1, 1800)] # p0001-p1799
    full_sequence += [f"D{i:04d}" for i in range(1, 5)]    # D0001-D0004

    # === 策略二：生成物理页条目 (存放图片和导航锚点) ===
    for i, page_id in enumerate(full_sequence):
        prev_id = full_sequence[i-1] if i > 0 else "#"
        next_id = full_sequence[i+1] if i < len(full_sequence)-1 else "#"
        
        img_name = page_id.replace('p', '') + ".png"
        
        content = f'<img class="pic" src="/{img_name}"><br>\n'
        content += '<center>'
        content += f'<a href="entry://{prev_id}">上一页</a>　' if prev_id != "#" else "上一页　"
        content += '<a href="entry://.">目录</a>　'
        content += '<a href="entry://C0013">部首</a>　'
        content += '<a href="entry://C0006">音节</a>　'
        content += f'<a href="entry://{next_id}">下一页</a>' if next_id != "#" else "下一页"
        content += '</center>'
        
        mdx_entries.append(f"{page_id}\n{content}\n</>")

    # === 策略三：构建总目录页 (.) 及功能性重定向 ===
    toc_html = '<div class="toc-header"><h2>现代汉语词典 (第7版) 目录</h2></div><ul class="toc-list">'
    
    # 遍历 toc.json
    for i, item in enumerate(toc_data):
        p_id = format_page_id(item['page'])
        
        # 区分目录显示逻辑：前 122 行通常是前言、目录及字母索引
        if i < 122:
            # 构建简化的目录 HTML 列表：去掉拼音页码链接，仅保留标题链接
            toc_html += f'<li><a href="entry://{p_id}"><b>{item["title"]}</b></a>'
            
            # 如果是“版本说明”或“附录”这类有 sub-title 的项，保留其子标题链接
            # 但排除了拼音索引类的 sub-items (即 title 为单个字母的情况)
            if 'more' in item and not (len(item['title']) == 1 and item['title'].isalpha()):
                sub_links = [f'<a href="entry://{format_page_id(m["page"])}">{m["title"]}</a>' for m in item['more']]
                toc_html += ' <span style="font-size:0.9em; color:#666;">(' + ' | '.join(sub_links) + ')</span>'
            
            toc_html += '</li>'
            
            # 生成功能重定向 (如搜索 ".封面")[cite: 1]
            mdx_entries.append(f".{item['title']}\n@@@LINK={p_id}\n</>")
        
        # 即使不在目录页显示，所有 toc 项目（包含拼音）依然建立后台索引[cite: 1]
        mdx_entries.append(f"{item['title']}\n@@@LINK={p_id}\n</>")

    toc_html += '</ul>'
    mdx_entries.append(f".\n{toc_html}\n</>")

    # === 策略四：关键词大规模重定向 (采用同名分列策略) ===
    # 1. 词条 (words.json)
    for word, pg in words_data.items():
        mdx_entries.append(f"{word}\n@@@LINK={format_page_id(pg)}\n</>")
    
    # 2. 单字 (chars.json)
    for char, pgs in chars_data.items():
        pages = pgs if isinstance(pgs, list) else [pgs]
        for pg in pages:
            mdx_entries.append(f"{char}\n@@@LINK={format_page_id(pg)}\n</>")
        
    # 3. 带音调拼音 (pinyin.json)
    for py, pg in pinyin_data.items():
        mdx_entries.append(f"{py}\n@@@LINK={format_page_id(pg)}\n</>")

    # === 最终写入 ===
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(mdx_entries) + "\n")

    print(f"成功！已生成源文件: {OUTPUT_FILE}，总词条数: {len(mdx_entries)}")

if __name__ == "__main__":
    generate()

