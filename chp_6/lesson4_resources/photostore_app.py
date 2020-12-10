## Import packages
import streamlit as st
import os, shutil

from PIL import Image
from photostore import PhotoStore as PS
from width_control import * 


### --------------------- Flow Outline ----------------------------------
# Implementing 20 functions, 2 with inputs and 18 without.



### --------------------- Config Section ----------------------------------

## Setup page config
st.set_page_config(
    page_title="PhotoStore - Definitely not PhotoShop!",
    page_icon=":camera:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

## Add width control
select_block_container_style()


## Setup temp working folder for state saving
#Create a new one if not exist
if not os.path.isdir("temp_images"):
    os.mkdir("temp_images")



# ------------- NEW STUFF FOR ANSWER HERE ------------- 

#In order to do undo / redo, we will have to change how temp_status is calculated! 
#No longer just setting temp_status = len(os.listdir("temp_images")), we a better way that can be manipulated
#We unfortunately can't just keep it in a variable in memory because streamlit restarts (and flushes the variables in memory) on button clicks!

#Therefore, we will have to reate new text file that writes the latest temp_status value in it
if not os.path.isfile("temp_status.txt"):
    
    with open("temp_status.txt","w+") as file_: #w+ means to write and if the file does not exist, make one
        temp_status = 0 
        file_.write(str(temp_status)) #only accepts str as input to write


else:

    with open("temp_status.txt","r") as file_: #r means read
        temp_status = int(file_.read()) #read and cast as integer
    

## We will also have to change how save_temp works for a bit
def save_temp(temp_status,ps):
    """
    Simple function to save temp images. Called repetitively.
    """
    temp_status += 1
    img_name = '{}.jpg'.format(str(temp_status))
    ps.save_image(img,"temp_images/{}".format(img_name))

    #Update temp_status.txt
    with open("temp_status.txt","w") as file_: #w means to write only
        file_.write(str(temp_status)) #only accepts str as input to write


    return temp_status
    

# ------------- NEW STUFF FOR ANSWER HERE ------------- 



### --------------------- Header Section ----------------------------------
#Create header
st.header("Welcome to PhotoStore")
st.info("Insert your info and app explanation here :smile:")
st.markdown("""This is a simple python streamlit app that does simple image manipulation.
            Insert your own image :camera: below to give it a go!""")

col1, col2, col3 = st.beta_columns(3)
with col1:
   st.image("https://static.streamlit.io/examples/cat.jpg", use_column_width=True)

with col2:
   st.image("https://static.streamlit.io/examples/dog.jpg", use_column_width=True)

with col3:
   st.image("https://images.unsplash.com/photo-1516467508483-a7212febe31a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80", use_column_width=True)



### --------------------- Upload Section ----------------------------------
#Section off with line
st.markdown('<hr>', unsafe_allow_html=True)

#Create subheader
st.subheader("Provide a picture to begin!")

#Define var first, otherwise get error of var "img" is not defined!
img = None

#Provide picture by upload
uploaded_file = st.file_uploader("Alternatively upload a file")
if uploaded_file is not None and temp_status < 1:
    img = Image.open(uploaded_file)
    st.success("Uploaded.")


    # ------------- NEW STUFF FOR ANSWER HERE ------------- 

    #Let's save a copy of the raw image in temp_images for temp_status of 0; exactly like PhotoStore in Chapter 3's Tutorial
    img_name = '{}.jpg'.format(str(temp_status))
    img.save("temp_images/{}".format(img_name))

    # ------------- NEW STUFF FOR ANSWER HERE ------------- 


#Override above with temp_status dictated image
if temp_status > 0:
    img = Image.open("temp_images/{}.jpg".format(str(temp_status)))



### --------------------- Display Section ----------------------------------
#Section off with line
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("Main Display")

#Create empty placeholder
main_display = st.empty()
use_col_width = False 


#Display image only if not None, otherwise error!
if img:
    main_display.image(img, use_column_width=use_col_width)


### --------------------- Editing Section ----------------------------------
st.subheader("Input Independent Editing Controls")

#Instantiate PS class
ps = PS(img)


## Create layout!
#4 buttons per row; currently have 18 input-less functions (button based)
#Total of 5 rows
row1_col1, row1_col2, row1_col3, row1_col4 = st.beta_columns(4)
row2_col1, row2_col2, row2_col3, row2_col4 = st.beta_columns(4)
row3_col1, row3_col2, row3_col3, row3_col4 = st.beta_columns(4)
row4_col1, row4_col2, row4_col3, row4_col4 = st.beta_columns(4)
row5_col1, row5_col2 = st.beta_columns(2)



#Row 1
with row1_col1:
    #Flip vertical
    if st.button("Flip Vertical"):

        #Perform action and update display
        img = ps.flip_image(img,'vertical')
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row1_col2:
    #Flip vertical
    if st.button("Flip Horizontal"):

        #Perform action and update display
        img = ps.flip_image(img,'horizontal')
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row1_col3:
    #Resize up, fixed proportions
    if st.button("Resize Up (+10%)"):

        #Perform action and update display
        img = ps.resize_image_uniform(img,1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row1_col4:
    #Resize down, fixed proportions
    if st.button("Resize Down (-10%)"):

        #Perform action and update display
        img = ps.resize_image_uniform(img,0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)



#Row 2
with row2_col1:
    #Saturation up
    if st.button("Saturation Up (+10%)"):

        #Perform action and update display
        img = ps.change_saturation(img,1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row2_col2:
    #Saturation down
    if st.button("Saturation Down (-10%)"):

        #Perform action and update display
        img = ps.change_saturation(img,0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row2_col3:
    #Contrast up
    if st.button("Contrast Up (+10%)"):

        #Perform action and update display
        img = ps.change_contrast(img,1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row2_col4:
    #Contrast down
    if st.button("Contrast Down (-10%)"):

        #Perform action and update display
        img = ps.change_contrast(img,0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)



#Row 3
with row3_col1:
    #Brightness up
    if st.button("Brightness Up (+10%)"):

        #Perform action and update display
        img = ps.change_brightness(img,1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row3_col2:
    #Brightness down
    if st.button("Brightness Down (-10%)"):

        #Perform action and update display
        img = ps.change_brightness(img,0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row3_col3:
    #Sharpness up
    if st.button("Sharpness Up (+10%)"):

        #Perform action and update display
        img = ps.change_sharpness(img,1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row3_col4:
    #Sharpness down
    if st.button("Sharpness Down (-10%)"):

        #Perform action and update display
        img = ps.change_sharpness(img,0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)



#Row 4
with row4_col1:
    #Rotate counter-clockwise
    if st.button("Rotate (+10 degrees)"):

        #Perform action and update display
        img = ps.rotate_image(img,10)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


with row4_col2:
    #Rotate clockwise
    if st.button("Rotate (-10 degrees)"):

        #Perform action and update display
        img = ps.rotate_image(img,-10)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)


# ------------- NEW STUFF FOR ANSWER HERE ------------- 

with row4_col3:
    #Undo
    if st.button("Undo"):
        
        #Very simply just move subtract temp_status
        #Check first if we're at bottom (e.g. 0)
        if temp_status == 0:
            st.warning("No more steps to undo!") #do nothing

        else:
            temp_status -= 1 #subtract

            #Update temp_status.txt
            with open("temp_status.txt","w") as file_: #w means to write only
                file_.write(str(temp_status)) #only accepts str as input to write


with row4_col4:
    #Redo
    if st.button("Redo"):

        #Very simply just move add temp_status
        #Check first if we're at top (e.g. len(os.listdir(temp_images)) - 1)
        if temp_status == len(os.listdir("temp_images")) - 1:
            st.warning("No more steps to redo!")

        else:
            temp_status += 1 #add

            #Update temp_status.txt
            with open("temp_status.txt","w") as file_: #w means to write only
                file_.write(str(temp_status)) #only accepts str as input to write


# ------------- NEW STUFF FOR ANSWER HERE ------------- 


#Row 5
with row5_col1:
    #Save Image
    if st.button("Save Image"):

        #Perform action and update display
        ps.save_image(img,"your_edited_image.jpg")
        st.success("Saved to {}".format(os.path.abspath('./')))

        #No temp_status update for this one



# ------------- NEW STUFF FOR ANSWER HERE ------------- 

with row5_col2:
    #Reset Image
    if st.button("Reset Image"):
        
        #For reset, let's preserve this history up to this point thus far.
        #Let's just make the next image (e.g. latest img in temp_images) be the raw image itself
        curr_img = Image.open("temp_images/0.jpg")

        #Update temp_status and save image as usual
        temp_status += 1
        img_name = '{}.jpg'.format(str(temp_status))
        curr_img.save("temp_images/{}".format(img_name))

        #Update temp_status.txt
        with open("temp_status.txt","w") as file_: #w means to write only
            file_.write(str(temp_status)) #only accepts str as input to write


# ------------- NEW STUFF FOR ANSWER HERE ------------- 


## Input-dependent function: Cropping
st.subheader("Crop Image Controls")

#Get coordinates
crop_coords = st.text_input("Crop Coordinates")


#Crop
if crop_coords:

    #Turn input into a list of integers
    crop_coords = crop_coords.split(",") #Split string input into different elements by ',' 
    crop_coords = list(map(int,crop_coords)) 

    #Crop
    img = ps.crop_image(img,crop_coords)
    main_display.image(img, use_column_width=use_col_width) 

    #Update temp_status and save image
    temp_status = save_temp(temp_status,ps)



## Input-dependent function: Put Text
st.subheader("Text Insert Controls")

#Get text and coordinates
text = st.text_input("Text to Insert")
text_coords = st.text_input("Text Coordinates")

#Put Text
if text_coords and text:
    st.error("Not implemented yet! Your tutorial to do so!")



### --------------------- End Section ----------------------------------
#Section off with line
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("Finished? Click to Clear!")

#If already exist, clear it of previous work
if st.button("Clear Workspace"):
    shutil.rmtree("temp_images")
