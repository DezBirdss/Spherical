
import random
import discord
import aiohttp
import discord.ext
from discord.ext import commands
from discord import Color
import time
import os



class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("s!"), intents=discord.Intents().all())


    async def on_ready(self):
        print("Spherical can see me ")
        synced = await self.tree.sync()



client = Client()

@client.hybrid_command(name="seal", description="Seal pictures")
async def seal(ctx: commands.Context):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/seals/.json', headers={'User-agent': 'Mozilla/5.0'}) as response:
            json_data = await response.json()
            posts = json_data['data']['children']
            image_posts = [post for post in posts if 'preview' in post['data']]
            random_post = random.choice(image_posts)
            image_url = random_post['data']['url']
            embed = discord.Embed(title='Seal!', color=discord.Color.blue())
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)

@client.hybrid_command(name="ping", description="Tells you the seals status")
async def ping(ctx):
    embed = discord.Embed(
        color=discord.Color.from_rgb(42,45,49)  
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1070822894675951616/1092912035613917294/seal-5882547_1280.png') # Set custom image URL as thumbnail
    embed.add_field(name='Latency', value=int(client.latency * 1000), inline=False)
 
        
            
   
    await ctx.send(embed=embed)

@client.hybrid_command(name="support", description="Links you to the support server")
async def ping(ctx):
    embed = discord.Embed(
        color=discord.Color.from_rgb(42,45,49)  
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1070822894675951616/1092912035613917294/seal-5882547_1280.png') # Set custom image URL as thumbnail
    embed.add_field(name='Support',value='[**Join**](https://discord.gg/Scr3rzWPNf)')
 
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(embed=discord.Embed(description=':bangbang: Command not found. Please check your input.', color=0xFF0000))
    elif isinstance(error, commands.MissingRequiredArgument) and str(error.param) == 'user':
        await ctx.reply(embed=discord.Embed(description=':bangbang: Please mention a user. Usage: `!userinfo [user]`', color=0xFF0000))
        

@client.hybrid_command(name="userinfo", description="Gets information on user")
async def ping(ctx, user: discord.Member):
    embed = discord.Embed(
        color=discord.Color.from_rgb(42,45,49)  
    )
   
    embed.add_field(name='Name', value=user.name, inline=True)
    embed.add_field(name='ID', value=user.id, inline=False)
    role_mentions = ', '.join([r.mention for r in user.roles[1:]])
    embed.add_field(name='Roles', value=role_mentions if role_mentions else 'No roles', inline=False)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1070822894675951616/1092912035613917294/seal-5882547_1280.png')

    await ctx.send(embed=embed)

client.remove_command('help')

@client.hybrid_command(name="help", description="gives you information about the commands")
async def help(ctx):
    embed = discord.Embed(
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1070822894675951616/1092912035613917294/seal-5882547_1280.png')
    embed.add_field(name='`/userinfo`',value= ' - shows information on someone or yourself' ,inline=False)
    embed.add_field(name='`/ping`',value=' - Shows the bots latency' ,inline=False) 
    embed.add_field(name='`/seal`',value=' - Shows cute pictures of seals 🦭' ,inline=False)
    embed.add_field(name='`/support`',value=' - Shows link to the support server' ,inline=False)
    embed.add_field(name='`/say`',value=' - Repeats a message back' ,inline=False)
    embed.add_field(name='`/sealfact`',value=' - gives you a seal fact 🦭' ,inline=False)
    embed.add_field(name='`/sealgif`',value=' - gives you a seal a seal gif 🦭' ,inline=False)
    embed.add_field(name='`/sealavatar`',value=' - puts your avatar on a seal 🦭' ,inline=False)
    embed.add_field(name='`/sealgame`',value=' - a game about seals 🦭' ,inline=False)
    
    await ctx.send(embed=embed)

@client.hybrid_command(name="say", description="your message repeats back with the bot")
@commands.has_permissions(administrator=True)  # daddy pig needs administrator perms
async def say(ctx, *, message):
    """Sends a message to the same channel as the command was used."""
    await ctx.send(message)

@say.error
async def say_error(ctx, error):
    """Error handler for the say command."""
    if isinstance(error, commands.MissingPermissions):
        # Send an error message pooy message saying YOU CANT FUCKING DO THAT!!
        await ctx.send("You don't have permission to use this command.")

@client.command()
@commands.is_owner()  #ok
async def guilds(ctx):
    """Lists all the servers the bot is a member of"""
    try:
        server_list = [guild.name for guild in client.guilds]
        server_count = len(server_list)
        server_list_str = '\n'.join(server_list)
        embed = discord.Embed(title=f'Guilds ({server_count} servers)', description=server_list_str, color=discord.Color.blue())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1070822894675951616/1092912035613917294/seal-5882547_1280.png')
        await ctx.send(embed=embed, ephemeral=True)
    except Exception as e:
        await ctx.send(f'An error occurred while listing servers: {e}', ephemeral=True)

@guilds.error
async def list_servers_error(ctx, error):
    """Handles error when non-owner user tries to use the list_servers command"""
    if isinstance(error, commands.CheckFailure):
        await ctx.send('This command can only be used by the bot owner.', ephemeral=True)

seal_facts = [
    "Seals are marine mammals that are closely related to sea lions and walruses.",
    "Seals are excellent swimmers and can stay submerged for long periods of time.",
    "Seals have a layer of blubber that helps them stay warm in cold waters.",
    "There are about 33 species of seals found in both Arctic and Antarctic regions.",
    "Seals feed on a diet of fish, squid, and other marine creatures.",
    "Seals have excellent hearing and vision, which help them navigate and locate prey in the water.",
    "Seals come in a variety of sizes, with some species reaching up to 3,500 pounds.",
    "Seals spend much of their time resting on ice floes or beaches.",
    "Seals have a unique way of moving on land called \"hopping\" or \"galloping\".",
    "Seals are known for their playful behavior and can often be seen swimming, diving, and interacting with each other.",
    "Seals have a unique way of thermoregulating with the ability to constrict blood",
    "Seals are capable of sleeping both on land and in the water, often resting with their heads above water while floating.",
    "Seals have a high metabolic rate, allowing them to generate enough heat to stay warm in cold waters.",
    "Seals are known to migrate over long distances, often traveling hundreds or even thousands of miles in search of food.",
    "Seals have a keen sense of touch, with sensitive whiskers called vibrissae that help them navigate in the dark and locate prey.",
    "Seals have a unique way of resting on land called bottling, where they lay on their side with their head and flippers elevated.",
    "Seals have specialized nostrils that close tightly when they are underwater, preventing water from entering their lungs.",
    "Seals are well-adapted to living in cold environments, with a thick layer of blubber and dense fur to keep them warm.",
    "Seals have a relatively long lifespan, with some species living up to 30 years or more.",
    "Seals are well-adapted to living in cold environments, with a thick layer of blubber and dense fur to keep them warm.",
    "Seals are social animals, often found in groups called colonies or haul-outs.",
    "Seals have a thick layer of blubber that helps them stay buoyant in the water.",
    "Seals are known for their agility in the water, able to make quick turns and maneuvers to catch prey.",
    "Seals have a streamlined body shape that allows them to swim at high speeds, reaching up to 20 miles per hour.",
    "Seals are capable of diving to great depths, with some species known to dive over 1,500 feet.",
    "Seals have a highly developed sense of smell, which helps them locate prey in the water.",
    "Seals are important indicators of the health of marine ecosystems, as their presence or absence can provide insight into the overall health of the environment.",
    "Seals have specialized teeth that are adapted for catching and eating fish.",
    "Seals have a thick layer of fur that helps insulate them from the cold water.",
    "Seals have a unique circulatory system that allows them to reduce blood flow to non-essential organs while diving, conserving oxygen.",
]


@client.hybrid_command(name="sealfact", description="gives you a random seal fact")
async def seal_fact(ctx):
    """Provides a random fact about seals"""
    random_fact = random.choice(seal_facts)
    embed = discord.Embed(title="Seal Fact", description=random_fact, color=discord.Color.blue())
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1070822894675951616/1092912035613917294/seal-5882547_1280.png')
    await ctx.send(embed=embed)

import requests
import json
from random import randint


api_key = "dsFEgvQUFm5Y5tWxSj2Zc92DMUMSSLLR" # bugsy put giphy api as tenor is ass
@client.hybrid_command(name="sealgif", brief="Display a random seal GIF")
async def seal_gif(ctx):
    try:
        
        query = "seal"

       
        url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=25"

       
        response = requests.get(url)

        # Parse response
        data = json.loads(response.text)

       
        if "data" in data and len(data["data"]) > 0:
            
            gif_index = randint(0, len(data["data"]) - 1)
            gif_url = data["data"][gif_index]["images"]["original"]["url"]

            
            await ctx.send(gif_url)
        else:
            await ctx.send("No GIFs found.")
    except Exception as e:
        await ctx.send(f"Error occurred: {e}")


from PIL import Image
import requests
from io import BytesIO
import discord

@client.hybrid_command(name="sealavatar", description="Puts your avatar on a seal's head")
async def seal_avatar(ctx):
    try:
        # Get author's avatar URL
        author_avatar_url = str(ctx.author.avatar.url)
        response = requests.get(author_avatar_url)
        avatar_image = Image.open(BytesIO(response.content))
        avatar_image = avatar_image.resize((300, 300))  # Resize to seal's head size

        # Download seal image
        seal_url = "https://media.discordapp.net/attachments/1092978456196829265/1094021443978805288/IMG_0363.jpg"
        seal_response = requests.get(seal_url)
        seal_image = Image.open(BytesIO(seal_response.content))

        # Paste avatar on seal's head
        seal_image.paste(avatar_image, (161, 58))  # Adjust coordinates as needed

        # Save edited image to a BytesIO buffer
        edited_image_buffer = BytesIO()
        seal_image.save(edited_image_buffer, format="JPEG")
        edited_image_buffer.seek(0)

        # Send edited image as a file
        await ctx.send(file=discord.File(edited_image_buffer, filename="seal_avatar.jpg"))
    except Exception as e:
        await ctx.send(f"Error occurred: {e}")

seal_species = {
    "Harbor seal": "https://media.discordapp.net/attachments/1092978456196829265/1094222110626435163/IMG_0365.jpg",
    "Gray seal": "https://media.discordapp.net/attachments/1092978456196829265/1094222419717275659/image0.jpg",
    "Harp seal": "https://media.discordapp.net/attachments/1092978456196829265/1094223176701059172/IMG_0366.jpg",
    "Ringed seal": "https://media.discordapp.net/attachments/1092978456196829265/1094223706924011601/image0.jpg",
    "Leopard seal": "https://media.discordapp.net/attachments/1092978456196829265/1094224036667600956/image0.jpg"
}      
@client.hybrid_command(name="sealgame", description="Guess the species of seals")
async def guess_seal(ctx):
    try:
        score = 0
        await ctx.send("Welcome to Guess the Seal Species game! Let's get started.")
        for i in range(5):
            species = random.choice(list(seal_species.keys()))
            image_url = seal_species[species]
            response = requests.get(image_url)
            with open("seal_image.jpg", "wb") as f:
                f.write(response.content)
            with open("seal_image.jpg", "rb") as f:
                await ctx.send(f"What species of seal is this?", file=discord.File(f))
            response = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author)
            if response.content.lower() == species.lower():
                await ctx.send("Correct!")
                score += 1
            else:
                await ctx.send(f"Incorrect. The correct answer is {species}.")
        
        if score == 5:
            await ctx.send("Well done! You guessed all the species correctly!")
        else:
            await ctx.send(f"You guessed {score} out of 5 species correctly. Try again!")
    
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Try again later.")

    except Exception as e:
        await ctx.send(f"Error occurred: {e}")

# Define the seal species dictionary
seal_species = {
    'Harbor Seal': {
        'Description': 'The harbor seal, also known as the common seal, is a true seal found along the coastal regions of the Northern Hemisphere. It has a characteristic V-shaped nostrils and a spotted coat.',
        'Scientific Name': 'Phoca vitulina',
        'Habitat': 'Coastal waters, including estuaries, bays, and harbors.',
        'Conservation Status': 'Least Concern',
        'Interesting Fact': 'Harbor seals are excellent divers and can stay submerged for up to 30 minutes while hunting for food.'
    },
    'Gray Seal': {
        'Description': 'The gray seal is a large seal species found in the North Atlantic Ocean. It has a long, robust body with a distinctive horseshoe-shaped nostrils and a mottled coat.',
        'Scientific Name': 'Halichoerus grypus',
        'Habitat': 'Coastal waters and offshore areas of the North Atlantic Ocean.',
        'Conservation Status': 'Least Concern',
        'Interesting Fact': 'Gray seals are known for their unique mating behavior called "rookery", where multiple males compete for a female and form harems.'
    },
    'Southern Elephant Seal': {
        'Description': 'The southern elephant seal is the largest seal species and one of the most sexually dimorphic mammals, with males weighing up to 4,000 kg and females weighing around 900 kg. They are found in the Southern Ocean and sub-Antarctic islands.',
        'Scientific Name': 'Mirounga leonina',
        'Habitat': 'Southern Ocean and sub-Antarctic islands.',
        'Conservation Status': 'Least Concern',
        'Interesting Fact': 'Southern elephant seals can hold their breath for up to 120 minutes, making them the champion divers among marine mammals.'
    },
    'Weddell Seal': {
        'Description': 'The Weddell seal is a distinctive seal species found in the Antarctic region. It has a stocky body, a small head, and a spotted coat with a unique pattern of black spots on a light background.',
        'Scientific Name': 'Leptonychotes weddellii',
        'Habitat': 'Antarctic region, including pack ice and fast ice.',
        'Conservation Status': 'Least Concern',
        'Interesting Fact': 'Weddell seals are known for their exceptional diving ability and can dive to depths of up to 600 meters and stay submerged for over an hour.'
    },
    'Bearded Seal': {
        'Description': 'The bearded seal is a large seal species found in the Arctic and sub-Arctic regions. It has a stocky body, a broad head, and long, curved whiskers that give it a distinctive "bearded" appearance.',
        'Scientific Name': 'Erignathus barbatus',
        'Habitat': 'Arctic and sub-Arctic regions, including pack ice and coastal areas.',
        'Conservation Status': 'Least Concern',
        'Interesting Fact': 'Bearded seals are known for their unique vocalizations, which include various calls, songs, and underwater vocal displays.'
 }
}

@client.hybrid_command(name='sealinfo', description='Get information about different species of seals')
async def get_seal_info(ctx, species: str):
    # Check if the specified species exists in the dictionary
    if species in seal_species:
        # Get the information for the specified species
        species_info = seal_species[species]

        # Create an embedded message with the species information
        embed = discord.Embed(
            title=f'{species} Information',
            description=species_info['Description'],
            color=discord.Color.blue()
        )
        embed.add_field(name='Scientific Name', value=species_info['Scientific Name'], inline=False)
        embed.add_field(name='Habitat', value=species_info['Habitat'], inline=False)
        embed.add_field(name='Conservation Status', value=species_info['Conservation Status'], inline=False)
        embed.add_field(name='Interesting Fact', value=species_info['Interesting Fact'], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'Species not found. Available species: {", ".join(seal_species.keys())}')

@client.hybrid_command(name='membercount', description='Get the member count of the guild')
async def membercount(ctx):
    # Get the member count of the guild
    guild = ctx.guild
    member_count = guild.member_count
    online_member_count = len([m for m in guild.members if m.status != discord.Status.offline])

    # Create an embedded message with the member count information
    embed = discord.Embed(
        title='',
        color=discord.Color.from_rgb(42,45,49)  
    )
   
    # Set the thumbnail image for the embedded message
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1070822894675951616/1092912035613917294/seal-5882547_1280.png')
    # Add the member count as a field in the embedded message
    embed.add_field(name='Members', value=member_count, inline=True)
    embed.add_field(name='Online', value=online_member_count, inline=True)
    await ctx.send(embed=embed)


client.run("TOKEN HERE")
