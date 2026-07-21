
# -----------------------------------------------------------------------------
# src/model/image_model.py
# -----------------------------------------------------------------------------

from src.core               import BaseNode, command, Console, Logger
from src.file.backend       import PillowImageFile
from src.model              import BaseModel
from src.model.adapter      import DiffusersAdapter
from src.model.helper       import ImageHelper

# -----------------------------------------------------------------------------
# ImageModel
#
# * Gives access to all usable image commands
# * Has the ability to access the JSON configuration with convenient
# python functions and names
# -----------------------------------------------------------------------------


class ImageModel(BaseModel):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        super().__init__()

    # -------------------------------------------------------------------------
    # Generation with AI models
    # -------------------------------------------------------------------------

    @command("generate-image-from-text")
    def generate_image_from_text(self, context: BaseNode) -> None:
        Logger.debug(
            type(self),
            f"generate-image-from-text: adapter={context.adapter}, parameters={context.parameters}"
        )

        (
            DiffusersAdapter()
            .update(context.parameters)
            .text_to_image()
        )

    @command("generate-image-from-image")
    def generate_image_from_image(self, context: BaseNode) -> None:
        Logger.debug(
            type(self),
            f"generate-image-from-text: adapter={context.adapter}, parameters={context.parameters}"
        )

        (
            DiffusersAdapter()
            .update(context.parameters)
            .image_to_image()
        )

    # -------------------------------------------------------------------------
    # Image IO
    # -------------------------------------------------------------------------

    @command("import-as")
    def import_as(self, context: BaseNode) -> None:
        Console.info("Dummy implementation for 'import-as' command")

    @command("export-as")
    def export_as(self, context: BaseNode) -> None:
        Console.info("Dummy implementation for 'export-as' command")

    # -------------------------------------------------------------------------
    # General image transformations
    # -------------------------------------------------------------------------

    @command("color-to-image")
    def color_to_image(self, context: BaseNode) -> None:
        image = ImageHelper.color_to_image(
            context.color.get(),
            context.alpha.get(),
            context.width.get(),
            context.height.get()
        )
        PillowImageFile(image).to_destination(
            context.output_image_path,
            context.output_image_reference
        )

    @command("resize-image")
    def resize_image(self, context: BaseNode) -> None:
        base_image_file = PillowImageFile.from_source(
            context.input_image_path,
            context.input_image_reference
        )
        image = ImageHelper.resize(
            base_image_file.image,
            context.width.get(),
            context.height.get()
        )
        PillowImageFile(image).to_destination(
            context.output_image_path,
            context.output_image_reference
        )

    @command("insert-image-at")
    def insert_image_at(self, context: BaseNode) -> None:
        base_image_file = PillowImageFile.from_source(
            context.input_image_path,
            context.input_image_reference
        )
        image_to_insert_file = PillowImageFile.from_source(
            context.insert_image_path,
            context.insert_image_reference
        )
        image = ImageHelper.insert_image_at(
            base_image_file.image,
            context.x.get(),
            context.y.get(),
            image_to_insert_file.image
        )
        PillowImageFile(image).to_destination(
            context.output_image_path,
            context.output_image_reference
        )

# -----------------------------------------------------------------------------
