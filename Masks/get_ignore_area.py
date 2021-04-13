import skimage
from skimage.measure import label 
from scipy.ndimage.filters import gaussian_filter
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json


count_thred = 0.02
min_area = 500
gass_sigma = 2
score_thred = 0.1

def get_video_names():
  video_names = []
  
  with open('../dataset.json', 'r') as f:
    data = json.load(f)

  
  for video in data['videos']:
    video_names.append(video['name'].split('.')[0])

  return video_names


#video_names = read_video_file_names("/content/gdrive/Shared drives/UASD Fondocyt Proyecto 911/Datasets/AI city challenge/AIC20_track1/Dataset_A/",'list_video_id.txt')
video_names=get_video_names()

for video_name in video_names:
	dt_results_fbf = {}
	with open("%s.txt"%(video_name),'r') as f:
		for line in f:
			line = line.rstrip()
			word = line.split(',')
			frame = int(word[0])
			x1 = int(float(word[2]))
			y1 = int(float(word[3]))
			tmp_w = int(float(word[4]))
			tmp_h = int(float(word[5]))
			score = float(word[6])
			if frame not in dt_results_fbf:
				dt_results_fbf[frame]=[]
			if score > score_thred :
				dt_results_fbf[frame].append([x1,y1,x1+tmp_w,y1+tmp_h,score])

	# im = cv2.imread("data/AIC_Track3/ori_images/%s/1.jpg"%video_name)

	h = 410
	w = 800
	c = 3
	mat = np.zeros((h,w))
	# print(len(dt_results_fbf))
	for frame in dt_results_fbf:
		if frame <18000:
			tmp_score = np.zeros((h,w))

			for box in dt_results_fbf[frame]:
				score = box[4]
				tmp_score[int(float(box[1])):int(float(box[3])),int(float(box[0])):int(float(box[2]))] = np.maximum(score,tmp_score[int(float(box[1])):int(float(box[3])),int(float(box[0])):int(float(box[2]))])

			mat = mat+tmp_score
	# plt.imshow(mat)
	# plt.show()
	mat = mat-np.min(mat)
	mat = mat/np.max(mat)
	mask= mat>count_thred
	mask = label(mask, connectivity = 1)
	num = np.max(mask)
	print(num)
	for i in range(1,int(num+1)):
		if np.sum(mask==i)<min_area:
			mask[mask==i]=0     
	mask = mask>0
	mask = mask.astype(float)
	k = gaussian_filter(mask,gass_sigma)
	mask = k>count_thred
	np.save("Mas/%s.npy"%str(video_name),mask)
