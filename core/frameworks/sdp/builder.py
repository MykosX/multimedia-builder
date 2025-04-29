
from core.frameworks.base   import BaseBuilder
from core.utils             import Utils
from PIL                    import Image, ImageColor

class SDPBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.image          = None
        self.sdp_pipeline   = None

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

    def load(self, action) -> 'SDPBuilder':
        """Load image from a given file or from cache."""
        input_image_path    = action.get("input-image-path")
        image_name          = action.get("image-name")

        if input_image_path:
            self.image = self.load_image(input_image_path)
        elif image_name:
            self.image = self.load_from_cache("image", image_name)
        else:
            self.logger.error("[SDPBuilder] No load source specified (file or cache).")
            
        return self

    def save(self, action) -> 'SDPBuilder':
        """Save image to cache or to a given file."""
        image_name          = action.get("image-name")
        output_image_path   = action.get("output-image-path")

        if not (output_image_path or image_name):
            self.logger.error("[SDPBuilder] No save target specified (file or cache).")
            
        if output_image_path:
            self.save_image(self.image, output_image_path)

        if image_name:
            self.save_to_cache("image", image_name, self.image)
        return self

    def set_pipeline(self, pipeline) -> 'SDPBuilder':
        """Set StableDiffusionPipeline to be used with this builder."""
        if pipeline:
            self.sdp_pipeline = pipeline
        else:
            self.logger.error("[SDPBuilder] No StableDiffusionPipeline provided.")
            
        return self

    def generate_image(self) -> 'SDPBuilder':
        """Generate the image from current text and other settings."""
        self.image = self.sdp_pipeline(self.text).images[0]
            
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
        path_to_image       = action.get("path-to-image")
        image_to_insert     = action.get("image-to-insert")
        x                   = action.get("x", 0)
        y                   = action.get("y", 0)
        
        insertion = {
            "input-image-path"  : path_to_image,
            "image-name"        : image_to_insert
        }
        sdp_builder = SDPBuilder().load(insertion)
        overlay = sdp_builder.image
        self.image.paste(overlay, (x, y), overlay.convert("RGBA"))
            
        return self
