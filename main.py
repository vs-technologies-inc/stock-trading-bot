import discord
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tracked_symbols = {}
CHANNEL_IDS = [1234567890, 9876543210]  # Replace with your actual channel IDs

async def check_common_symbols():
    now = datetime.now()
    expired_symbols = []

    for symbol, timestamp in tracked_symbols.items():
        if now - timestamp > timedelta(hours=24):
            expired_symbols.append(symbol)

    for symbol in expired_symbols:
        del tracked_symbols[symbol]

def extract_symbols(message_content):
    words = message_content.split()
    return [word for word in words if word.isalpha() and word.isupper()]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id not in CHANNEL_IDS:
        return

    symbols = extract_symbols(message.content)

    common_symbols = []

    for symbol in symbols:
        if symbol in tracked_symbols:
            common_symbols.append(symbol)
        else:
            tracked_symbols[symbol] = datetime.now()

    if common_symbols:
        await message.channel.send(f"Common stock symbols found: {', '.join(common_symbols)}")

    # Cleanup expired symbols periodically
    await check_common_symbols()

client.run('YOUR_BOT_TOKEN')
