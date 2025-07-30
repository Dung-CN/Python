#Khai báo thư viện
from PIL import Image
import turtle

#Risize hình ảnh robot
img=Image.open("anh_robot.gif")
img_resize=img.resize((50,50))
img_resize.save("anh_robot_1.gif")

#Tạo sceen turtle
s = turtle.Screen()
s.addshape("anh_robot_1.gif")
s.bgcolor("black")
#Tạo đối tượng turtle-1,2,3
t1=turtle.Turtle()
t2=turtle.Turtle()
t3=turtle.Turtle() 
 
for t, color, x, y in zip([t1, t2, t3], ["red", "green", "blue"], [-130, -50, 160], [100, -100, 110]):
    t.color(color)
    t.shape("anh_robot_1.gif")
    t.pensize(20)
    t.speed(0)
    t.penup()
    t.goto(x, y)
    t.pendown()
# xoay hướng Robot_1
t1.setheading(-195)     

for step in range(180):
    #In ra màn hình chữ C
    if step < 180: 
        t1.circle(100, 1.2)
	#In ra màn hình chữ N
    if step < 60:
        t2.setheading(90)
        t2.forward(3.4)
    elif step == 60:
        t2.setheading(-59)
    elif 60<= step < 120:	
        t2.forward(3.9)
    elif step == 120:
        t2.setheading(90)
    elif 120 <= step < 180:
        t2.forward(3.4)
    #In ra màn hình chữ D
    if step < 90:
        t3.setheading(-90)
        t3.forward(2.4)
    elif step == 90:
        t3.setheading(10)
    elif 90 <= step < 180:
        t3.circle(110, 1.8)

for t, x, y in zip ([t1, t2, t3], (0, 0, 0), (170, 170, 170)):
	t.penup()
	t.goto(x,y)
	t.pendown()

turtle.mainloop()