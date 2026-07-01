
# src/models/helpers/image.py

from src.models.core            import BaseHelper
from src.utils                  import Logger
from PIL                        import Image, ImageColor, ImageDraw, ImageFont

EMPTY_IMAGE = Image.new("RGBA", (1, 1), (0, 0, 0, 0))

class ImageHelper(BaseHelper):
    def __init__(self, image : Image):
        self.image = image or EMPTY_IMAGE.copy()
    
    def get_image(self) -> Image:
        return self.image

    # loads omage from specified file path
    def load(self, source_path) -> ImageHelper:
        try:
            Logger.logger.info("ImageHelper", f"Loading image from: {source_path}")
            
            self.image = Image.open(source_path)
        except Exception as e:
            Logger.logger.error("ImageHelper", f"Error while loading image: {e}")
        
        return ImageHelper(self.image)
    
    # saves image to a specified file
    def save(self, destination_path: str, format: str="JPEG") -> ImageHelper:
        try:
            Logger.log_info("ImageHelper", f"Saving image to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
            
            image.save(destination_path, format=format.upper())
        except Exception as e:
            Logger.log_error("ImageHelper", f"Error while saving image to {destination_path}: {e}")
        
        return self
    
    # resolves the input as image: a) read from a file or b) read from cache
    def resolve_input(self, input_image_path, input_image_reference) -> ImageHelper:
        if input_image_path:
            image_helper = ImageHelper().load(input_image_path)
        elif input_image_reference:
            image_helper = ImageHelper.load_from_cache("image", input_image_reference)
        else:
            Logger.log_error("ImageHelper", f"No image source specified (file:'{input_image_path}' or reference:'{input_image_reference}').")
            image_helper = ImageHelper()
            
        return image_helper

    # resolves the output as image: a) writes to a file or b) saves to cache
    def resolve_output(self, output_image_path, output_image_reference) -> ImageHelper:
        if not (output_image_path or output_image_reference):
            Logger.log_error("ImageHelper", f"No save target specified (file:'{output_image_path}' or reference:'{output_image_reference}').")

        if output_image_path:
            self.save(output_image_path)

        if output_image_reference:
            ImageHelper.save_to_cache("image", output_image_reference, self)
        
        return self
    
    @staticmethod
    def resolve_positive_prompt(model_settings):
        return model_settings.get("positive-prompt")

    @staticmethod
    def resolve_negative_prompt(model_settings):
        return model_settings.get("negative-prompt")

    @staticmethod
    def resolve_model(model_settings):
        return model_settings.get("model-path", "MykosX/delia-anime-sd")

    @staticmethod
    def resolve_device(model_settings):
        device = model_settings.get("torch-device",  "cpu")
        
        if device == "cuda" and not torch.cuda.is_available():
            device = "cpu"
            Logger.log_warning("ImageHelper", f"CUDA requested but unavailable. Falling back to CPU.")
        
        return device

    @staticmethod
    def resolve_dtype(model_settings):
        dtype = model_settings.get("torch-type", "float16")
        
        if dtype == "float16" and not torch.cuda.is_available():
            return torch.float32

        return torch.float16

    @staticmethod
    def resolve_generator(model_settings):
        seed = model_settings.get("seed", 0)
        
        return torch.manual_seed(seed)

    @staticmethod
    def resolve_seed_image_path(model_settings):
        return model_settings.get("seed-image-path")

    @staticmethod
    def resolve_image_width(model_settings):
        width = model_settings.get("width", 512)
        new_width = (width // 8) * 8
        
        if new_width != width:
            Logger.log_warning("ImageHelper", f"Realigned width to multiple of 8: new-width={new_width}")
        
        return new_width

    @staticmethod
    def resolve_image_height(model_settings):
        height = model_settings.get("height", 512)
        new_height = (height // 8) * 8
        
        if new_height != height:
            Logger.log_warning("ImageHelper", f"Realigned height to multiple of 8: new-height={new_height}")
        
        return new_height

    @staticmethod
    def resolve_guidance_scale(model_settings):        
        return model_settings.get("guidance-scale", 7.5)

    @staticmethod
    def resolve_strength(model_settings):        
        return model_settings.get("strength", 0.5)

    @staticmethod
    def resolve_inference_steps(model_settings):        
        return model_settings.get("inference-steps", 30)

    @staticmethod
    def resolve_color(color: str):
        try:
            rgb = ImageColor.getrgb(color)
        except ValueError:
            Logger.log_warning("ImageHelper", f"Invalid color '{color}', falling back to black")
            rgb = (0, 0, 0)

        return rgb

    @staticmethod
    def resolve_alpha(alpha: int | None):
        return max(0, min(255, alpha or 255))

    @staticmethod
    def to_rgba_color(rgb_color, alpha):
        return (*rgb_color, alpha)

    def load_diffusers_pipeline(self, pipeline_class, model_settings):
        model_path  = ImageHelper.resolve_model(model_settings)
        dtype       = ImageHelper.resolve_dtype(model_settings)
        device      = ImageHelper.resolve_device(model_settings)

        pipeline = pipeline_class.from_pretrained(
            model_path,
            torch_dtype=dtype
        ).to(device)

        Logger.log_info("ImageHelper", f"{pipeline_class.__name__} loaded: model={model_path}, dtype={dtype}, device={device}")

        return pipeline

    def get_t2i_pipeline(self, model_settings):
        from diffusers import AutoPipelineForText2Image
        
        return self.load_diffusers_pipeline(
            AutoPipelineForText2Image,
            model_settings
        )
    
    def get_i2i_pipeline(self, model_settings):
        from diffusers      import AutoPipelineForImage2Image
        
        return self.load_diffusers_pipeline(
            AutoPipelineForImage2Image,
            model_settings
        )
    
    def convert(self, mode:str="RGBA") -> ImageHelper:
        return ImageHelper(self.image.convert(mode))
    
    def text_to_image(self, model_settings) -> ImageHelper:
        pipeline = self.get_t2i_pipeline(model_settings)
        
        image = pipeline(
            prompt              = ImageHelper.resolve_positive_prompt(model_settings),
            negative_prompt     = ImageHelper.resolve_negative_prompt(model_settings),
            guidance_scale      = ImageHelper.resolve_guidance_scale(model_settings),
            num_inference_steps = ImageHelper.resolve_inference_steps(model_settings),
            generator           = ImageHelper.resolve_generator(model_settings),
            width               = ImageHelper.resolve_image_width(model_settings),
            height              = ImageHelper.resolve_image_height(model_settings),
        ).images[0]
        
        return ImageHelper(image)

    def image_to_image(self, model_settings) -> ImageHelper:
        pipeline = self.get_i2i_pipeline(model_settings)
        
        image = pipeline(
            prompt              = ImageHelper.resolve_positive_prompt(model_settings),
            negative_prompt     = ImageHelper.resolve_negative_prompt(model_settings),
            image               = self.image
            guidance_scale      = ImageHelper.resolve_guidance_scale(model_settings),
            num_inference_steps = ImageHelper.resolve_inference_steps(model_settings),
            generator           = ImageHelper.resolve_generator(model_settings),
            width               = ImageHelper.resolve_image_width(model_settings),
            height              = ImageHelper.resolve_image_height(model_settings),
        ).images[0]
        
        return ImageHelper(image)

    def color_to_image(self, color, alpha, width, height) -> ImageHelper:
        rgba_color = ImageHelper.rgba_color(color, alpha)
        image = Image.new(
            "RGBA",
            (width, height),
            rgba_color
        )

        return ImageHelper(image)

