
import torch

from diffusers              import StableDiffusionPipeline
from core.frameworks.base   import BaseHandler
from core.frameworks.sdp    import SDPBuilder

class SDPHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.pipe           = None
        self.device         = "cuda" if torch.cuda.is_available() else "cpu"

        self.commands       = {
            "generate-image"        : self.generate_image,
            "create-from-color"     : self.create_from_color,
            "resize-image"          : self.resize_image,
            "insert-into-image"     : self.insert_into_image
        }

    def load_defaults(self, defaults):
        self.model_path     = defaults.get("model-path", "runwayml/stable-diffusion-v1-5")
        self.pipe           = StableDiffusionPipeline.from_pretrained(self.model_path)

        self.pipe.to(self.device)
        self.logger.info(f"[SDPHandler] Loaded defaults: model={self.model_path}, device={self.device}")

    def generate_image(self, action):
        try:
            self.logger.info("[SDPHandler] Generating image")
            
            sdp_builder = SDPBuilder()
            sdp_builder.set_pipeline(self.pipe).set_text(action)
            sdp_builder.generate_image().save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in generate-image: {e}")

    def create_from_color(self, action):
        try:
            self.logger.info("[SDPHandler] Creating image from color")
            
            sdp_builder = SDPBuilder()
            sdp_builder.color_to_image(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in create-from-color: {e}")

    def resize_image(self, action):
        try:
            self.logger.info("[SDPHandler] Resizing image")
            
            sdp_builder = SDPBuilder()
            sdp_builder.load(action).resize(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in resize-image: {e}")

    def insert_into_image(self, action):
        try:
            self.logger.info("[SDPHandler] Inserting an image into another")
            
            sdp_builder = SDPBuilder()
            sdp_builder.load(action).insert_image(action).save(action)
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error in insert-into-image: {e}")

