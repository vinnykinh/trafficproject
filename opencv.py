import time
import cv2
import numpy as np

# step 2 load yolo
# We load the algorythm. The run the algorythm we need three files:
# Weight file: it’s the trained model, the core of the algorythm to detect the objects.
# Cfg file: it’s the configuration file, where there are all the settings of the algorythm.
# Name files: contains the name of the objects that the algorythm can detect.
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# defining the start time
starting_time = time.time()
# initialize the frame_id as 0
frame_id = 0
#test list file 
density =[8,2,7,4]
textfile= open("density.txt","w")
for element in density:
    textfile.write(str(element))
textfile.close()
list_of_vehicles = ["car", "bus", "motorbike", "truck", "bicycle"]
# defining the layernames
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

#randomizes between the range of colors
colors = np.random.uniform(20, 255, size=(len(classes), 3))

# Loading image
cap0 = cv2.VideoCapture("sample_videos/lane.mkv")
cap3 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture("sample_videos/bridge.mp4")
cap4 = cv2.VideoCapture("sample_videos/test.mp4")
# Object detection from Stable camera
vehicle_lane0_count = 0


def cameraFeed(frame_id, vehicle_lane0_count, camera):
        ret, img = camera.read()
        frame_id += 1
        vw = img.shape[1]
        vh = img.shape[0]
        print(img.shape)

        img = cv2.resize(img, None, fx=0.7, fy=0.7)
        # cam3 = cv2.resize(cam3, None, fx=0.4, fy=0.4)
        # get the height and width of each frame in the video
        height, width, channels = img.shape
        # 1. Object Detection
        # Showing informations on the screen
        # Detecting objects
        # the blob is used to extract feature from the image and resize them as Yolo accept only three sizes
        # 320X320 for less accuracy
        # 609x609 for high accuracy
        # 416x416 for mid accuracy
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True, crop=False)
        # blob = cv2.dnn.blobFromImage(roi, 1 / 255, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        # the  variable outs is the result of the detection
        outs = net.forward(output_layers)
        class_ids = []
        confidences = []
        boxes = []
        # We then loop trough the outs array
        # we calculate the confidence and we choose a confidence threshold.
        for out in outs:
            for detection in out:
                # defined array for scores
                scores = detection[5:]
                # function np.argmax returns indices of the max element of the scores
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # we set a threshold confidence of 0.5,
                # if it’s greater we consider the object correctly detected, otherwise we skip it.
                # The threshold goes from 0 to 1. The closer to 1 the greater is the accuracy of the detection,
                # while the closer to 0 the less is the accuracy but also it’s greater the number of the objects detected.
                if confidence > 0.55:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    for (x, y, w, h) in boxes:
                        automotiveCY = int(y + h / 2)
                        linCy = height - 200
                        if linCy + 2 > automotiveCY > linCy - 2:
                            vehicle_lane0_count = vehicle_lane0_count + 1
                            cv2.line(img, (100, height - 100), (width - 0, height - 100), (0, 0, 255), 5)

        # When we perform the detection, it happens that we have more boxes for the same object,
        # so we should use another function to remove this “noise”.
        # It’s called Non maximum suppresion.
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # define the font to be used
        font = cv2.FONT_ITALIC
        dets = []
        for i in range(len(boxes)):
            if i in indexes:
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                dets.append([x, y, x + w, y + h, confidences[i]])
                # label- Box: contain the coordinates of the rectangle sorrounding the object detected.
                # Label: it’s the name of the object detected
                # Confidence: the confidence about the detection from 0 to 1.
                label = classes[class_ids[i]]
                print(label)
                color =colors[i]

                fontSize = 0.6
                fontthickness = 2
                eleapsed_time = time.time() - starting_time
                fps = frame_id / eleapsed_time
                # drawing the features into the image detected
                # Display the ID at the center of the box
                cv2.putText(img, "VEHICLE COUNT : " + str(vehicle_lane0_count), (450, 70), font, fontSize, (0, 0, 255),
                            fontthickness)
                cv2.putText(img, "FPS : " + str(fps), (450, 30), font, fontSize, (0, 0, 255),
                            fontthickness)
                cv2.putText(img, str(label), (x, y + 40), font, fontSize, color, fontthickness)

                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, str(round(confidences[0], 2) * 100) + "%", (x, y - 20), font, fontSize, color, fontthickness)
                # camera 2
        # show each frame as it occurs

        cv2.imshow("Image", img)

        # cv2.imshow("image",frame)
        print(vehicle_lane0_count)


while 1:
    cameraFeed(frame_id,vehicle_lane0_count,cap0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
