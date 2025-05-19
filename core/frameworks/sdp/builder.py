
from core.frameworks.base   import BaseBuilder
from core.utils             import Utils
from PIL                    import Image, ImageColor, ImageDraw, ImageFont

class SDPBuilder(BaseBuilder):
    def __init__(self):
        import torch
        super().__init__()
        self.image          = None
        self.pipeline       = None
        self.device         = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_type     = torch.float16 if torch.cuda.is_available() else torch.float32

    def load_image(self, source_path):
        try:
            self.logger.info(f"[SDPBuilder] Loading image from: {source_path}")
            
            return Image.open(source_path)
        except Exception as e:
            self.logger.error(f"[SDPBuilder] Error while loading image: {e}")
            return None

    def save_image(self, image, destination_path):
        try:
            self.logger.info(f"[SDPBuilder] Saving image to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
        
            if image.mode == "RGBA" and destination_path.lower().endswith(".jpg"):
                image = image.convert("RGB")
            
            image.save(destination_path)
        except Exception as e:
            self.logger.error(f"[SDPBuilder] Error while saving image: {e}")

    def load(self, action, path_key="input-image-path", cache_key="image-name") -> 'SDPBuilder':
        """Load image from a given file or from cache."""
        input_image_path    = action.get(path_key)
        image_name          = action.get(cache_key)

        if input_image_path:
            self.image = self.load_image(input_image_path)
        elif image_name:
            self.image = self.load_from_cache("image", image_name)
        else:
            self.logger.error("[SDPBuilder] No load source specified (file or cache).")
            
        return self

    def save(self, action, path_key="output-image-path", cache_key="image-name") -> 'SDPBuilder':
        """Save image to cache or to a given file."""
        image_name          = action.get(cache_key)
        output_image_path   = action.get(path_key)

        if not (output_image_path or image_name):
            self.logger.error("[SDPBuilder] No save target specified (file or cache).")
            
        if output_image_path:
            self.save_image(self.image, output_image_path)

        if image_name:
            self.save_to_cache("image", image_name, self.image)
        return self

    def setup_text2image_pipeline(self, action) -> 'SDPBuilder':
        from diffusers      import AutoPipelineForText2Image
        """Set-up standard StableDiffusion for use with this builder."""
        base_model_path     = action.get("model-path", "stabilityai/stable-diffusion-2-1")

        self.pipeline = AutoPipelineForText2Image.from_pretrained(base_model_path, torch_dtype=self.torch_type).to(self.device)

        self.logger.info(f"[SDPBuilder] Text to image pipeline: base={base_model_path}, device={self.device}")
        
        return self

    def setup_image2image_pipeline(self, action) -> 'SDPBuilder':
        from diffusers      import AutoPipelineForImage2Image
        """Set-up controlled StableDiffusion for use with this builder."""
        base_model_path     = action.get("model-path", "stabilityai/stable-diffusion-2-1")
        self.pipeline = AutoPipelineForImage2Image.from_pretrained(base_model_path, torch_dtype=self.torch_type).to(self.device)

        self.logger.info(f"[SDPBuilder] Text + Image to image pipeline: base={base_model_path}, device={self.device}")

        return self

    def adapt_size(self, width, height):
        """Adapts width and height to match multiples of 8 as Stable Diffusion expects"""
        new_width = (width // 8) * 8
        new_height = (height // 8) * 8
        
        return (new_width, new_height)

    def text_to_image(self, action) -> 'SDPBuilder':
        """Generate the image from current text and other settings."""
        width               = action.get("width", 512)
        height              = action.get("height", 512)
        guidance_scale      = action.get("guidance-scale", 7.5)
        
        prompt              = self.get_text(action, "prompt", "prompt-path")
        negative_prompt     = self.get_text(action, "negative-prompt", "negative-prompt-path")
        self.setup_text2image_pipeline(action)
        
        (width, heigh) = self.adapt_size(width, height)
        
        self.image = self.pipeline(prompt=prompt, negative_prompt=negative_prompt, width=width, height=height, guidance_scale=guidance_scale).images[0]
            
        return self

    def image_to_image(self, action) -> 'SDPBuilder':
        """Generate the image from current text and other settings."""
        width               = action.get("width", 512)
        height              = action.get("height", 512)
        guidance_scale      = action.get("guidance-scale", 7.5)
        strength            = action.get("strength", 0.5)
        
        prompt              = self.get_text(action, "prompt", "prompt-path")
        negative_prompt     = self.get_text(action, "negative-prompt", "negative-prompt-path")
        self.setup_image2image_pipeline(action)
        
        builder = SDPBuilder().load(action, "seed-image-path", "seed-image-name")
        
        if builder.image:
            (width, heigh) = self.adapt_size(width, height)
            self.image = self.pipeline(prompt=prompt, negative_prompt=negative_prompt, image=builder.image, width=width, height=height, strength=strength, guidance_scale=guidance_scale).images[0]
        else:
            self.logger.error("[SDPBuilder] Missing source image")
            
        return self

    def color_to_image(self, action) -> 'SDPBuilder':
        """Generate the image from color, width, height and alpha."""
        color               = action.get("color", "black")
        width               = action.get("width", 512)
        height              = action.get("height", 512)
        alpha               = action.get("alpha", 255)

        rgb_color = ImageColor.getrgb(color)
        rgba_color = (*rgb_color, alpha)
        
        self.image = Image.new("RGBA", (width, height), rgba_color)
            
        return self

    def resize(self, action) -> 'SDPBuilder':
        """Resize the image with new width and height."""
        width               = action.get("width", 512)
        height              = action.get("height", 512)

        self.image = self.image.resize((width, height))
            
        return self

    def insert_image(self, action) -> 'SDPBuilder':
        """Insert an image in the current one at position (x, y)."""
        x                   = action.get("x", 0)
        y                   = action.get("y", 0)

        sdp_builder = SDPBuilder().load(action, "path-to-image", "image-to-insert")
        overlay = sdp_builder.image
        self.image.paste(overlay, (x, y), overlay.convert("RGBA"))
            
        return self

    def draw_text(self, action) -> 'SDPBuilder':
        """Draws text at mentioned coordinates."""
        text_color      = action.get("text-color", "black")
        font_name       = action.get("font-name", "Arial")
        font_size       = action.get("font-size", 30)
        x               = action.get("x", 0)
        y               = action.get("y", 0)

        try:
            import matplotlib.font_manager as fm
            font_path = fm.findfont(font_name)
            font = ImageFont.truetype(font_path, size=font_size)
        except Exception as e:
            font = ImageFont.load_default()

        draw_on_image = ImageDraw.Draw(self.image)
        text = self.get_text(action)

        # Draw text
        draw_on_image.text((x, y), text, font=font, fill=text_color)

        return self

    def apply_speech_bubbles(self, action) -> 'SDPBuilder':
        """Applies speech bubbles at mentioned coordinates."""
        import matplotlib.font_manager as fm

        balloons = action.get("balloon-texts", [])
        
        draw_on_image = ImageDraw.Draw(self.image)

        for balloon in balloons:
            text            = balloon.get("text")
            text_color      = balloon.get("text-color", "black")
            font_name       = balloon.get("font-name", "Arial")
            font_size       = balloon.get("font-size", 30)
            fill_color      = balloon.get("fill-color", "white")
            outline_color   = balloon.get("outline-color", "black")
            x               = balloon.get("x", 0)
            y               = balloon.get("y", 0)
            padding         = balloon.get("padding", 10)

            font_path = fm.findfont(font_name)
            font = ImageFont.truetype(font_path, size=font_size)

            # ✅ Modern Pillow: use textbbox
            bbox = draw_on_image.textbbox((x, y), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            # Draw speech bubble (ellipse)
            draw_on_image.ellipse(
                [x - padding, y - padding, x + w + padding, y + h + padding],
                fill=fill_color,
                outline=outline_color
            )

            # Draw text
            draw_on_image.text((x, y), text, font=font, fill=text_color)

        return self
