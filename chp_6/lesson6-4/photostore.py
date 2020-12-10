from PIL import Image, ImageOps
from PIL import ImageEnhance as IE #can use alias
from PIL import ImageDraw as ID
from PIL import ImageFont as IF

class PhotoStore():
    
    def __init__(self,raw_image):
        """
        Instantiate class and store raw image in a class variable.
        
        Input:
            raw_image: Raw image to be altered.
        """
        self.raw_image = raw_image
        self.cache = []
        self.index = 0
        self.newestImage = raw_image

        self.cache.append(self.newestImage)
        
    def save_to_cache(self, image):
        self.cache.append(image)
        self.index += 1

        return

    def save_image(self,path):
        """
        Simple function to save edited image.

        Input:
            image: Image to be saved.
            path: Path to save image to.
        """
        self.newestImage.save(path)

        return
    
    
    def resize_image(self, dim):
        """
        Resize a given image according to a given dimension.

        Input:
            image: input image
            dim: size to resize image to
        """
        self.newestImage = self.newestImage.resize(dim)

        self.save_to_cache(self.newestImage)

        return self.newestImage

    def resize_image_uniform(self, multiple):
        """
        Resize a given image to a multiple of its size. Maintains aspect ratio.

        Input:
            image: input image
            multiple: value to compute resized image dimensions
        """

        #Compute size
        width,height = self.newestImage.size
        target_size = (int(width * multiple), 
                       int(height * multiple))

        self.newestImage = self.newestImage.resize(target_size)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def flip_image(self, axis='vertical'):
        """
        Flip an image around the given axis.

        Input:
            image: input image
            axis: 'horizontal' or 'vertical'. Axis to flip image around
        """

        #Set axis to flip
        if axis == 'vertical':
            axis_ = Image.FLIP_LEFT_RIGHT

        elif axis == 'horizontal':
            axis_ = Image.FLIP_TOP_BOTTOM

        else:
            raise Exception("Axis provided is invalid! Please use either 'horizontal' or 'vertical' only.")

        self.newestImage = self.newestImage.transpose(axis_)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def rotate_image(self, degree):
        """
        Rotate a given image according to a given degree.

        Input:
            image: input image
            degree: degree to rotate image to
        """

        self.newestImage = self.newestImage.rotate(degree)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def pad_image(self, size, color='black'):
        """
        Pad a given image according to a given size.

        Input:
            image: input image
            size: size of new padded image
            color: image of pads to be added
        """

        self.newestImage = ImageOps.pad(self.newestImage,size,color=color)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def crop_image(self, coordinates):
        """
        Crop a given image according to a given size.

        Input:
            image: input image
            coordinates: coordinates to crop. Need to be a list or tuple like (left, upper, right, lower).
        """

        self.newestImage = self.newestImage.crop(coordinates)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def change_saturation(self,saturation):
        """
        Change image saturation according to the saturation value.

        Input:
            image: input image
            saturation: Change image saturation level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Color(self.newestImage)
        self.newestImage = enhancer.enhance(saturation)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def change_contrast(self,contrast):
        """
        Change image contrast according to the contrast value.

        Input:
            image: input image
            contrast: Change image contrast level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Contrast(self.newestImage)
        self.newestImage = enhancer.enhance(contrast)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def change_brightness(self,brightness):
        """
        Change image brightness according to the brightness value.

        Input:
            image: input image
            brightness: Change image brightness level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Brightness(self.newestImage)
        self.newestImage = enhancer.enhance(brightness)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def change_sharpness(self,sharpness):
        """
        Change image sharpness according to the sharpness value.

        Input:
            image: input image
            sharpness: Change image sharpness level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Sharpness(self.newestImage)
        self.newestImage = enhancer.enhance(sharpness)

        self.save_to_cache(self.newestImage)

        return self.newestImage


    def generate_mandelbrot(self):
        """
        For fun function that generates an image of the Mandelbrot Set: https://en.wikipedia.org/wiki/Mandelbrot_set. 
        """
        size = (512, 512)
        extent = (-2, -1.5, 1, 1.5)
        quality = 100

        return Image.effect_mandelbrot(size, extent, quality)
    

    def paste_image(self,image2Paste,coordinates):
        """
        Paste image2 onto image1.

        Input:
            image1: Image to be pasted on.
            image2Paste: Image to be pasted.
            coordinates: Coordinate to paste image at.
        """

        #Paste
        self.newestImage.paste(image2Paste,coordinates)

        self.save_to_cache(self.newestImage)

        return self.newestImage

    
    def put_text(self,text,coordinates,color,size):
        """
        Put a blob of text on an image.

        Input:
            image: Image to be pasted on.
            text: Text to be added.
            coordinates: Coordinate to add text at. Should be like [width,height].
            color: RGB value of the color. Should be like [255,255,255].
        """

        #Make copy and instantiate text obj
        _ = self.newestImage.copy()
        draw = ID.Draw(_)
        font = IF.truetype("alata-regular.ttf", size)

        draw.text(coordinates,text,color,font=font)

        self.newestImage = _

        self.save_to_cache(self.newestImage)

        return self.newestImage
    
    
    def undo(self):
        if self.index == 0:
            # furthest in history OwO
            self.newestImage = self.newestImage
        else:
            self.index -= 1
            self.newestImage = self.cache[self.index]
        
        return self.newestImage
        # raise NotImplementedError("This is your task! Good Luck")
        
        
    def redo(self):
        if self.index == (len(self.cache)-1):
            self.newestImage = self.newestImage
        else:
            self.index += 1
            self.newestImage = self.cache[self.index]
        
        return self.newestImage
        # raise NotImplementedError("This is your task! Good luck!")

