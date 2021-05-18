import os
import cv2
import numpy as np
from natsort import natsorted

base = "processed_images/"
base2 = "processed_images2/"

folders = natsorted(os.listdir(base))

image_text_file=open("images.txt","w")
  
for fo in folders:
	files = natsorted(os.listdir(base+fo+'/'))
	if not os.path.isdir(base2+fo):
		os.mkdir(base2+fo)

	for f in files:
		images_path=[str(base2+fo+ "/" +f.split('.')[0] + "_1" + ".jpg"),
		str(base2+fo+ "/" +f.split('.')[0] + "_2" + ".jpg"),
		str(base2+fo+ "/" +f.split('.')[0] + "_3" + ".jpg")]
		D = cv2.imread(base+fo+'/'+f)
		cv2.imwrite(images_path[0],D[:,0:400,:])
		cv2.imwrite(images_path[1],D[:,200:600,:])
		cv2.imwrite(images_path[2],D[:,400:800,:])

		for j in range(0,len(images_path)):
			image_text_file.write("../NVIDIA_AICITY/"+images_path[j])
			image_text_file.write('\n')
