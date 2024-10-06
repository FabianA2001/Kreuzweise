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
img :Img
worts = ["Haus","Pflanze","Ritter","See","Frau","Liebe","Essen","Apfelkuchen"]

@bot.command()
async def send(ctx):
    # Save the image to a BytesIO object
    img.update()
    # img.img.save("test.png")
    with io.BytesIO() as image_binary:
        img.img.save(image_binary, 'PNG')
        image_binary.seek(0)  # Move the cursor to the start of the file
        
        # Send the image as a Discord file
        message = await ctx.send(file=discord.File(fp=image_binary, filename="image.png"))




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
async def reset(ctx):
    global img
    img = Img(worts)
    await ctx.send(f"reset")

@bot.command()
async def get(ctx):
    message = await ctx.author.send(img.reduceCarts())
    await message.add_reaction('✅')
    await message.add_reaction('❌')
 
# Event listener that triggers when a reaction is added
@bot.event
async def on_reaction_add(reaction, user):
    # Ignore reactions added by the bot itself
    if user.bot:
        return
    
    # Check if the reaction is on a specific message or a general condition
    if str(reaction.emoji) == "✅":
        print(reaction.message.content)
        img.addCart(reaction.message.content)
    elif str(reaction.emoji) == "❌":
        img.addDiscard()
 
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
