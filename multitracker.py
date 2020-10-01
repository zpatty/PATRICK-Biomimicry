#!/usr/bin/env python

import sys
import cv2
from random import randint
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
 
def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]: 
    tracker = cv2.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)
     
  return tracker

# Set video to load
videoPath = r"/home/zpatty/Documents/git-repos/biomimic_patrick/near_tip_cut.mp4"
 
# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)
 
# Read first frame
success, frame = cap.read()
# quit if unable to read the video file
if not success:
  print('Failed to read video')
  sys.exit(1)


bboxes = []
colors = [] 
 
# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects
while True:
  # draw bounding boxes over objects
  # selectROI's default behaviour is to draw box starting from the center
  # when fromCenter is set to false, you can draw box starting from top left corner
  bbox = cv2.selectROI('MultiTracker', frame)
  bboxes.append(bbox)
  colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
  print("Press q to quit selecting boxes and start tracking")
  print("Press any other key to select next object")
  k = cv2.waitKey(0) & 0xFF
  if (k == 113):  # q is pressed
    break
 
print('Selected bounding boxes {}'.format(bboxes))

# Specify the tracker type
trackerType = "CSRT"   
 
# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()
 
# Initialize MultiTracker 
for bbox in bboxes:
  multiTracker.add(createTrackerByName(trackerType), frame, bbox)


centroids = []

# Process video and track objects
while cap.isOpened():
  success, frame = cap.read()
  if not success:
    break
   
  # get updated location of objects in subsequent frames
  success, boxes = multiTracker.update(frame)
 
  # draw tracked objects
  centroid_step = []
  for i, newbox in enumerate(boxes):
    print(newbox)
    p1 = (int(newbox[0]), int(newbox[1]))
    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
    cent = np.mean([p1,p2],axis=0)
    centroid_step.append(cent)
    cv2.circle(frame,(int(cent[0]),int(cent[1])),10,colors[i])
  print("\n")
  centroids.append(centroid_step)
 
  # show frame
  cv2.imshow('MultiTracker', frame)
   
  # quit on ESC button
  if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
    break
sio.savemat(r'C:\Users\Zach\Documents\MEGAsync\SML\Code\centroids_alt1.mat',{'centroids':np.array(centroids)})
