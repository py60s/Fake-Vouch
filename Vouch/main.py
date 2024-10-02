import json
import os
import asyncio
import random
import discord
from discord.ext import commands

# Load configuration from input/config.json
with open('input/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

channel_id = config["channel_id"]
wait_time = config["wait_time"]
message_count = config["message_count"]

# Load tokens from input/tokens.txt
with open('input/token.txt', 'r', encoding='utf-8') as f:
    tokens = [line.strip() for line in f.readlines() if line.strip()]

# Load reasons from input/reasons.txt
with open('input/reasons.txt', 'r', encoding='utf-8') as f:
    reasons = [line.strip() for line in f.readlines() if line.strip()]

# Set CMD title
os.system(f'title    build: [ py ]    token: [{len(tokens)}]    Ms: [{len(reasons)}]')

# Clear terminal function
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Banner display
def display_banner():
    banner = """
    ██▒   █▓ ▒█████   █    ██  ▄████▄   ██░ ██ 
    ▓██░   █▒▒██▒  ██▒ ██  ▓██▒▒██▀ ▀█  ▓██░ ██▒
    ▓██  █▒░▒██░  ██▒▓██  ▒██░▒▓█    ▄ ▒██▀▀██░
    ▒██ █░░▒██   ██░▓▓█  ░██░▒▓▓▄ ▄██▒░▓█ ░██ 
     ▒▀█░  ░ ████▓▒░▒▒█████▓ ▒ ▓███▀ ░░▓█▒░██▓
     ░ ▐░  ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░ ▒ ░░▒░▒
     ░ ░░    ░ ▒ ▒░ ░░▒░ ░ ░   ░  ▒    ▒ ░▒░ ░
       ░░  ░ ░ ░ ▒   ░░░ ░ ░ ░         ░  ░░ ░
        ░      ░ ░     ░     ░ ░       ░  ░  ░
       ░                     ░                  

    """
    print(banner)

# Main logic for the bot
async def send_messages(token):
    intents = discord.Intents.default()
    intents.messages = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        channel = bot.get_channel(int(channel_id))
        if channel:
            print(f"[+] Token: {token[:-5]}*****")  # Show token with last 5 characters masked
            for _ in range(message_count):
                reason = random.choice(reasons)
                await channel.send(reason)
                await asyncio.sleep(wait_time)  # Use asyncio.sleep
        else:
            print(f"[-] Failed to find channel with ID: {channel_id}")
        await bot.close()  # Ensure the bot connection is closed

    try:
        await bot.start(token)
    except Exception as e:
        print(f"[-] Failed: {e}")

async def main():
    clear_terminal()
    display_banner()

    print("Wait for cooldown")
    tasks = []

    for token in tokens:
        tasks.append(send_messages(token))

    await asyncio.gather(*tasks)  # Run all tasks concurrently

    # Display banner after all tokens are processed
    clear_terminal()
    display_banner()
    
    # Prompt to run again
    while True:
        input("Press Enter to run again")
        # Restart the main function
        await main()

if __name__ == "__main__":
    asyncio.run(main())
