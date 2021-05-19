# define helper functions
import json
import re
from natsort import natsorted
from google.colab import output
from ipyfilechooser import FileChooser
import os
import shutil
from google.colab import files


# use this to upload files
def upload(path):
  from google.colab import files
  uploaded = files.upload()
  os.chdir(path) 
  for name, data in uploaded.items():
    with open(path+name, 'wb') as f:
      f.write(data)
      print ('saved file', name)
  os.chdir("..")
 
# use this to download a file  
def download(path):
  from google.colab import files
  files.download(path)
 
#use this to write the videos on a json file 
def load_dataset(path):
  files = os.listdir(path)
  files = natsorted(files)
  data = {}
  data['videos']=[]
  id = 1; 
  
  for f in files:
    if f.split(".")[1]=="mp4":
    
        name = f.split(".")[0]
        
        data["videos"].append({
                'id':id,
                'name':f,
                'path':path+'/'+f
            })
        id += 1
    else:
      continue;
        
 
  with open('dataset.json','w') as json_file:
    json.dump(data,json_file)

#Choose the medium to pick up the videos
def pick_source_menu():
  
  if os.path.isdir("Data")==False:
    os.mkdir("Data")
  
  path=""
  option = input("Choose the medium to pick up the files\n"+
      "1.Use a Sample Video\n"+
      "2.My computer\n"+
      "3.Google Drive\n"+
      "4.Get out of the menu\n")
  
  if option=="1":
   load_sample_video()
  
  elif option=="2": # This option loads all videos located in the Data folder
    output.clear()
    print("Choose the videos")
    path="Data/"
    upload(path)
    load_dataset(path)

  elif option=="3": pick_up_from_google_drive() #This option picks the dataset folder from Google Drive.
  elif option=="4": 
    output.clear()
    return
      
  else:
    output.clear()
    print("Incorrect option")
    pickSource()



def pick_up_from_google_drive():
    output.clear() 
  
    file_chooser = FileChooser("/content/gdrive/MyDrive/")
    file_chooser.use_dir_icons = True

    option = input("Choose the way to pick up the files\n"+
                "1.A single video\n"+
                 "2.A dataset folder\n"+
                 "3.Get back to the main menu\n")

    if option=="1":
      output.clear()
      
      file_chooser.filter_pattern = ['*.mp4']
      file_chooser.show_only_dirs = False
    
  
      def on_selected_video(chooser):
      
        data = {}
        data["videos"]=[]

     

        id = 1
        video_name =chooser.selected_filename
        path = chooser.selected


        data["videos"].append({
           "id":id,
           "name":video_name,
           "path":path
        })
      

        with open('dataset.json','w') as json_file:
          json.dump(data,json_file)
        
        
    
      file_chooser.register_callback(on_selected_video)
      print("Choose a video")
      display(file_chooser)
   
    elif option=="2":
      file_chooser.show_only_dirs = True
     
      def on_selected_folder(chooser):
            print(chooser.selected)     
            path = chooser.selected_path     
            load_dataset(path)     
     
      file_chooser.register_callback(on_selected_folder)
      output.clear()
      
      print("Choose the dataset folder")
      display(file_chooser)

    elif option=="3": 
      output.clear()
      pick_source_menu()
    else:
        output.clear()
        print("Incorrect Option")
        pick_up_from_google_drive()  

 


#Ask to remove the past files on the data folder
def ask_clear_data_folder():
  if os.path.isdir("Data")==False:
    os.mkdir("Data")
  
  option = input("Do you want to clear Data folder ?\n"+
      "1.Yes\n"+
      "2.No\n")
  if option=="1":
    print("Removing all files in the data folder")
    shutil.rmtree("Data")
    os.mkdir("Data")
  elif option=="2":
    return
  else:
    output.clear()
    print("Incorrect option")
    ask_clear_data_folder()

def load_sample_video():
    
    data = {}
    data["videos"]=[]

    id = 1
    video_name ="video_1.mp4"
    path = "sample_video/video_1.mp4"


    data["videos"].append({
           "id":id,
           "name":video_name,
           "path":path
        })
      

    with open('dataset.json','w') as json_file:
          json.dump(data,json_file)
    
    json_file.close

