
# src/models/domain/image.py

from src.models.core            import BaseModel
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
            action.get("prompt"),
            action.get("prompt-path"),
            None
        ).get_text()
        
        negative_prompt = TextHelper().resolve_input(
            action.get("negative-prompt"),
            action.get("negative-prompt-path"),
            None
        ).get_text()
            
        model_settings = {
            # model
            "model-path"        : action.get("model-path"),

            # prompts
            "positive-prompt"   : positive_prompt,
            "negative-prompt"   : negative_prompt,

            # image
            "width"             : action.get("image-width"),
            "height"            : action.get("image-height"),

            # diffusion
            "guidance-scale"    : action.get("guidance-scale"),
            "strength"          : action.get("strength"),
            "inference-steps"   : action.get("inference-steps"),

            # randomness
            "seed"              : action.get("seed"),

            # torch
            "torch-device"      : action.get("torch-device"),
            "torch-type"        : action.get("torch-type"),
        }
        return model_settings

    def text_to_image(self, action):
        output_image_path           = action.get("output-image-path")
        output_image_reference      = action.get("output-image-reference")
        
        try:
            Logger.log_info("ImageModel", "Generating image from text")
            
            image_helper = ImageHelper().text_to_image(self.get_model_settings(action))
            image_helper.resolve_output(output_image_path, output_image_reference)
            
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in text_to_image: {e}")

    def image_to_image(self, action):
        seed_image_path             = action.get("seed-image-path")

        output_image_path           = action.get("output-image-path")
        output_image_reference      = action.get("output-image-reference")
        
        try:
            Logger.log_info("ImageModel", "Generating image from text and a base image")
            
            image_helper = ImageHelper(seed_image_path).image_to_image(self.get_model_settings(action))
            image_helper.resolve_output(output_image_path, output_image_reference)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in image-to-image: {e}")

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
            image_helper.resolve_output(output_image_path, output_image_reference)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in color-to-image: {e}")

    def resize_image(self, action):
        try:
            Logger.log_info("ImageModel", "Resizing image")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).resize(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in resize-image: {e}")

    def paste_image(self, action):
        try:
            Logger.log_info("ImageModel", "Inserting an image into another")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).insert_image(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in paste-image: {e}")

    def draw_text(self, action):
        try:
            Logger.log_info("ImageModel", "Drawing text over image")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).draw_text(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in draw-text: {e}")

    def with_speech_bubbles(self, action):
        try:
            Logger.log_info("ImageModel", "Inserting speech bubbles")
            
            #sdp_builder = SDPBuilder()
            #sdp_builder.load(action).apply_speech_bubbles(action).save(action)
        except Exception as e:
            Logger.log_error("ImageModel", f"Error in with-speech-bubbles: {e}")
