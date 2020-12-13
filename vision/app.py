import streamlit as st

# from FDK.src.core.detect import Detector
# from FDK.src.core.utils import utils

from PIL import Image
import os, shutil
import matplotlib.pyplot as plt
import numpy

from width_control import *

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from torch.autograd import Variable

st.set_page_config(
  page_title="Fruiesh",
  page_icon=":seedling:",
  layout="centered",
  initial_sidebar_state="collapsed",
)
select_block_container_style()

# -------------------- Header --------------------

st.markdown('## upload pic of apple/orange/banana to detect fruit spoilt or not')
st.markdown('### 🍎🍊🍌')

# -------------------- Helper Functions --------------------

data_dir = 'data/dataset/test'
test_transforms = transforms.Compose([transforms.Resize((224, 224)),
                                      transforms.ToTensor(),
                                    ])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load('fruitmodel.pth')
model.eval()

@st.cache
def predict_image(image):
  image_tensor = test_transforms(image).float()
  image_tensor = image_tensor.unsqueeze_(0)
  input = Variable(image_tensor)
  input = input.to(device)
  output = model(input)
  index = output.data.cpu().numpy().argmax()
  return index

@st.cache
def get_random_images(num):
  data = datasets.ImageFolder(data_dir, transform=test_transforms)
  classes = data.classes
  indices = list(range(len(data)))
  np.random.shuffle(indices)
  idx = indices[:num]
  from torch.utils.data.sampler import SubsetRandomSampler
  sampler = SubsetRandomSampler(idx)
  loader = torch.utils.data.DataLoader(data, 
              sampler=sampler, batch_size=num)
  dataiter = iter(loader)
  images, labels = dataiter.next()
  return images, labels

# -------------------- Display --------------------
# -------------------- Upload --------------------

# if not os.path.isdir('temp'):
#   os.mkdir('temp')

img = None
uploaded_file = st.file_uploader('')

if uploaded_file is not None:
  img = Image.open(uploaded_file)
  st.success('Uploaded!')

img_display = st.empty()
col_width = False
if img:
  classes = datasets.ImageFolder(data_dir, transform=test_transforms).classes
  
  pred = classes[predict_image(img)]
  img_display.image(img, use_column_width=col_width)
  st.markdown('# {}'.format(pred))


# if st.button("Process Image!"):
#   det = Detector(model="COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml", device='cuda')
#   # convert to cv2 img
#   img_cv = utils.pil_to_cv2(img)
#   # predict
#   output = det.predict(img_cv)
#   out_img = det.visualize(img_cv, output, figsize=(18,18))
#   # convert back to PIL for streamlit
#   img = Image.fromarray(out_img)

#   print('done!')

#   temp_stat += 1
#   img.save('temp/{}.jpg'.format(str(temp_stat)))

#   main_display.image(img, use_column_width=col_width)

# -------------------- Clear --------------------
# if st.button("Clear Workspace"):
#   shutil.rmtree("temp")

