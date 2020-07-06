import cv2
import numpy as np
import pandas as pd
import argparse

#CLI to accept image path
ap=argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True,help='image path')
args=vars(ap.parse_args())
img_path=args['image']

#reading image with cv2
img=cv2.imread(img_path)


clicked=False
r=g=b=xpos=ypos=0

index=["color","color_name","hex","R","G","B"]
csv=pd.read_csv('C:/Users/SATYAJIT/Desktop/colors/colors.csv',names=index,header=None)

#using K-nn classifier algorithm
#finding the closest similar RGB combination

def getColorName(R,G,B):
    minimum=10000
    for i in range(len(csv)):
        d=abs(R-int(csv.loc[i,"R"]))+abs(G-int(csv.loc[i,"G"]))+abs(B-int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum=d
            cname=csv.loc[i,"color_name"]
    return cname

#function to get the coordinates of point of mouse double click
def drawFunction(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos,clicked
        clicked=True
        xpos=x
        ypos=y
        b,g,r=img[y,x]
        b=int(b)
        g=int(g)
        r=int(r)
cv2.namedWindow('image')
cv2.setMouseCallback('image',drawFunction)

while(1):
    cv2.imshow("image", img)
    if (clicked):
        cv2.rectangle(img,(20,20),(750,60),(b,g,r),-1)  #arguments=cv2.rectangle(image,starting_point,ending_point,thickness)
        text=getColorName(r,g,b) + 'R ='+str(r) + 'B ='+str(b) + 'G ='+str(g)   #creating the color name of double clicked position
        #displaying text.parameters=cv2.putText(image,text,start,font_size,font_scale,font_color,thickness,line_type
        cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        if(r+g+b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA) #for very light colors font_color becomes black
        clicked=False
    if cv2.waitKey(20) & 0xFF == 27:
        break           #exit when user hits esc
    cv2.waitKey(20)

cv2.destroyAllWindows()