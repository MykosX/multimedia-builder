
from core.frameworks.base   import BaseHandler
from core.frameworks.sdp    import SDPBuilder

class SDPHandler(BaseHandler):
    def __init__(self):
        super().__init__()

        self.commands       = {
            "text-to-image"         : self.text_to_image,
            "image-to-image"        : self.image_to_image,
            "color-to-image"        : self.color_to_image,
            "resize-image"          : self.resize_image,
            #"crop-image"            : self.crop_image(image, x, y, w, h),
            #"rotate-image"          : self.rotate_image(image, degrees),
            #"flip-image"            : self.flip_image(image, direction), # horizontal/vertical
            #"overlay-image"         : self.overlay_image(image, overlay, x, y, alpha)
            "paste-image"           : self.paste_image,
            #"add-border"            : self.add_border(image, size, color),
            #"adjust-brightness"     : self.adjust_brightness(image, factor),
            #"adjust-contrast"       : self.adjust_contrast(image, factor),
            #"remove-background"     : self.remove_background,
            "draw-text"             : self.draw_text,
            #"draw-shape"            : self.draw_shape(image, shape_type, coordinates, color, thickness),
            "with-speech-bubbles"   : self.with_speech_bubbles
            #"blur"                  : self.blur(image, type="gaussian"),
            #"sharpen"               : self.sharpen(image),
            #"grayscale"             : self.grayscale(image),
            #"sepia"                 : sepia(image),
            #"cartoonize"            : cartoonize(image),
            #"threshold"             : threshold(image, value),
            #"invert-colors"         : invert_colors(image),
            #"enhance"               : enhance(image) # super-resolution, detail restore,
            #"face-swap"             : face_swap(source_face, target_image),
        }

    def text_to_image(self, action):
        try:
            self.logger.info("[SDPHandler] Generating image from text")
            
            sdp_builder = SDPBuilder()
            sdp_builder.text_to_image(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in text_to_image: {e}")

    def image_to_image(self, action):
        try:
            self.logger.info("[SDPHandler] Generating image from text and a base image")
            
            sdp_builder = SDPBuilder()
            sdp_builder.image_to_image(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in image-to-image: {e}")

    def draw_text(self, action):
        try:
            self.logger.info("[SDPHandler] Drawing text over image")
            
            sdp_builder = SDPBuilder()
            sdp_builder.load(action).draw_text(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in draw-text: {e}")

    def color_to_image(self, action):
        try:
            self.logger.info("[SDPHandler] Creating image from color")
            
            sdp_builder = SDPBuilder()
            sdp_builder.color_to_image(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in color-to-image: {e}")

    def resize_image(self, action):
        try:
            self.logger.info("[SDPHandler] Resizing image")
            
            sdp_builder = SDPBuilder()
            sdp_builder.load(action).resize(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in resize-image: {e}")

    def paste_image(self, action):
        try:
            self.logger.info("[SDPHandler] Inserting an image into another")
            
            sdp_builder = SDPBuilder()
            sdp_builder.load(action).insert_image(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in paste-image: {e}")

    def with_speech_bubbles(self, action):
        try:
            self.logger.info("[SDPHandler] Inserting speech bubbles")
            
            sdp_builder = SDPBuilder()
            sdp_builder.load(action).apply_speech_bubbles(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in with-speech-bubbles: {e}")

