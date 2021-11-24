import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import time


def main():
    _first_num = random.randint(1, 1000)
    _code_style = ['加', '减', '乘', '+', '-', '*']
    _last_num = random.randint(1, 1000)
    init_chars = [str(_first_num), random.choices(_code_style)[0], str(_last_num)]

    def create_validate_code(size=(150, 50),
                             chars=init_chars,
                             img_type="PNG",
                             mode="RGB",
                             bg_color=(255, 255, 255),
                             fg_color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                             font_size=18,
                             font_type="./msyh.ttc",
                             draw_lines=True,
                             n_line=(1, 2),
                             draw_points=True,
                             point_chance=1):
        """
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        """

        width, height = size  # 宽高
        # 创建图形
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)  # 创建画笔

        def get_chars():
            return chars

        def create_lines():
            """绘制干扰线"""
            line_num = random.randint(*n_line)  # 干扰线条数

            for i in range(line_num):
                # 起始点
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                # 结束点
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            """绘制干扰点"""
            chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            """绘制验证码字符"""
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)
            font_width /= 0.7
            font_height /= 0.7
            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                      strs, font=font, fill=fg_color)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 80,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 80,
                  float(random.randint(3, 5)) / 450,
                  0.001,
                  float(random.randint(3, 5)) / 450
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
        output_buffer = BytesIO()
        img.save(output_buffer, format='PNG')
        img_byte_data = output_buffer.getvalue()
        # img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
        return img_byte_data, strs
    res = create_validate_code()
    return res


main()
try:
    os.mkdir('./训练图片生成')
except FileExistsError:
    print('训练图片生成 文件夹已经存在')
print('生成存储文件夹成功')
while 1:
    number = input('请输入要生成的验证码数量')
    try:
        for i in range(int(number)):
            res = main()
            with open('./picture/{0}_{1}.png'.format(res[1].replace('*', '乘'), int(time.time())), 'wb') as f:
                f.write(res[0])
            print('生成第', i+1, '个图片成功')
    except ValueError:
        print('请输入一个数字，不要输入乱七八糟的东西，打你哦')
    except:
        import traceback
        traceback.print_exc()
        break
    input('理论上生成完成了~，QAQ 共生成了' + number + '个验证码')
input('出现未知错误，错误已打印')
