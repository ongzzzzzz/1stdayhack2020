import streamlit as st
import os, shutil

from PIL import Image
from photostore import PhotoStore as PS
from width_control import *

st.set_page_config(
    page_title="PS (PhotoStore)",
    page_icon=":camera:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
select_block_container_style()


# -------------------- Helpers --------------------

if not os.path.isdir('temp_images'):
    os.mkdir('temp_images')

if not os.path.isfile("temp_status.txt"):
    with open("temp_status.txt","w+") as file_: #w+ means to write and if the file does not exist, make one
        temp_status = 0 
        file_.write(str(temp_status)) #only accepts str as input to write
else:
    with open("temp_status.txt","r") as file_: #r means read
        temp_status = int(file_.read()) #read and cast as integer

def save_temp(temp_status,ps):
    """
    Simple function to save temp images. Called repetitively.
    """
    temp_status += 1
    img_name = '{}.jpg'.format(str(temp_status))
    ps.save_image("temp_images/{}".format(img_name))

    #Update temp_status.txt
    with open("temp_status.txt","w") as file_: #w means to write only
        file_.write(str(temp_status)) #only accepts str as input to write


    return temp_status


# -------------------- Header --------------------
st.header('Welcome to PhotoStore!')
st.info('**Note**: this is not Photoshop.')
st.markdown("""This is a Python-Streamlit App that does stuff to your images!
            Insert your own :camera: and give it a go!""")


# -------------------- Upload --------------------

st.markdown('<hr>', unsafe_allow_html=True)
st.subheader('Provide a picture to begin!')

# define image first
img = None

uploaded_file = st.file_uploader('Alternatively, upload a file.')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.success('Uploaded!')

    img_name = '{}.jpg'.format(str(temp_status))
    img.save("temp_images/{}".format(img_name))


if temp_status > 0:
    img = Image.open('temp_images/{}.jpg'.format(str(temp_status)))

# -------------------- Image Display --------------------
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader('~~Main Display~~ Workspace!')

main_display = st.empty()
use_col_width = False

if img:
    main_display.image(img, use_column_width=use_col_width)


# -------------------- Editing --------------------
st.subheader('Input Independent Editing Controls')

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
        img = ps.flip_image('vertical')
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row1_col2:
    #Flip vertical
    if st.button("Flip Horizontal"):

        #Perform action and update display
        img = ps.flip_image('horizontal')
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row1_col3:
    #Resize up, fixed proportions
    if st.button("Resize Up (+10%)"):

        #Perform action and update display
        img = ps.resize_image_uniform(1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row1_col4:
    #Resize down, fixed proportions
    if st.button("Resize Down (-10%)"):

        #Perform action and update display
        img = ps.resize_image_uniform(0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
#Row 2
with row2_col1:
    #Saturation up
    if st.button("Saturation Up (+10%)"):

        #Perform action and update display
        img = ps.change_saturation(1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row2_col2:
    #Saturation down
    if st.button("Saturation Down (-10%)"):

        #Perform action and update display
        img = ps.change_saturation(0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row2_col3:
    #Contrast up
    if st.button("Contrast Up (+10%)"):

        #Perform action and update display
        img = ps.change_contrast(1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row2_col4:
    #Contrast down
    if st.button("Contrast Down (-10%)"):

        #Perform action and update display
        img = ps.change_contrast(0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
#Row 3
with row3_col1:
    #Brightness up
    if st.button("Brightness Up (+10%)"):

        #Perform action and update display
        img = ps.change_brightness(1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row3_col2:
    #Brightness down
    if st.button("Brightness Down (-10%)"):

        #Perform action and update display
        img = ps.change_brightness(0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row3_col3:
    #Sharpness up
    if st.button("Sharpness Up (+10%)"):

        #Perform action and update display
        img = ps.change_sharpness(1.1)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row3_col4:
    #Sharpness down
    if st.button("Sharpness Down (-10%)"):

        #Perform action and update display
        img = ps.change_sharpness(0.9)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
#Row 4
with row4_col1:
    #Rotate counter-clockwise
    if st.button("Rotate (+10 degrees)"):

        #Perform action and update display
        img = ps.rotate_image(10)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row4_col2:
    #Rotate clockwise
    if st.button("Rotate (-10 degrees)"):

        #Perform action and update display
        img = ps.rotate_image(-10)
        main_display.image(img, use_column_width=use_col_width) 

        #Update temp_status and save image
        temp_status = save_temp(temp_status,ps)
with row4_col3:
    #Undo
    if st.button("Undo"):

        if temp_status == 0:
            st.warning('nothing undoable!!')
        else:
            temp_status -= 1
            #Update temp_status.txt
            with open("temp_status.txt","w") as file_: #w means to write only
                file_.write(str(temp_status)) #only accepts str as input to write

        # st.error("Not implemented yet! Your tutorial to do so!")
        #Hint; temp_status may help ;)
with row4_col4:
    #Redo
    if st.button("Redo"):
        
        if temp_status == len(os.listdir('temp_images'))-1:
            st.warning('nothing redoable!!')
        else:
            temp_status += 1
            #Update temp_status.txt
            with open("temp_status.txt","w") as file_: #w means to write only
                file_.write(str(temp_status)) #only accepts str as input to write

        # st.error("Not implemented yet! Your tutorial to do so!")
        #Hint; temp_status may help ;)
#Row 5
with row5_col1:
    #Save Image
    if st.button("Save Image"):

        #Perform action and update display
        ps.save_image("your_edited_image.jpg")
        st.success("Saved to {}".format(os.path.abspath('./')))

        #No temp_status update for this one
with row5_col2:
    #Reset Image
    if st.button("Reset Image"):

        first_temp_img = Image.open("temp_images/0.jpg")

        # add this to the history
        temp_status += 1
        first_temp_img.save("temp_images/{}.jpg".format(str(temp_status)))

        #Update temp_status.txt
        with open("temp_status.txt","w") as file_: #w means to write only
            file_.write(str(temp_status)) #only accepts str as input to write


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
    img = ps.crop_image(crop_coords)
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
    text_coords = text_coords.split(",") #Split string input into different elements by ',' 
    text_coords = list(map(int,text_coords)) 

    print(text)
    #Crop
    img = ps.put_text(text, text_coords, 'white', 69)
    main_display.image(img, use_column_width=use_col_width) 

    #Update temp_status and save image
    temp_status = save_temp(temp_status,ps)

    # st.error("Not implemented yet! Your tutorial to do so!")


# -------------------- End Section --------------------
#Section off with line
st.markdown('<hr>', unsafe_allow_html=True)
st.subheader("Finished? Click to Clear!")

#If already exist, clear it of previous work
if st.button("Clear Workspace"):
    shutil.rmtree("temp_images")
    os.remove('temp_status.txt')
