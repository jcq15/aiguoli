from PIL import Image, ImageFont, ImageDraw
import csv


# 长文本换行，txt：文本，width：区域宽度，font：所用字体
# 返回包含'\n'的字符串
# 我觉得PIL库应该实现一下这玩意，挺常用的
# 真啰嗦……
def long_text_split(txt, width, font):
    splited = []
    start = 0
    end = 1
    while end <= len(txt):
        while end <= len(txt) and font.getsize(txt[start:end])[0] <= width:
            end += 1
        splited.append(txt[start:end-1])
        start = end - 1
    return '\n'.join(splited)


def make_calendar(year, month, day, event, avoid):
    font_file = 'fonts/MSYHMONO.ttf'            # 微软雅黑mono字体
    color = (0, 0, 0)
    im = Image.open('resources/template.png')
    draw = ImageDraw.Draw(im)

    # year
    draw.text((327, 205), year, fill=color, font=ImageFont.truetype(font_file, 100))
    
    # month
    draw.text((700, 205), month, fill=color, font=ImageFont.truetype(font_file, 100))
    
    # day要居中，先计算位置再写
    font_day = ImageFont.truetype(font_file, 512)
    day_width = font_day.getsize(day)[0]
    day_y = int((im.size[0] - day_width) / 2)
    draw.text((day_y, 512), day, fill=color, font=font_day)

    # event
    font_event = ImageFont.truetype(font_file, 64)
    event_splited = long_text_split('[事件]'+event, 1062, font_event)
    draw.multiline_text((97, 1117), event_splited, spacing=50, fill=color, font=font_event)

    # avoid
    font_avoid = ImageFont.truetype(font_file, 64)
    avoid_splited = long_text_split('[注意事项]'+avoid, 1062, font_avoid)
    draw.multiline_text((97, 1526), avoid_splited, spacing=50, fill=color, font=font_avoid)

    return im


if __name__ == '__main__':
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for item in reader:
            # 忽略第一行
            if reader.line_num == 1:
                continue
            year, month, day = item[0].split('/')
            day = str(int(day))    # 去掉开头的0
            im = make_calendar(year, month, day, item[1], item[2]) 
            im.save('output/%s.png' % item[0].replace('/', ''))