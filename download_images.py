import os
import random
from PIL import Image, ImageDraw, ImageFont
import math

def draw_apple(filename, is_fresh):
    # 1. 创建一张深色背景的高清图片
    width, height = 800, 800
    img = Image.new('RGB', (width, height), color=(40, 40, 40))
    draw = ImageDraw.Draw(img)

    # 2. 设置颜色 (红苹果 和 烂苹果)
    if is_fresh:
        main_color = (220, 40, 40)    # 鲜艳的红
        highlight_color = (255, 100, 100)
        spot_color = None
    else:
        main_color = (110, 80, 50)    # 烂的暗色
        highlight_color = None
        spot_color = (40, 30, 20)     # 霉斑

    # 3. 绘制苹果的形状 (带顶部的凹陷)
    center_x, center_y = 400, 450
    points = []
    for i in range(360):
        rad = math.radians(i)
        x = math.cos(rad)
        y = math.sin(rad)
        
        # 在顶部 (y < 0 时) 往里收缩，形成苹果柄的凹陷
        if y < 0:
            x *= 0.85 
            y *= 0.9
        
        # 将点映射到 800x800 的画布上
        px = int(center_x + x * 240)
        py = int(center_y + y * 260)
        points.append((px, py))
        
    # 绘制苹果主体
    draw.polygon(points, fill=main_color, outline=None)

    # 4. 添加高光 (让红苹果看起来有光泽)
    if is_fresh:
        draw.ellipse([300, 320, 420, 440], fill=highlight_color, outline=None)
        # 稍微模糊一下高光让它更自然 (这里用半透明叠加模拟)
        highlight = Image.new('RGBA', (width, height), (0,0,0,0))
        h_draw = ImageDraw.Draw(highlight)
        h_draw.ellipse([300, 320, 420, 440], fill=(255, 255, 255, 80))
        img.paste(highlight, (0, 0), highlight)

    # 5. 绘制苹果把儿
    draw.rectangle([385, 160, 400, 230], fill=(80, 50, 30))
    # 画一片小叶子
    leaf_points = [(390, 170), (450, 150), (430, 190)]
    draw.polygon(leaf_points, fill=(60, 130, 60) if is_fresh else (100, 90, 60))

    # 6. 如果是烂苹果，画上随机霉斑
    if not is_fresh:
        for _ in range(100):
            # 限制霉斑主要分布在苹果内部
            spot_x = random.randint(200, 600)
            spot_y = random.randint(250, 650)
            spot_r = random.randint(8, 30)
            draw.ellipse([spot_x-spot_r, spot_y-spot_r, spot_x+spot_r, spot_y+spot_r], fill=spot_color)
    
    # 7. 保存文件
    img.save(filename)
    print(f"✅ 已生成: {filename}")

def main():
    # 清理旧文件
    for folder in ["fresh", "rotten"]:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                os.remove(os.path.join(folder, f))
        else:
            os.makedirs(folder)

    print("\n🎨 正在绘制新鲜的苹果...")
    for i in range(100):
        draw_apple(f"fresh/apple_{i+1}.jpg", is_fresh=True)

    print("\n🎨 正在绘制腐烂的苹果...")
    for i in range(100):
        draw_apple(f"rotten/apple_{i+1}.jpg", is_fresh=False)

    print("\n✨ 全部绘制完毕！快去 fresh 和 rotten 文件夹里看看吧！")

if __name__ == "__main__":
    main()