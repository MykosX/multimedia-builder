
# -----------------------------------------------------------------------------
# src/model/helper/image_helper.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.core               import Console, Logger

from PIL                    import Image, ImageColor

# -----------------------------------------------------------------------------
# ImageHelper
#
# * Gives access to specific image IO functions
# * Provides access to image transformations
# -----------------------------------------------------------------------------


class ImageHelper:
    # -------------------------------------------------------------------------
    # Image IO
    # -------------------------------------------------------------------------

    def import_as(self) -> ImageHelper:
        pass

    def export_as(self) -> None:
        pass

    # -------------------------------------------------------------------------
    # General image transformations
    # -------------------------------------------------------------------------

    @classmethod
    def resolve_color(cls, color: str) -> tuple[int, int, int]:
        try:
            return ImageColor.getrgb(color)
        except ValueError:
            Console.warning(f"Invalid color '{color}', falling back to black")
            return (0, 0, 0)

    @classmethod
    def resolve_alpha(cls, alpha: int) -> int:
        return max(0, min(255, alpha))

    @classmethod
    def to_rgba_color(cls, color: tuple[int, int, int], alpha: int) -> tuple[int, int, int, int]:
        return (*color, alpha)

    @classmethod
    def color_to_image(cls, color: str = "0x000000", alpha: int = 255, width: int = 512, height: int = 512) -> Image:
        new_color = cls.resolve_color(color)
        new_alpha = cls.resolve_alpha(alpha)
        rgba_color = cls.to_rgba_color(new_color, new_alpha)

        Logger.debug(
            cls,
            f"color-to-image: color={new_color}, alpha={new_alpha}, width={width}, height={height}"
        )

        return Image.new(
            "RGBA",
            (width, height),
            rgba_color
        )

    @classmethod
    def resize(cls, base_image: Image, width: int = 512, height: int = 512) -> Image:
        Logger.debug(
            type(cls),
            f"resize: base-image={base_image}, width={width}, height={height}"
        )

        return base_image.resize((width, height))

    @classmethod
    def insert_image_at(cls, base_image: Image, x:int, y: int, image_to_insert: Image) -> Image:
        Logger.debug(
            type(cls),
            f"insert-image-at: base-image={base_image}, image-to-insert={image_to_insert}, x={x}, y={y}"
        )

        image = base_image.copy()
        image.paste(image_to_insert, (x, y))

        return image

# -----------------------------------------------------------------------------
