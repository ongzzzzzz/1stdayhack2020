# ### Flow
# 1. Create page, header and main display image
# 2. Use empty for display
# 3. Use width_control
# 4. Read gallery and select with slider
# 5. Show variable with button
# 6. Add new image by url with text_input
# 7. Animated plots 



import streamlit as st
import os

from width_control import *

#Configurations
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon=":shark:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

select_block_container_style()


#Header
st.markdown("# My First Application! :poop:")
st.write("This is my first application and it's a image gallery viewer.")


#Loading images
my_images = os.listdir("images")
my_images.sort()
new_images = ['images/'+i for i in my_images]


#Display
display = st.empty()
display.image("onsen.jpg", use_column_width=True)


#Controls
st.markdown("### Control Panel")


url = st.text_input("Insert img url to add")

if url != "":
    new_images.append(url)


value = st.slider("Image to Preview",0,len(new_images)-1)
new_image_to_preview = new_images[value]

#Display new image
display.image(new_image_to_preview, use_column_width=True)

#Display variable state
if st.button("Display Variable"):
    new_images