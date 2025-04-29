
import os
import torch

from diffusers import StableDiffusionPipeline
from core.utils.utils import Utils
from core.utils.logger import SimpleLogger
from core.handlers.base_handler import BaseHandler

class SDPHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.commands = {
            "generate_image": self.generate_image
        }

    def load_defaults(self, defaults):
        self.model_path = defaults.get("model_path", "runwayml/stable-diffusion-v1-5")
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_path)
        self.pipe.to(self.device)
        self.logger.info(f"[SDPHandler] Loaded model: {self.model_path} on {self.device}")

    def generate_image(self, action):
        text = action.get("text")
        text_source = action.get("text_source")
        output_path = action.get("output")

        if text_source and os.path.isfile(text_source):
            with open(text_source, "r", encoding="utf-8") as f:
                text = f.read().strip()

        if not text:
            self.logger.warning("[SDPHandler] No prompt text found.")
            return

        try:
            self.logger.info(f"[SDPHandler] Generating image from prompt: {text}")
            image = self.pipe(text).images[0]

            Utils.ensure_dir(os.path.dirname(output_path))
            image.save(output_path)

            self.logger.info(f"[SDPHandler] Image saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"[SDPHandler] Error generating image: {e}")
