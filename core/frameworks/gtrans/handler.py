
from core.frameworks.base       import BaseHandler
from core.frameworks.gtrans     import GTransBuilder

class GTransHandler(BaseHandler):
    def __init__(self):
        super().__init__()

        self.commands       = {
            "translate-text"        : self.translate_text
        }

    def translate_text(self, action):
        try:
            self.logger.info("[GTransHandler] Translating")
            
            gtrans_builder = GTransBuilder()
            gtrans_builder.set_text(action).translate(action)
        except Exception as e:
            self.logger.error(f"[GTransHandler] Error in translate-text: {e}")
