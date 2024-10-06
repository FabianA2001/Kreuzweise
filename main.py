import discord
from discord.ext import commands
from TOKEN import TOKEN   #python Datei mit TOKEN = "$discord token$"
from Img import Img
import io

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# File to store user IDs
player1: int = 0
player2: int = 0
img :Img
worts = ["Haus","Pflanze","Ritter","See","Frau","Liebe","Essen","Apfelkuchen"]
is_runnning:bool = False


async def is_startet(ctx) -> bool:
    if(is_runnning):
        return True
    await ctx.send("Start game with '!start'")
    return False

@bot.command()
async def send_img(ctx):
    # Save the image to a BytesIO object
    img.update()
    # img.img.save("test.png")
    with io.BytesIO() as image_binary:
        img.img.save(image_binary, 'PNG')
        image_binary.seek(0)  # Move the cursor to the start of the file
        
        # Send the image as a Discord file
        message = await ctx.send(file=discord.File(fp=image_binary, filename="image.png"))
        await message.add_reaction('✅')
        await message.add_reaction('❌')



async def send_message_to_user(user_id, message):
    """Send a message to a user by their user ID."""
    try:
        user = await bot.fetch_user(user_id)  # Fetch user from the Discord API
        await user.send(message)  # Send the message
    except discord.Forbidden:
        print(f'Could not send message to {user.name}. They might have DMs disabled.')
    except discord.HTTPException as e:
        print(f'Failed to send message to user {user_id}: {e}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    global img 
    img = Img(worts)

@bot.command()
async def save(ctx, member: discord.Member, member2: discord.Member):
    global player1, player2
    player1 = member.id
    player2 = member2.id
    await ctx.send(f'player 1: {member.mention} --- player 2: {member2.mention}')

@bot.command()
async def send(ctx, *, message: str):
    if(player1 == 0):
        await ctx.send(f"Player 1 nicht festgelet")

    if(player2 == 0):
        await ctx.send(f"Player 2 nicht festgelet")
    if(player1 != 0 and player2 != 0):
        await send_message_to_user(player1, message)  # Await the send_message_to_user
        await send_message_to_user(player2, message)  # Await the send_message_to_user

@bot.command()
async def reset(ctx):
    global player1, player2, img,is_runnning
    player1 = 0
    player2 = 0
    img = Img(worts)
    is_runnning = False
    await ctx.send(f"reset")

@bot.command()
async def start(ctx):
    if(player1 == 0):
        await ctx.send(f"Player 1 nicht festgelet")
    if(player2 == 0):
        await ctx.send(f"Player 2 nicht festgelet")
    if(player1 != 0 and player2 != 0):
        global is_runnning
        is_runnning = True
        await send_img(ctx)

@bot.command()
async def get(ctx):
    if not is_startet(ctx):
        return
    if ctx.auther.id == player1:
        await send_message_to_user(player1, img.reduceCarts())  # Await the send_message_to_user
        await ctx.send("Player 1 hat eine Karte bekommen")

    if ctx.auther.id == player2:
        await send_message_to_user(player2, img.reduceCarts())  # Await the send_message_to_user
        await ctx.send("Player 2 hat eine Karte bekommen")
 

 
# Global error handler for all commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # Handle missing argument errors
        await ctx.send(f"Error: Missing required argument: {error.param}")
    elif isinstance(error, commands.CommandNotFound):
        # Handle unknown commands
        await ctx.send("Error: Command not found.")
    elif isinstance(error, commands.CommandInvokeError):
        # Handle exceptions that occurred during the command invocation
        await ctx.send(f"An error occurred while executing the command: {str(error)}")
    elif isinstance(error, commands.MemberNotFound):
        # Handle exceptions that occurred during the command invocation
        await ctx.send(f"can't find member: {error}")
    else:
        # Log the error for any other unhandled exceptions
        await ctx.send(error)

# Run the bot with your token
bot.run(TOKEN)
