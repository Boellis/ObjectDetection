import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
import pymysql
#MySQL
pymysql.install_as_MySQLdb()
import MySQLdb

from utils.app_utils import FPS, WebcamVideoStream
from multiprocessing import Queue, Pool
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

CWD_PATH = os.getcwd()
#MySQL
db = MySQLdb.connect(user="boellis",password="patdev",host="localhost",db="pat")
cursor = db.cursor()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
# The path to frozen_inference_graph.pb is:
# ./desktop/object_detector_app/object_detection_ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb
#MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_NAME = 'soda_modelv5'
PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
# The path for the label map is:
PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'soda_label_map.pbtxt')

NUM_CLASSES = 4

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def detect_objects(image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    
    has_already_printed_sthg = False
    #db = MySQLdb.connect(user="boellis",password="patdev",host="localhost",db="pat")
    for index,value in enumerate(classes[0]):
        class_name = category_index[classes[0][0]]['name']
        if scores[0,index] > 0.5:
            if(class_name == 'coke'):
                cursor.execute("SELECT * FROM soda LIMIT 0,1")
                data=cursor.fetchall()
                print(data)
                if not has_already_printed_sthg: # Print this only once
                    print('This should print coke')
                    has_already_printed_sthg = True
            elif(class_name == 'sprite'):
                cursor.execute("SELECT * FROM soda LIMIT 1,1")
                data=cursor.fetchall()
                print(data)
                if not has_already_printed_sthg: # Print this only once
                    print('This should print sprite')
                    has_already_printed_sthg = True
            elif(class_name == 'dr_pepper'):
                cursor.execute("SELECT * FROM soda LIMIT 2,1")
                data=cursor.fetchall()
                print(data)
                if not has_already_printed_sthg: # Print this only once
                    print('This should print dr_pepper')
                    has_already_printed_sthg = True
            elif(class_name == 'orange_fanta'):
                cursor.execute("SELECT * FROM soda LIMIT 3,1")
                data=cursor.fetchall()
                print(data)
                if not has_already_printed_sthg: # Print this only once
                    print('This should print orange_fanta')
                    has_already_printed_sthg = True
    return image_np


def worker(input_q, output_q):
    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        #sess = tf.Session(graph=detection_graph)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(graph=detection_graph, config=config)



    fps = FPS().start()
    while True:
        fps.update()
        frame = input_q.get()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output_q.put(detect_objects(frame_rgb, sess, detection_graph))

    fps.stop()
    sess.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-src', '--source', dest='video_source', type=int,
                        default=0, help='Device index of the camera.')
    parser.add_argument('-wd', '--width', dest='width', type=int,
                        default=1000, help='Width of the frames in the video stream.')
    parser.add_argument('-ht', '--height', dest='height', type=int,
                        default=500, help='Height of the frames in the video stream.')
    parser.add_argument('-num-w', '--num-workers', dest='num_workers', type=int,
                        default=2, help='Number of workers.')
    parser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
                        default=5, help='Size of the queue.')
    args = parser.parse_args()
    """
    parser.add_argument('-wd', '--width', dest='width', type=int,
                        default=480, help='Width of the frames in the video stream.')
    parser.add_argument('-ht', '--height', dest='height', type=int,
                        default=360, help='Height of the frames in the video stream.')
    """

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)

    input_q = Queue(maxsize=args.queue_size)
    output_q = Queue(maxsize=args.queue_size)
    pool = Pool(args.num_workers, worker, (input_q, output_q))

    video_capture = WebcamVideoStream(src=args.video_source,
                                      width=args.width,
                                      height=args.height).start()
    fps = FPS().start()

    while True:  # fps._numFrames < 120
        frame = video_capture.read()
        input_q.put(frame)

        t = time.time()

        output_rgb = cv2.cvtColor(output_q.get(), cv2.COLOR_RGB2BGR)
        cv2.imshow('Video', output_rgb)
        fps.update()

        print('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    fps.stop()
    print('[INFO] elapsed time (total): {:.2f}'.format(fps.elapsed()))
    print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))

    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()
