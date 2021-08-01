import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()

import pathlib
import cv2

# path to the folder containing .pb file
model_path = "trained_models"

# path to the folder containing images
image_path = "input_images"

# creating a tensorflow session (we will be using this to make our predictions later)
session = tf.Session(graph=tf.Graph())

# laoding model into session
tf.saved_model.loader.load(session, ['serve'], model_path)

# extract the coordinates of the rectange that's to be drawn on the image
def draw_boxes(height, width, box, img):
  # starting coordinates of the box
  ymin = int(max(1, (box[0] * height)))
  xmin = int(max(1, (box[1] * width)))
  # last coordinates of the box
  ymax = int(min(height, (box[2] * height)))
  xmax = int(min(width, (box[3] * width)))
  
  # draw a rectange using the coordinates
  cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (10, 255, 0), 10)

for file in pathlib.Path(image_path).iterdir():
    # get the current image path

    # current_image_path = r"{}".format(file.resolve())
    current_image_path = str(file.resolve())

    # image bytes since this is what Google ML model needs as input
    img_bytes = open(current_image_path, 'rb').read()

    # pass image as input to Google ML model and get the result
    result = session.run(['detection_boxes:0', 'detection_scores:0'], feed_dict = {
        'encoded_image_string_tensor:0' : [img_bytes]
    })

    print (result)

    boxes = result[0][0]
    scores = result[1][0]

    print ("File {} ".format(file.stem))

    # read the image with opencv
    img = cv2.imread(current_image_path)
    imH, imW, _ = img.shape

    for i in range(len(scores)):
        # only consider dected object if it's probability is above 25%
        if scores[i] > 0.75:
            print ("The box {} has probability {}".format(boxes[i], scores[i] ))
            draw_boxes(imH, imW, boxes[i], img)
    
    # resize image to fir screen
    new_img = cv2.resize(img, (1280, 1200))

    # show image on screen
    cv2.imshow("image", new_img)
    cv2.waitKey(0)





