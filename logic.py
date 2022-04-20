import requests
import urllib
import base64
import webbrowser
from PIL import Image
import numpy as np

def face(arr,old):
    face=arr[8:16,8:16]
    f=Image.fromarray(face)
    f.save("face.png")

def front(arr,old):
    front=np.copy(arr[0:32,0:16])
    #white background
    front[:,:,:]=0
    if(old):
        #face
        front[0:8,4:12] = arr[8:16,8:16]
        #body
        front[8:20,4:12] = arr[20:32,20:28]
        #left arm
        front[8:20,0:4] = arr[20:32,44:48]
        #right arm
        front[8:20,12:16] = arr[20:32,44:48]
        #left leg
        front[20:32,4:8] = arr[20:32,4:8]
        #right leg
        front[20:32,8:12] = arr[20:32,4:8]
        f=Image.fromarray(front)
        f.save("front.png")
    else:
        #face
        front[0:8,4:12] = arr[8:16,8:16]
        #body
        front[8:20,4:12] = arr[20:32,20:28]
        #left arm
        front[8:20,0:4] = arr[20:32,44:48]
        #right arm
        front[8:20,12:16] = arr[52:64,36:40]
        #left leg
        front[20:32,4:8] = arr[20:32,4:8]
        #right leg
        front[20:32,8:12] = arr[52:64,20:24]
        f=Image.fromarray(front)
        f.save("front.png")

def side(arr,old):
    if(old):
        side=np.copy(arr[0:32,0:16])
        #white background
        side[:,:,:]=0
        #face
        side[0:8,4:12] = arr[8:16,0:8]
        #left leg
        side[20:32,6:10] = arr[20:32,0:4]
        #left arm
        side[8:20,6:10] = arr[20:32,40:44]
        f=Image.fromarray(side)
        f.save("side.png")
    else:
        side=np.copy(arr[0:32,0:16])
        #white background
        side[:,:,:]=0
        #face
        side[0:8,4:12] = arr[8:16,0:8]
        #left leg
        side[20:32,6:10] = arr[20:32,0:4]
        #left arm
        #side[8:20,6:10] = arr[52:64,32:36]
        side[8:20,6:10] = arr[52:64,40:44]
        f=Image.fromarray(side)
        f.save("side.png")

def upscale(file,x):
    arr=np.array(Image.open(file))
    shape=np.shape(arr)
    print(shape[0]*x,shape[1]*x)
    big=np.zeros((shape[0]*x,shape[1]*x,4),dtype=np.uint8)
    for r in range(shape[0]):
        for c in range(shape[1]):
            big[(r*x):((r+1)*x),c*x:((c+1)*x)] = arr[r,c]
    f=Image.fromarray(big)
    f.save(file)

            



Username = input("What account do you want information on?: ")
UUID = requests.request("GET","https://api.mojang.com/users/profiles/minecraft/"+Username)
UUID=UUID.json()["id"]
print(UUID)

skinlink = (requests.request("GET","https://sessionserver.mojang.com/session/minecraft/profile/"+UUID)).json()["properties"][0]["value"]
skinlink=base64.b64decode(skinlink)
skinlink=(skinlink.decode().split()[18]).split("\"")[1]
print(skinlink)

skin=urllib.request.urlretrieve(skinlink, "sample.png")
im=Image.open("sample.png")
im=np.array(im)
print(np.shape(im))

if(np.shape(im)[0]<60):

    old=True
else:
    old=False
side(im,old)
front(im,old)
face(im,old)

upscale("face.png",10)
upscale("sample.png",10)
upscale("front.png",10)
upscale("side.png",10)

file = open("namedata.txt", "a")
file.truncate(0)
name_history=requests.request("GET", "https://api.mojang.com/user/profiles/"+UUID+"/names").json()
for i in name_history:
    file.write(i["name"]+"\n")
file.close()

webbrowser.open("index.html")


'''
skinlink = (requests.request("GET","https://sessionserver.mojang.com/session/minecraft/profile/"+UUID)).json()["properties"][0]["value"]
skinlink=base64.b64decode(skinlink)
skinlink=(skinlink.decode().split()[18]).split("\"")[1]
print(skinlink)
skin=urllib.request.urlretrieve(skinlink, "sample.png")
'''