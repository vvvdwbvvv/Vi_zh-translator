import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
import dotenv
import os

dotenv.load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator()

LANGUAGES = {
    "zh": "中文",
    "vi": "越南語"
}

@bot.event
async def on_ready():
    print(f"✅ 機器人 {bot.user} 已啟動")
    try:
        # 同步應用指令（Slash Commands）
        synced = await bot.tree.sync()
        print(f"✅ 成功同步 {len(synced)} 個指令")
    except Exception as e:
        print(f"❌ 指令同步失敗: {e}")

@bot.tree.command(name="test", description="翻譯文字（自動偵測語言）")
async def test(interaction: discord.Interaction, text: str):
    """ 使用 `/translate 文字` 自動偵測語言並翻譯 """
    try:
        detected_lang = translator.detect(text).lang  # 自動偵測語言
        
        # 🛠️ 除錯：顯示偵測到的語言
        await interaction.response.send_message(f"🔍 偵測到的語言: `{detected_lang}`", ephemeral=True)
        return  # 先測試這部分，之後再啟用翻譯

    except Exception as e:
        await interaction.response.send_message("❌ 偵測語言失敗！", ephemeral=True)
        print(e)


@bot.tree.command(name="translate", description="翻譯文字（自動偵測語言）")
async def translate(interaction: discord.Interaction, text: str):
    """ 使用 `/translate 文字` 自動偵測語言並翻譯 """
    try:
        detected_lang = translator.detect(text).lang.lower()  # 自動偵測語言並轉換小寫
        
        # ✅ 修正大小寫問題，確保 `zh-cn`, `zh-tw` 都能正確轉換
        if detected_lang.startswith("zh"):
            target_lang = "vi"
        elif detected_lang == "vi":
            target_lang = "zh-cn"
        else:
            await interaction.response.send_message(f"❌ 只支援 中文 ↔ 越南語！(偵測到: `{detected_lang}`)", ephemeral=True)
            return

        translated = translator.translate(text, dest=target_lang)
        await interaction.response.send_message(f"**翻譯結果:** {translated.text}")

    except Exception as e:
        await interaction.response.send_message("❌ 翻譯失敗，請稍後再試！", ephemeral=True)
        print(e)


bot.run(os.getenv("BOT_TOKEN")) 