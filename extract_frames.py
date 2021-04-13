import cv2
import os
import sys
import glob
import tqdm
from pathlib import Path
from natsort import natsorted
import numpy as np
import json
#video_name = sys.argv[1]


def get_video_names():
  video_names = []
  
  with open('dataset.json', 'r') as f:
    data = json.load(f)

  
  for video in data['videos']:
    video_names.append(video['name'])

  return video_names  


ori_images_txt = open("ori_images.txt","w")
root = "/content/gdrive/Shareddrives/UASD Fondocyt Proyecto 911/Datasets/AI city challenge/AIC20_track4/test-data"
dest_dir = "ori_images/"
video_names=get_video_names()
print("caputure videos")
for video_name in tqdm.tqdm(video_names):
    file_name = video_name
    folder_name = dest_dir+file_name.split('.')[0]
    os.makedirs(folder_name,exist_ok=True)
   
    vc = cv2.VideoCapture(root+'/'+video_name)
    
    c = 1
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    timeF = int(sys.argv[1])
    

    while rval: 
        rval, frame = vc.read()
        pic_path = folder_name+'/'
        
       
        if (c % timeF == 0 and rval): 
            cv2.imwrite(pic_path + str(c) + '.jpg', frame)
            ori_images_txt.write('/content/gdrive/MyDrive/Colab Notebooks'
            +'/NVIDIA_AICITY/'+pic_path+str(c)+'.jpg')
            ori_images_txt.write('\n')

        c = c + 1
        cv2.waitKey(1)
    vc.release()

dest_dir_processed = "processed_images/"

if not os.path.isdir(dest_dir_processed):
    os.mkdir(dest_dir_processed)
print("average images")




for vn in video_names:
    video_name = vn.split('.')[0]
    path_file_number=glob.glob(os.path.join(dest_dir,video_name,'*.jpg')) 
    internal_frame = 4
    start_frame = 100
   
    nums_frames = len(path_file_number)
    alpha=0.1
    Path(dest_dir_processed+video_name).mkdir(exist_ok=True)

    for j in range(4,5):
        internal_frame = 100
        num_pic = int(nums_frames)
        former_im = cv2.imread(dest_dir+video_name+"/100.jpg")
        
        img = cv2.imread(os.path.join(dest_dir,video_name,str(start_frame)+'.jpg'))
        for i in range(num_pic):
            # print(os.path.join(dest_dir,video_name,str(start_frame)+'.jpg'))
            # print(os.path.join(dest_dir,video_name,str(i*internal_frame+start_frame)+'.jpg'))
            now_im = cv2.imread(os.path.join(dest_dir,video_name,str(i*internal_frame+start_frame)+'.jpg'))
            if now_im is not None:
              if np.mean(np.abs(now_im-former_im))>5:
                  img = img*(1-alpha)+now_im*alpha
                  cv2.imwrite(dest_dir_processed+video_name+'/'+str(i*internal_frame+start_frame)
                        +'_'+str(j)+'.jpg',img)
              else:
                  cv2.imwrite(dest_dir_processed+video_name+'/'+str(i*internal_frame+start_frame)
                        +'_'+str(j)+'.jpg',img*0)
              former_im = now_im

