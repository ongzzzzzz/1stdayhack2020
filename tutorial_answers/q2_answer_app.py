## Import packages
import streamlit as st
import os, shutil, cv2
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from PIL import Image
from width_control import * 
from detectron2_coco2017_labels import thing_classes,thing_colors,thing_dataset_id_to_contiguous_id

from q2_custom_code import custom_Detector as Detector
from FDK.src.core.depth import DepthEst
from FDK.src.core.utils import utils




### --------------------- Config Section ----------------------------------

## Setup page config
st.set_page_config(
    page_title="NAVI - Autonomous Hazardous Environment Helper",
    page_icon=":robot_face:",
    layout="centered"
)

#Set width adjuster
select_block_container_style()

## Instantiate detector
detector = Detector(name="MyDet",device="cpu")

## Instantiate depth estimator
depth = DepthEst(name="DeptEstimator",device="cuda")


#Helper function
@st.cache
def read_images(img_path):

    #Create placeholder
    images = []

    #List out images
    dir_imgs = os.listdir(img_path)
    dir_imgs.sort()

    #Read and save into memory
    for i in dir_imgs:
        img_ = Image.open(img_path + '/' + i)

        #Need to convert to cv2 before saving for model requirement
        img_ = utils.pil_to_cv2(img_)
        images.append(img_)

    return images


# ---------------------- NEW STUFF FOR ANSWER HERE ------------------------
classes_to_include = ["person","backpack","handbag"]


### --------------------- Header Section ----------------------------------
#Create header
st.header("Welcome to the NAVI-Core Demo")
st.markdown("""
               This is a streamlit app to demonstrate the core perception capability of 
               NAVI (hence NAVI-Core :gear:) in its ability to facilitate autonomous navigation
               in a crowded environment, with varying room layout. :smile:
               
               NAVI is a proposed Autonomous Hazardous Environment Helper designed to provide
               assistance or carry out specific tasks in understaffed and hazardous COVID-19 wards
               where human exposure should be kept to a minimum. NAVI is envisioned to be a stand-in
               robotic helper in order to alleviate the over-crowding of hospitals. Therefore,
               NAVI will need to be able to perceive a given crowded indoor environment - e.g. an 
               over-crowded ward - in order to navigate and carry its task effectively. :robot_face:

               NAVI relies on 2 modules
               from **1stDayKit**, namely the Detector and Depth Estimator module based on
               Detectron2 and MiDaS. With these modules NAVI will be able to generate depth maps in order 
               to estimate its distance from other objects in its environment, and detect relevant entities 
               such as patients and doctors with a single camera feed :camera:.""")


st.image("https://media-exp1.licdn.com/dms/image/C4D1BAQEZsgDO-UZ_Kg/company-background_10000/0?e=2159024400&v=beta&t=V6FGY5_iw_APSPfBaGCydwAso1f485R_UK5juLO5IRI",
        use_column_width=True,
        caption='Image taken from Diligent Robotics; Moxi.')



### --------------------- Upload Section ----------------------------------
#Section off with line
st.markdown('<hr>', unsafe_allow_html=True)

#Create subheader
st.subheader("Provide images to begin!")
st.info("Make sure you have uploaded the images onto the cloud instance first if you are on Colab!")


#Provide pictures
img_path = st.text_input("Images dir path","None")


#Create placeholder
images = []


#If it's an images directory
if img_path != "None":

    images = read_images(img_path)
    st.success("Uploaded.")

### --------------------- Display Section ----------------------------------
#Section off with line
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("Main Display")

#Create empty placeholder within proper columns
use_col_width = True 

row2_col1, row2_co12 = st.beta_columns(2)

#Detector output
with row2_col1:
    main_display_row2_col1 = st.empty()

#Depth estimator output
with row2_co12:
    main_display_row2_col2 = st.empty()

#Main raw image
with st.beta_container():
    main_display_row1_col1 = st.empty()


#Display image only if not None, otherwise error!
#Display model outputs as well; only on first image for initialisation
if img_path != "None":

        #Main raw image
        raw_display_image = utils.cv2_to_pil(images[0]) #convert back to proper format
        main_display_row2_col1.image(raw_display_image,use_column_width=use_col_width,caption="Raw",format="RGB")

        #Detector output
        detect_output = detector.predict(images[0])
        detect_output = detector.visualize(images[0], detect_output, noplot=True,classes_to_include=classes_to_include)
        detect_output = Image.fromarray(detect_output)
        main_display_row1_col1.image(detect_output,use_column_width=use_col_width,caption="Detection")

        #Depth estimator output
        depth_output = depth.predict(images[0])
        depth_output = depth_output/depth_output.max() #normalize
        depth_output = Image.fromarray(np.uint8(cm.gist_earth(depth_output)*255)).convert("RGB")
        main_display_row2_col2.image(depth_output,use_column_width=use_col_width,caption="Depth Map")



### --------------------- Editing Section ----------------------------------
st.subheader("Controls")


## Swipe frames preview
max_len = len(images) if images else 1
idx_to_run = st.slider("Preview Frame Selection",0,max_len)

if idx_to_run:
    #Main raw image
    raw_display_image = utils.cv2_to_pil(images[idx_to_run]) #convert back to proper format
    main_display_row2_col1.image(raw_display_image,use_column_width=use_col_width,caption="Raw",format="RGB")

    #Detector output
    detect_output = detector.predict(images[idx_to_run])
    detect_output = detector.visualize(images[idx_to_run], detect_output, noplot=True,classes_to_include=classes_to_include)
    detect_output = Image.fromarray(detect_output)
    main_display_row1_col1.image(detect_output,use_column_width=use_col_width,caption="Detection")

    #Depth estimator output
    depth_output = depth.predict(images[idx_to_run])
    depth_output = depth_output/depth_output.max() #normalize
    depth_output = Image.fromarray(np.uint8(cm.gist_earth(depth_output)*255)).convert("RGB")
    main_display_row2_col2.image(depth_output,use_column_width=use_col_width,caption="Depth Map")



## Frames to include
frames_bound = st.slider("Video Frames Boundary",0,len(images),(1,len(images)-1))
images_to_run = images[frames_bound[0]:frames_bound[1]]



## Class to include in detection
classes = st.multiselect("What classes to include?",thing_classes,classes_to_include)




## --------------------- End Section ----------------------------------
#Section off with line
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("Finished? Save Results and Clear Workspace!")


#Apply model on all images and save out
if st.button("Run All and Save"):

    st.info("This will create new folders in the current working dir to save.")

    #Check folder
    if not os.path.isdir("detector_output"):
        os.mkdir("detector_output")

    if not os.path.isdir("depth_output"):
        os.mkdir("depth_output")


    for idx,i in enumerate(images_to_run):

        #Detector output
        detect_output = detector.predict(i)
        detect_output = detector.visualize(i, detect_output, noplot=Tru,classes_to_include=classes_to_include)
        detect_output = Image.fromarray(detect_output)

        #Depth estimator output
        depth_output = depth.predict(i)
        depth_output = depth_output/depth_output.max() #normalize
        depth_output = Image.fromarray(np.uint8(cm.gist_earth(depth_output)*255)).convert("RGB")

        #Save
        detect_output.save("detector_output/detect_{:05d}.jpg".format(idx))
        depth_output.save("depth_output/depth_{:05d}.jpg".format(idx))


#Clean up taxing objects
if st.button("Clear Workspace"):
    del images, detector, depth
