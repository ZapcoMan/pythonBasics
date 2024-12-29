import turtle

def draw_circle(color, position):
    try:
        turtle.color(color)
        turtle.penup()
        turtle.goto(position)
        turtle.pendown()
        turtle.circle(50)
        turtle.penup()
    except Exception as e:
        print(f"Error drawing circle: {e}")

if __name__ == '__main__':
    # 设置画笔宽度为10像素
    turtle.width(10)

    # 定义要绘制的圆的信息
    circles = [
        ("blue", (0, -50)),
        ("black", (120, -50)),
        ("red", (240, -50)),
        ("yellow", (55, -100)),
        ("green", (180, -100))
    ]

    # 将画笔移动到起始位置
    turtle.penup()
    turtle.goto(120, 20)
    turtle.pendown()

    # 绘制所有圆
    for color, position in circles:
        draw_circle(color, position)

    # 防止窗口立即关闭
    turtle.done()
