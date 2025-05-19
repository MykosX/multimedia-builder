
from core.frameworks.base   import BaseBuilder
from googletrans            import Translator

class GTransBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.translator = Translator()

    def load(self, action) -> 'GTransBuilder':
        """Does nothing. Writing text is done with set_text command."""
        return self

    def save(self, action) -> 'GTransBuilder':
        """Does nothing. File is saved by translate function."""
        return self

    def translate(self, action) -> 'GTransBuilder':
        """Translate the loaded text."""
        source_language     = action.get("lang-source", "en")
        target_language     = action.get("lang-target", "ro")
        output_text_path    = action.get("output-text-path")
        
        text = self.get_text(action)

        translation = self.translator.translate(text, src=source_language, dest=target_language).text
        self.save_text(translation, output_text_path)
        
        return self
