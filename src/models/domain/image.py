
# src/models/domain/image.py

from src.models.core            import BaseModel
from src.models.core.decorators import command
from src.models.helpers         import ImageHelper, TextHelper
from src.utils                  import Logger

class ImageModel(BaseModel):
    def __init__(self):
        super().__init__()

        #"crop-image":           self.crop_image(image, x, y, w, h),
        #"rotate-image":         self.rotate_image(image, degrees),
        #"flip-image":           self.flip_image(image, direction), # horizontal/vertical
        #"overlay-image":        self.overlay_image(image, overlay, x, y, alpha)
        #"add-border":           self.add_border(image, size, color),
        #"adjust-brightness":    self.adjust_brightness(image, factor),
        #"adjust-contrast":      self.adjust_contrast(image, factor),
        #"remove-background":    self.remove_background,
        #"draw-shape":           self.draw_shape(image, shape_type, coordinates, color, thickness),
        #"blur":                 self.blur(image, type="gaussian"),
        #"sharpen":              self.sharpen(image),
        #"grayscale":            self.grayscale(image),
        #"sepia":                self.sepia(image),
        #"cartoonize":           self.cartoonize(image),
        #"threshold":            self.threshold(image, value),
        #"invert-colors":        self.invert_colors(image),
        #"enhance":              self.enhance(image) # super-resolution, detail restore,
        #"face-swap":            self.face_swap(source_face, target_image),

    def get_model_settings(self, action):        
        positive_prompt = TextHelper().resolve_input(
            "prompt",
            "prompt-path",
            None
        ).get_text()
        
        negative_prompt = TextHelper().resolve_input(
            "negative-prompt",
            "negative-prompt-path",
            None
        ).get_text()
        
        action["positive-prompt"] = positive_prompt
        action["negative-prompt"] = negative_prompt
        
        return action

    # generate the image from current text and other settings
    @command("text-to-image")
    def text_to_image(self, action):
        output_image_path           = action.get("output-image-path")
        output_image_reference      = action.get("output-image-reference")
        
        try:
            Logger.log_info("ImageModel", "Generating image from text")
            
            image_helper = ImageHelper().text_to_image(self.get_model_settings(action))
            image_helper.resolve_output(output_image_path, output_image_reference)
            
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in text_to_image: {e}")

    # generate the image from current text and other settings
    @command("image-to-image")
    def image_to_image(self, action):
        seed_image_path             = action.get("seed-image-path")

        output_image_path           = action.get("output-image-path")
        output_image_reference      = action.get("output-image-reference")
        
        try:
            Logger.log_info("ImageModel", "Generating image from text and a base image")
            
            image_helper = ImageHelper().load(seed_image_path).image_to_image(self.get_model_settings(action))
            image_helper.resolve_output(output_image_path, output_image_reference)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in image-to-image: {e}")

    # generate the image from color, alpha, width and height
    @command("color-to-image")
    def color_to_image(self, action):
        color                       = ImageHelper.resolve_color(action.get("color"))
        alpha                       = ImageHelper.resolve_alpha(action.get("alpha"))
        width                       = ImageHelper.resolve_image_width(action)
        height                      = ImageHelper.resolve_image_height(action)

        output_image_path           = action.get("output-image-path")
        output_image_reference      = action.get("output-image-reference")

        try:
            Logger.log_info("ImageModel", "Creating image from color")
            
            image_helper = ImageHelper().color_to_image(color, alpha, width, height)
            image_helper.convert("RGBA").resolve_output(output_image_path, output_image_reference)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in color-to-image: {e}")

    # resize the image with new width and height
    @command("resize-image")
    def resize_image(self, action):
        try:
            Logger.log_info("ImageModel", "Resizing image")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).resize(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in resize-image: {e}")

    # insert an image in the current one at position (x, y)
    @command("insert-image")
    def insert_image(self, action):
        try:
            Logger.log_info("ImageModel", "Inserting an image into another")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).insert_image(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in paste-image: {e}")

    # draws text at (x, y)
    @command("draw-text")
    def draw_text(self, action):
        try:
            Logger.log_info("ImageModel", "Drawing text over image")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).draw_text(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in draw-text: {e}")

    # applies speech bubbles at (x, y)
    @command("with-speech-bubbles")
    def with_speech_bubbles(self, action):
        try:
            Logger.log_info("ImageModel", "Inserting speech bubbles")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).apply_speech_bubbles(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in with-speech-bubbles: {e}")
