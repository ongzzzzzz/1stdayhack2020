import streamlit as st

from FDK.src.core.detect import Detector
from FDK.src.core.super_res import SuperReser
from FDK.src.core.utils import utils

from PIL import Image

import os
import matplotlib.pyplot as plt
import numpy

from width_control import *

st.set_page_config(
    page_title="First ML App",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
select_block_container_style()

