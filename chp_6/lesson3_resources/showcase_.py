import streamlit as st
import pandas as pd
import os,random

from width_control import *


#Configurations
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon=":shark:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

select_block_container_style()


#Start page
st.markdown("# My First Application :wave:")
st.write("This is my first ever application with Streamlit!")

#Gallery
display = st.empty()
display.image("onsen.jpg","My idea vacation spot!",use_column_width=True)

st.markdown("<br>",unsafe_allow_html=True)

#Control area
st.markdown("### Controls")

#Read images
images = os.listdir("images")
images = ['images/' + i for i in images]
images.sort(reverse=False)


#Add image to folder
new_image_url = st.text_input("Insert image url here")
if new_image_url is not "":
    images.append(new_image_url)
# images.append("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBEkXPhuutNfjl8wzLuIqqxuA9jfljxNz1tA&usqp=CAU")

#Create slider
idx = st.slider("Image Selector",0,len(images)-1)

#Update display
display.image(images[idx],use_column_width = True)

#Show variable
if st.button("Check Images Var"):
    images



