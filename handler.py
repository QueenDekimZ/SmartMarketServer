# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, redirect, Response

# from flask_uploads import configure_uploads, UploadSet
# from werkzeug.wrappers import Response, Request
from utils import label_map_util
from utils import visualization_utils as vis_util

import json
import cv2
import os
# cap = cv2.VideoCapture(0)
# cap.set(10,200)

PATH_TO_CKPT = 'ssd_mobilenet_v1_coco/frozen_inference_graph.pb'
PATH_TO_LABELS = 'ssd_mobilenet_v1_coco/mscoco_label_map.pbtxt'
NUM_CLASSES = 90
data1 = {}

detection_sess = tf.Session()
with detection_sess.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:   # 读取pb模型
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

		image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
		detection_boxes = tf.get_default_graph().get_tensor_by_name('detection_boxes:0')
		detection_scores = tf.get_default_graph().get_tensor_by_name('detection_scores:0')
		detection_classes = tf.get_default_graph().get_tensor_by_name('detection_classes:0')
		num_detections = tf.get_default_graph().get_tensor_by_name('num_detections:0')

# detection_graph = tf.Graph()
# with detection_graph.as_default():
# 	od_graph_def = tf.GraphDef()
# 	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
# 		od_graph_def.ParseFromString(fid.read())
# 		tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# with detection_graph.as_default():
# 	with tf.Session(graph=detection_graph) as sess:
# 		image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# 		detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# 		detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
# 		detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# 		num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# from flask import Flask, render_template, Response
# import cv2


class VideoCamera(object):
	def __init__(self):
		# 通过opencv获取实时视频流
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		# global bottle_count
		# success, image = self.video.read()
		# 处理视频帧


		ret, image_np = self.video.read()
		image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
		image_np_expanded = np.expand_dims(image_np, axis=0)
		# 前向传播
		(boxes, scores, classes, num) = detection_sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_np_expanded})
		image, bottle_count = vis_util.visualize_boxes_and_labels_on_image_array(image_np,
																				 np.squeeze(boxes),
																				 np.squeeze(classes).astype(
																					 np.int32),
																				 np.squeeze(scores),
																				 category_index,
																				 use_normalized_coordinates=True,
																				 line_thickness=8)
		ret, jpeg = cv2.imencode('.jpg', image_np)
		with open('data1.txt', 'wt') as f:        # 将余量数据保存到txt
			f.write(str(bottle_count))
		return jpeg.tobytes()

# app = Flask(__name__, static_folder='./static')
app = Flask(__name__)


@app.route('/')  # 主页
def index():
	# 返回index.html模板
	return render_template('index.html')


def gen(camera):
	while True:
		frame = camera.get_frame()
		# 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')  # 返回视频流响应
def video_feed():
	return Response(gen(VideoCamera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')

# 开发板获取图片
@app.route('/syn_image', methods=["GET","POST"])
def syn_image():
	# upload_file = request.files['file']
	res = request.json
	frame = eval(res["image"].decode("base64"))
	frame = np.array(frame, dtype=np.uint8)
	old_file_name = "image.jpg"
	app.logger.info("获取一张图片")
	cv2.imwrite(old_file_name, frame)
	# if upload_file:
	# 	# file_path = os.path.join()
	# 	upload_file.save(old_file_name)
	# 	app.logger.info("获取到一张图片")

# 监控平台获取数据
@app.route('/machine_1_handler', methods=["GET","POST"])
def machine_1_handler():
	with open('data1.txt', 'rt') as f:     # 获取当前余量数据
		data1["aa"] = f.read()
	# xxx += 1
	# data1["aa"] = str(xxx)
	return json.dumps(data1)
	# SURPLUS_1 = request.args.get('a')
	# data1["aa"] = str(bottle_count)
from ftpdownload import MyFTP
# 小程序端获取数据
@app.route('/remainBottle', methods=["POST","GET"])
def remainBottle():
	my_ftp = MyFTP("192.168.0.101")
	my_ftp.login("root", "newland000997")
	# 下载单个文件
	my_ftp.download_file("F:/qqdownload/fanshu/static/0001.jpg", "aa/camera/0001.jpg")
	my_ftp.close()
	current_dir = os.path.dirname(os.path.abspath(__file__))
	img_path = os.path.join(current_dir, "static/0001.jpg")
	image_np = cv2.imread(img_path,1)
	image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
	image_np_expanded = np.expand_dims(image_np, axis=0)
	# 前向传播
	(boxes, scores, classes, num) = detection_sess.run(
		[detection_boxes, detection_scores, detection_classes, num_detections],
		feed_dict={image_tensor: image_np_expanded})
	image, bottle_count = vis_util.visualize_boxes_and_labels_on_image_array(image_np,
																			 np.squeeze(boxes),
																			 np.squeeze(classes).astype(
																				 np.int32),
																			 np.squeeze(scores),
																			 category_index,
																			 use_normalized_coordinates=True,
																			 line_thickness=8)
	ret, jpeg = cv2.imencode('.jpg', image_np)
	with open('data1.txt', 'wt') as f:  # 将余量数据保存到txt
		f.write(str(bottle_count))

	# totalBottle = 6
	# money = request.files['content']

	# with open('data1.txt') as f:
	# 	numRemain = f.read()        # 获取当前余量数据
	# 	app.logger.info("*******还剩%s瓶饮料 ******" % numRemain)

	# return numRemain
	return str(bottle_count)

if __name__ == '__main__':
	app.run(host='127.0.0.1', debug=True, port=8000)

