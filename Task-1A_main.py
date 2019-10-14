#classes and subclasses to import
import cv2
import numpy
from collections import deque
import os

filename = 'results1A_26.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)
    filep.close()
def main(path):
#####################################################################################################
    #Write your code here!!!
#####################################################################################################
 class shapedetector:
  def detect(self, c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c,0.04*peri, True)
    if len(approx) == 3:
      shape = "triangle"
    elif len(approx) == 4:
      (x, y, w, h) = cv2.boundingRect(approx)
      ar = w / float(h)
      if ar>1.05 and ar<=1.6: shape="rhombus"
      else: shape="trapezium"
    elif len(approx) == 5:
      shape = "pentagon"
    elif len(approx) == 6:
      shape = "hexagon"
    else:
      shape = "circle"
    return shape
 colors={'red':(25,255,255),'green':(102,255,255),'blue':(130,255,255)}
 img=cv2.imread(path,1)
 hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
 boundaries=[([0,100,100],[25,255,255]),([33,80,40],[102,255,255]),([110,50,50],[130,255,255])]
 for (lower,upper) in boundaries:
    key=upper
    if key==[25,255,255]: color='red'
    elif key==[102,255,255]: color='green'
    else: color='blue'
    lower=numpy.array(lower,dtype="uint8")
    upper=numpy.array(upper,dtype="uint8")
    mask=cv2.inRange(hsv,lower,upper)
    res=cv2.bitwise_and(img,img,mask=mask)
    cnts=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    sd=shapedetector()
    for cnt in cnts:
       M=cv2.moments(cnt)
       cx=int(M['m10']/M['m00'])
       cy=int(M['m01']/M['m00'])
       l=[cx,cy]
       shape=sd.detect(cnt)
       both="{} {} {}".format(shape,color,l)
       cv2.putText(img,both,(cx-20,cy-30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)
       cv2.imshow('out',img)
       writecsv(color,shape,(cx,cy))
 cv2.waitKey(0)
 cv2.destroyAllWindows()

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    global filename
    filename='results1A_26.csv'
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [os.path.join(mypath,f) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open(filename,'a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open(filename,'a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
