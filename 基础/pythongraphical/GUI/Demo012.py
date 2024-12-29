import turtle

if __name__ == '__main__':
    # 设置画笔宽度为10像素
    turtle.width(10)
    # 将画笔移动到起始位置
    turtle.penup()
    turtle.goto(120, 20)
    turtle.pendown()
    # 第一个圆
    # 设置画笔颜色为蓝色，并绘制一个半径为50像素的圆
    turtle.color("blue")
    turtle.penup()
    turtle.goto(0, -50)
    turtle.pendown()
    turtle.circle(50)
    turtle.penup()
    # 第二个圆
    # 设置画笔颜色为黑色，并绘制一个半径为50像素的圆
    turtle.color('black')
    turtle.goto(120, -50)
    turtle.pendown()
    turtle.circle(50)
    turtle.penup()
    # 第三个圆形
    # 设置画笔颜色为红色，并绘制一个半径为50像素的圆
    turtle.color('red')
    turtle.goto(240, -50)
    turtle.pendown()
    turtle.circle(50)
    turtle.penup()
    # 第四个圆形
    # 设置画笔颜色为黄色，并绘制一个半径为50像素的圆
    turtle.color('yellow')
    turtle.goto(55, -100)
    turtle.pendown()
    turtle.circle(50)
    turtle.penup()
    # 第五个圆形
    # 设置画笔颜色为绿色，并绘制一个半径为50像素的圆
    turtle.color('green')
    turtle.goto(180, -100)
    turtle.pendown()
    turtle.circle(50)
    turtle.penup()
