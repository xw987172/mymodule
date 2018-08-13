#coding:utf8
from PIL import Image
i = 1
j = 1

img = Image.open("self.jpg")

print(img.size)
for i in range(16):
    for j in range(16):
        print(img.getpixel((4,4)))

width,height = img.size

for i in range(width):
    for j in range(height):
        data = img.getpixel((i,j))
        # print(data)
        if abs(data[0]-23)<=4 and abs(data[1]-160)<=8 and abs(data[2]-241)<=8:
            img.putpixel((i,j),(255,255,255,1))
img = img.convert("RGB")
img.save("new3.jpg")