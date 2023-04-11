import os 
import shutil

def b64_images():
    base_folder = "b64_img"

    if os.path.exists(base_folder):
        shutil.rmtree(base_folder)
    
    os.mkdir(base_folder)  

def img_to_b64():
    img_path = "./img/"

    for file_path in os.listdir(img_path):
        filename = file_path.split("/")[-1]
        os.system("cat " + img_path + file_path + " | base64 > b64_img/" + filename + ".b64")

b64_images()
img_to_b64()

print("Images converted to base64")