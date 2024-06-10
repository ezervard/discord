import discord
from discord.ext import commands
import gtts
from playsound import playsound
import os

config = {
    'token': 'my_token',
    'prefix': '/',
}
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
discord.Client(intents=intents)
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)


@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user.name}')


TARGET_CHANNEL_ID = channel_id  # ID голосового канала


@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        await channel.connect()


@bot.event
async def on_voice_state_update(member, before, after) -> None:
    # Проверяем, если пользователь подключился к каналу
    if after.channel and after.channel.id == TARGET_CHANNEL_ID and before.channel != after.channel:
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if voice_client and voice_client.channel.id == TARGET_CHANNEL_ID:
            # Создаем аудио сообщение с помощью gtts
            user = gtts.gTTS(f'На канал зашёл {member.global_name}', lang='ru', tld='co.uk', slow=False)
            user.save('user_connect.mp3')
            source = discord.FFmpegPCMAudio('user_connect.mp3')
            voice_client.play(source, after=lambda e: os.remove('user_connect.mp3') if not e else None)


bot.run(config['token'])

'(message.author.global_name)'
