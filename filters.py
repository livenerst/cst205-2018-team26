from PIL import Image
import requests
from io import BytesIO

myUrl = "https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?auto=compress&cs=tinysrgb&h=350"
response = requests.get(myUrl)
img = Image.open(BytesIO(response.content))

#blue filter
def blueImage(pixel):
    return (pixel[0],int(pixel[1]*.3),int(pixel[2]*1.2))
b_list = map(blueImage,img.getdata())
img.putdata(list(b_list))
img.save('blueFlower.jpg')

#green filter
def greenImage(pixel):
    return (int(pixel[0]*.2),int(pixel[1]*2.5),int(pixel[2]*.2))
g_list = map(greenImage,img.getdata())
img.putdata(list(g_list))
img.save('greenFlower.jpg')

#red Filter
def redImage(pixel):
    return (int(pixel[0]*2.5),int(pixel[1]*.3),pixel[2])
r_list = map(redImage,img.getdata())
img.putdata(list(r_list))
img.save('redFlower.jpg')


def solarize(pixel):
    return ()
# img,1 - 4*x + 4(x**2)):
#     return (x[0],x[1],x[2],x[3])
solarList = map(solarize,img.getdata())
img.putdata(list(solarList))
img.save('solarImg.jpg')
