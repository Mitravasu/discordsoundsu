from discord.ui import LayoutView, Container, TextDisplay, Separator
from discord import Color
from typing import List


class SoundsCard(LayoutView):
    def __init__(self, sounds: List[str]):
        super().__init__()

        container = Container(accent_color=Color.red())

        if sounds:
            container.add_item(TextDisplay("Available Sounds"))
            container.add_item(Separator())

            for sound in sounds:
                container.add_item(TextDisplay(sound))
            container.accent_color = Color.blue()
        else:
            container.add_item(TextDisplay("No sounds available."))

        self.add_item(container)
