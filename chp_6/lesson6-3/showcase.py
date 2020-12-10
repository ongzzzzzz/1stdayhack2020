import streamlit as st
import os

from width_control import *

st.set_page_config(
    page_title="appy thingy",
    page_icon=":apple:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
select_block_container_style()

st.markdown("# hello my guys and girls and gays :wave:")
st.write("this is my first ever gallery viewer thingy!!!")



images = os.listdir('images')
images.sort()
images = ['images/'+img for img in images]


display = st.empty()
display.image('onsen.jpg', use_column_width=True)


st.markdown('### Control Panel')

url = st.text_input('Insert img URL here to add')
if url != '':
    images.append(url)

value = st.slider('Image to View', 0, len(images)-1)

display.image(images[value], use_column_width=True)


if st.button('Display Image List'):
    images