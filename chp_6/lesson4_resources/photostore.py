#Import package
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
        
        
    def save_image(self,image,path):
        """
        Simple function to save edited image.

        Input:
            image: Image to be saved.
            path: Path to save image to.
        """
        return image.save(path)
    
    
    def resize_image(self, image, dim):
        """
        Resize a given image according to a given dimension.

        Input:
            image: input image
            dim: size to resize image to
        """

        return image.resize(dim,Image.BICUBIC)


    def resize_image_uniform(self, image, multiple):
        """
        Resize a given image to a multiple of its size. Maintains aspect ratio.

        Input:
            image: input image
            multiple: value to compute resized image dimensions
        """

        #Compute size
        width,height = image.size
        target_size = (int(width * multiple), 
                       int(height * multiple))

        return image.resize(target_size,Image.BICUBIC)


    def flip_image(self, image, axis='vertical'):
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

        return image.transpose(axis_)


    def rotate_image(self, image, degree):
        """
        Rotate a given image according to a given degree.

        Input:
            image: input image
            degree: degree to rotate image to
        """

        return image.rotate(degree,Image.BICUBIC)


    def pad_image(self, image, size, color='black'):
        """
        Pad a given image according to a given size.

        Input:
            image: input image
            size: size of new padded image
            color: image of pads to be added
        """

        return ImageOps.pad(image,size,color=color)


    def crop_image(self, image, coordinates):
        """
        Crop a given image according to a given size.

        Input:
            image: input image
            coordinates: coordinates to crop. Need to be a list or tuple like (left, upper, right, lower).
        """

        return image.crop(coordinates)


    def change_saturation(self,image,saturation):
        """
        Change image saturation according to the saturation value.

        Input:
            image: input image
            saturation: Change image saturation level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Color(image)
        image = enhancer.enhance(saturation)

        return image


    def change_contrast(self,image,contrast):
        """
        Change image contrast according to the contrast value.

        Input:
            image: input image
            contrast: Change image contrast level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Contrast(image)
        image = enhancer.enhance(contrast)

        return image


    def change_brightness(self,image,brightness):
        """
        Change image brightness according to the brightness value.

        Input:
            image: input image
            brightness: Change image brightness level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Brightness(image)
        image = enhancer.enhance(brightness)

        return image


    def change_sharpness(self,image,sharpness):
        """
        Change image sharpness according to the sharpness value.

        Input:
            image: input image
            sharpness: Change image sharpness level to this value
        """

        #Create IE object to apply effect. Just that IE is written this way.
        enhancer = IE.Sharpness(image)
        image = enhancer.enhance(sharpness)

        return image


    def generate_mandelbrot(self):
        """
        For fun function that generates an image of the Mandelbrot Set: https://en.wikipedia.org/wiki/Mandelbrot_set. 
        """
        size = (512, 512)
        extent = (-2, -1.5, 1, 1.5)
        quality = 100

        return Image.effect_mandelbrot(size, extent, quality)
    

    def paste_image(self,image1,image2,coordinates):
        """
        Paste image2 onto image1.

        Input:
            image1: Image to be pasted on.
            image2: Image to be pasted.
            coordinates: Coordinate to paste image at.
        """

        #Paste
        _ = image1.copy() #make a copy
        _.paste(image2,coordinates)

        return _

    
    def put_text(self,image,text,coordinates,color,size):
        """
        Put a blob of text on an image.

        Input:
            image: Image to be pasted on.
            text: Text to be added.
            coordinates: Coordinate to add text at. Should be like [width,height].
            color: RGB value of the color. Should be like [255,255,255].
        """

        #Make copy and instantiate text obj
        _ = image.copy()
        draw = ID.Draw(_)
        font = IF.truetype("alata-regular.ttf", size)

        draw.text(coordinates,text,color,font=font)

        return _
    
    
    def save_checkpoint(self,image):
        raise NotImplementedError("This is your task! Good Luck")
        
        
    def load_checkpoint(self,image):
        raise NotImplementedError("This is your task! Good luck!")