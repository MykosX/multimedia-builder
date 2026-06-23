
# -----------------------------------------------------------------------------
# src/model/adapter/diffusers_adapter.py
# -----------------------------------------------------------------------------

from diffusers              import AutoPipelineForText2Image
from diffusers              import AutoPipelineForImage2Image
import torch
from PIL                    import Image

from src.core               import Console, Config, Logger
from src.file               import TextFile
from src.file.backend       import PillowImageFile

# -----------------------------------------------------------------------------
# DiffusersAdapter
#
# * Gives access to diffusers framework
# -----------------------------------------------------------------------------


class DiffusersAdapter(Config):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        super().__init__(
            {
                "model-path"            : "MykosX/delia-anime-sd",
                "device"                : "cpu",
                "dtype"                 : "float32",
                "guidance-scale"        : 7.5,
                "num-inference-steps"   : 30,
                "seed"                  : 0,
                "width"                 : 512,
                "height"                : 512,
            }
        )

    # -------------------------------------------------------------------------
    # Internal interfaces
    # -------------------------------------------------------------------------

    def resolve_device(self):
        if self.config.device.get() == "cuda":
            torch_device = "cuda"
        else:
            torch_device = "cpu"
        
        if torch_device == "cuda" and not torch.cuda.is_available():
            Console.warning(f"CUDA unavailable. Using CPU instead.")
            return "cpu"

        return torch_device

    def resolve_dtype(self):
        if self.config.dtype.get() == "float16":
            torch_dtype = torch.float16
        else:
            torch_dtype = torch.float32

        if torch_dtype == torch.float16 and not torch.cuda.is_available():
            Console.warning(f"CUDA unavailable. Using torch.float32 instead.")
            return torch.float32

        return torch_dtype

    def resolve_generator(self):
         return torch.manual_seed(self.config.seed.get())

    def resolve_image_width(self):
        width = self.config.width.get()
        new_width = (width // 8) * 8
        
        if new_width != width:
            Console.warning(f"Realigned width to multiple of 8: new-width={new_width}")
        
        return new_width

    def resolve_image_height(self):
        height = self.config.height.get()
        new_height = (height // 8) * 8
        
        if new_height != height:
            Console.warning(f"Realigned height to multiple of 8: new-height={new_height}")
        
        return new_height

    def load_diffusers_pipeline(self, pipeline_class):
        model_path  = self.config.model_path.get()
        torch_dtype = self.resolve_dtype()
        torch_device= self.resolve_device()

        pipeline = pipeline_class.from_pretrained(
            model_path,
            torch_dtype=torch_dtype
        ).to(torch_device)

        Logger.info(
            type(self),
            f"{pipeline_class.__name__} loaded: model={model_path}, dtype={torch_dtype}, device={torch_device}"
        )
        return pipeline

    # -------------------------------------------------------------------------
    # Interfaces available to other classes
    # -------------------------------------------------------------------------

    def text_to_image(self) -> None:
        pipeline = self.load_diffusers_pipeline(AutoPipelineForText2Image)
        prompt_file = TextFile.from_source(
            self.config.prompt,
            self.config.prompt_path,
            self.config.prompt_reference
        )
        negative_prompt_file = TextFile.from_source(
            self.config.negative_prompt,
            self.config.negative_prompt_path,
            self.config.negative_prompt_reference,
            False
        )

        image = pipeline(
            prompt              = prompt_file.text,
            negative_prompt     = negative_prompt_file.text,
            guidance_scale      = self.config.guidance_scale.get(),
            num_inference_steps = self.config.num_inference_steps.get(),
            generator           = self.resolve_generator(),
            width               = self.resolve_image_width(),
            height              = self.resolve_image_height(),
        ).images[0]

        (
            PillowImageFile(image).to_destination(
                self.config.output_image_path,
                self.config.output_image_reference
            )
        )

    def image_to_image(self) -> None:
        pipeline = self.load_diffusers_pipeline(AutoPipelineForImage2Image)
        prompt_file = TextFile.from_source(
            self.config.prompt,
            self.config.prompt_path,
            self.config.prompt_reference
        )
        negative_prompt_file = TextFile.from_source(
            self.config.negative_prompt,
            self.config.negative_prompt_path,
            self.config.negative_prompt_reference,
            False
        )
        base_image_file = PillowImageFile.from_source(
            self.config.base_image_path,
            self.config.base_image_reference
        )

        image = pipeline(
            prompt              = prompt_file.text,
            negative_prompt     = negative_prompt_file.text,
            image               = base_image_file.image,
            guidance_scale      = self.config.guidance_scale.get(),
            num_inference_steps = self.config.num_inference_steps.get(),
            generator           = self.resolve_generator(),
            width               = self.resolve_image_width(),
            height              = self.resolve_image_height(),
        ).images[0]

        (
            PillowImageFile(image).to_destination(
                self.config.output_image_path,
                self.config.output_image_reference
            )
        )

# -----------------------------------------------------------------------------
