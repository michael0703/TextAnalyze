
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import glob
from keras.datasets import mnist
from keras.utils import np_utils as kutil
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Conv2D, Flatten, MaxPooling2D
from keras.layers import Conv3D,MaxPooling3D
# from matplotlib import pyplot as plt
import tensorflow as tf
import os 

import h5py
from keras.models import load_model
# In[2]:


# cut_width = 50
# cut_height = 400
# area = cut_width * cut_height
# empty_img = area * 255


# # In[3]:

# # img_list = ["./d10k/d10k_p002.png", "./d10k/d10k_p003.png"]
# img_list = glob.glob("./d10k/*")
# print(img_list)
# temp_img = "./d10k/d10k_p002.png"
# src = cv2.imread(temp_img)

# width, height, rgb = np.shape(src)

# # width, height, rgb


# # In[4]:


# cut_numw = int(np.floor(width/cut_width))
# cut_numh = int(np.floor(height/cut_height))

# STI = []

# # cut_numw, cut_numh


# # In[5]:


# gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# # gray[1:3, 2:3]


# # In[6]:


# for img in img_list:
# 	print(img)
# 	src = cv2.imread(img)
# 	gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# 	for j in range(cut_numw):
# 		for k in range(cut_numh):
# 			cuttemp = gray[cut_width * j: cut_width * (j+1), cut_height * k: cut_height * (k+1)]
# 			x = np.matrix(cuttemp)
# 			if x.sum == empty_img:
# 				pass
# 			else:
# 				STI.append(cuttemp)
				
# 		if k == cut_numh - 1:
# 			cuttemp = gray[cut_width * j: cut_width * (j+1), height-cut_height:height]
# 			x = np.matrix(cuttemp)
# 			if x.sum == empty_img:
# 				pass
# 			else:
# 				STI.append(cuttemp)
			
		
# print(STI[0].shape)
# print(len(STI))
# print(np.shape(STI))


# # In[8]:



# # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# # In[56]:
# (page,width,length)=np.shape(STI)
# x_test = np.array(STI).reshape(page,width,length,1).astype('float32')
# # normalization: mean=0, std=1

# for i in range(len(x_test)):
# 	x=x_test[i]
# 	m=x.mean()
# 	s=x.std()
# 	x_test[i]=(x-m)/s



# model = load_model('my_model.h5')
# # tf.__version__
# # tf.__path__
# # print(np.shape(STI))
# y_pred = model.predict(x_test)
# # print(y_pred)
# for row in y_pred:
# 	print(row)

# In[57]:

class ImgProcessor():

	def __init__(self, model):

		# self.model = load_model(model_path)
		self.model = model
		self.STI = []
		self.x_test = None


	def PreProcessImg(self, imgs):

		cut_width = 25
		cut_height = 800
		area = cut_width * cut_height
		empty_img = area * 255

		
		#first process imgs[0] to get basic info
		width, height, rgb = np.shape(imgs[0])

		cut_numw = int(np.floor(width/cut_width))
		cut_numh = int(np.floor(height/cut_height))


		for img in imgs:

			src = img
			gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

			for j in range(cut_numw):
				for k in range(cut_numh):
					cuttemp = gray[cut_width * j: cut_width * (j+1), cut_height * k: cut_height * (k+1)]
					x = np.matrix(cuttemp)
					if x.sum() == empty_img:
						pass
					else:
						self.STI.append(cuttemp)
				
					if k == cut_numh - 1:
						cuttemp = gray[cut_width * j: cut_width * (j+1), height-cut_height:height]
						x = np.matrix(cuttemp)
						if x.sum() == empty_img:
							pass
						else:
							self.STI.append(cuttemp)

		(page,width,length)=np.shape(self.STI)
		self.x_test = np.array(self.STI).reshape(page,width,length,1).astype('float32')

		for i in range(len(self.x_test)):
			x=self.x_test[i]
			m=x.mean()
			s=x.std()
			self.x_test[i]=(x-m)/s



	def GetResult(self):

		return self.model.predict(self.x_test)











