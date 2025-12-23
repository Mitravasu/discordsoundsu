from discord.ui import LayoutView, Container, TextDisplay, Separator
from discord import Color
from ..types import SleepData

class SleepInfoCard(LayoutView):
    def __init__(self, sleep_data: SleepData):
        super().__init__()

        self.add_item(
            Container(
                TextDisplay("🟢 **ENABLED**" if sleep_data.is_enabled else "🔴 **DISABLED**"),
                Separator(),
                TextDisplay(f"🕒 **Time:** {sleep_data.time}"),
                TextDisplay(f"🌍 **Timezone:** {sleep_data.timezone}"),
                TextDisplay(f"🔊 **Sound:** {sleep_data.sound}"),
                accent_color=(Color.green() if sleep_data.is_enabled else Color.red())
            )
        )

