from discord.ext import commands
import os
import sys
import discord
import random as rand
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)

months = ['January', "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

data = {
	1 : {'name': 'username', 'block_number': 'blocks', 'date': 0, 'taken' : False, 'gotblocks': False, 'gotdate': False}
}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def info(ctx):
    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)

@bot.command()
async def whoami(ctx):
    await ctx.send('You are ' + str(ctx.author))

@bot.command()
async def random(ctx):
    await ctx.send('Random number is ' + str(rand.randint(1,100)))


@bot.command(
    help = 'Looks like you need help',
    brief = "Enter the amount of blocks you are selling"
)
async def sell(ctx, arg):
    try:
        if (isinstance(int(arg), int) == True and int(arg) > 0):
            await ctx.send(f'You are selling {arg} block(s)?')
        else:
            await ctx.send(f'You cannot sell {arg} blocks.')
    except:
        await ctx.send(f'Not a valid input for sell')


@bot.command(
    help = 'Gives a list of people selling',
    brief = ''
)
async def list(ctx):
    await ctx.send()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Not an actual command. Please check !help for commands.')
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Missing parameters for {ctx.message.content}. Please check !help for help with commands.')
    raise error

@bot.command(
    brief = "Pongs back to channel"
)
async def ping(ctx):
	# SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
	await ctx.channel.send("pong")

@bot.command()
async def dm(ctx, user:discord.Member, *, message=None):
  message = "How many blocks do you want to sell?"
  embed=discord.Embed(title=message)
  await user.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'hello':
        print(message.channel.id)
        await message.channel.send('Hey')  
    # DM the bot
    elif not message.guild:
        if message.author == bot.user:
            return
        try:
            if message.content.isdigit() and int(message.content) > 0 and len(message.content) == 1:
                await message.channel.send(f"You are listing {message.content} block(s)")
                #save the data
                data[1] = {'name': message.author, 'block_number': int(message.content), 'date': 0, 'taken': False, 'gotblocks': True}
                data[1]['gotblocks'] = True
                await message.channel.send("For when do you want to list your block(s)? Format: DDMM")
            elif message.content.isdigit() != True or int(message.content) >= 3 and data[1]['gotblocks'] == False:
                await message.channel.send(f"You cannot sell {message.content} block(s). You can only sell a maximum of 2 blocks per block period.")
            if message.content.isdigit() == True and int(message.content) > 0 and len(message.content) == 4 and data[1]['gotblocks'] == True:
                month = int(message.content) % 100
                day = int(message.content) // 100
                await message.channel.send(f"You are listing your blocks for {day} {months[month-1]}")
                data[1] = {'date': message.content}
            elif message.content.isdigit() != True and int(message.content) <= 0 and len(message.content) != 4 and data[1]['gotblocks'] == True:
                await message.channel.send(f"Incorrect input format")
    
            # save message parameters into a list of sort
            #send the parsed list to the general server chat

            # We can hardcode the id to send message in both DM and general chat
            # if data[1]['gotblocks'] == True:
            #     channel = bot.get_channel(1020510140501348525)
            #     await channel.send(f"{data[1]['name']} has listed {data[1]['block_number']}") 
  
            # We can hardcode the id to send message in both DM and general chat
            channel = bot.get_channel(1020510140501348525)
            print("works")
            await channel.send(f"<<{data[1]['name']} has listed {data[1]['block_number']}>>") 

        except Exception as e:
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            #await message.channel.send("Not a valid input")
    else:
        pass
  	# Include this at the end of @bot.event
  	# otherwise we can't run commands
    await bot.process_commands(message)




  
@bot.event
async def on_raw_reaction_add(payload):
    #DM the buyer's discord name to the seller 
    if (payload.emoji.name == "👍"):
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # now parse message.content to get id of seller
                                                                                                                                    
        if message.content.startswith("<<"): 
            listing_partition = message.content.split(" ")
            # seller_name = listing_partition[0]
            # print(seller_id)
            # print(bot)
            seller = bot.get_user(575801080580145153)
            # print(seller)
            buyer = bot.get_user(payload.user_id)
            # print(payload.user_id)
            #dm_channel = await seller.create_dm()
            await seller.send(buyer.name + " bought " + seller.name + "'s block! :)")
                              
                                                                                                                                  
        print("User id : ", payload.user_id, "added a thumbs up emoji to message id: ", payload.message_id)


bot.run(TOKEN)