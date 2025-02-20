import discord
import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from discord.ext import commands
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

participant_list = []
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print("The bot is now ready for use!")
    print("---------------")


@client.command()
async def ask(ctx):
    await ctx.send("What's your favorite color?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30.0)
        embed = discord.Embed(
        title="Favorite color",
        description= f"Your favorite color is {message.content}",
        color=discord.Color.red()  
        )
        await ctx.send(embed=embed)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")

@client.command()
async def eternal(ctx):
    await ctx.send("An organization that provides the tools for anyone to reach their potential.")


@client.command()
async def inviteBot(ctx):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=1317511758486700045 Copy this link to add your bot to the server")
    
@client.command()
async def org_data(ctx, number: int, organization_name: str):
    
    

    club_trophy_list = []
    club_list = []
    

    
    
    def mean(Club_trophy_List,is2DList):
        numList = []
        if is2DList:
            for club in Club_trophy_List:
                for trophy in club:
                    numList.append(trophy)
        else:
            for trophy in Club_trophy_List:
                numList.append(trophy)
        sum = 0
        for num in numList:
            sum = sum + num
        return sum / len(numList)
            
    def median(Club_trophy_List, is2DList):
        numList = []
        if is2DList:
            for club in Club_trophy_List:
                for trophy in club:
                    numList.append(trophy)
        else:
            for trophy in Club_trophy_List:
                numList.append(trophy)

        
        numList.sort()
        if ((len(numList) % 2) == 1):
            median_index = int((len(numList)/2.0))
            return numList[median_index]
        else:
            Index1 = int((len(numList) / 2.0)) - 1
            Index2 = int((len(numList) / 2.0))
            return (numList[Index1] + numList[Index2]) / 2.0
    
    def check2d(List):
        try:
            sum(List, [])
            return True
        except:
            return False    
    
    def count(Club_trophy_List,is2DList):
        numList = []
        if is2DList:
            for club in Club_trophy_List:
                for trophy in club:
                    numList.append(trophy)
        else:
            for trophy in Club_trophy_List:
                numList.append(trophy)
        return len(numList)
    def minumum(Club_trophy_List, is2DList):
        numList = []
        if is2DList:
            for club in Club_trophy_List:
                for trophy in club:
                    numList.append(trophy)
        else:
            for trophy in Club_trophy_List:
                numList.append(trophy)
        numList.sort()
        return numList[0]
    def maximum(Club_trophy_List, is2DList):
        numList = []
        if is2DList:
            for club in Club_trophy_List:
                for trophy in club:
                    numList.append(trophy)
        else:
            for trophy in Club_trophy_List:
                numList.append(trophy)
        numList.sort()
        return numList[len(numList) - 1]
    def firstQuatile(Club_trophy_List, is2DList):
    
        numList = []
        if is2DList:
            for club in Club_trophy_List:
                for trophy in club:
                    numList.append(trophy)
        else:
            for trophy in Club_trophy_List:
                numList.append(trophy)
            
        numList.sort()
        median = 0
        if ((len(numList) % 2) == 1):
            median_index = int((len(numList)/2.0))
            median = numList[median_index]
        else:
            Index1 = int((len(numList) / 2.0)) - 1
            Index2 = int((len(numList) / 2.0))
            median = (numList[Index1] + numList[Index2]) / 2
        try:
            indexOfMedian = numList.index(median)
            firstIndex = int(indexOfMedian / 2.0 + 0.5) 
            secondIndex = int(indexOfMedian / 2.0 - 0.5)
        
            return (numList[firstIndex] + numList[secondIndex]) / 2
        except:
            halfLength = len(numList) / 2
            indexOf1stQuatile = int(halfLength / 2 + 0.5)
        
            return numList[indexOf1stQuatile]

    def thirdQuatile(Club_trophy_List, is2DList):
    
        numList = []
        if is2DList:
            for club in Club_trophy_List:
                for trophy in club:
                    numList.append(trophy)
        else:
            for trophy in Club_trophy_List:
                numList.append(trophy)
        numList.sort()
        median = 0
        if ((len(numList) % 2) == 1):
            median_index = int((len(numList)/2.0))
            median = numList[median_index]
        else:
            Index1 = int((len(numList) / 2.0)) - 1
            Index2 = int((len(numList) / 2.0))
            median = (numList[Index1] + numList[Index2]) / 2
        try:
            indexOfMedian = numList.index(median)
            firstIndex = int(((indexOfMedian + len(numList)) / 2) + 0.5)
            secondIndex = int(((indexOfMedian + len(numList)) / 2) - 0.5)
        
            return (numList[firstIndex] + numList[secondIndex]) / 2
        except:
            halfLength = len(numList) / 2
            indexOf3rdQuatile = int((halfLength + len(numList))/2 + 0.5)

            return numList[indexOf3rdQuatile]


    
    for i in range(number):
    
        await ctx.send("Enter your Club Tag. For example, 2UUGC0LVQ.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            club_tag = await client.wait_for('message', check=check, timeout=180.0)
        except asyncio.TimeoutError:
            await ctx.send("You took too long")


        API_Key = os.getenv("API_Key")
        headers = {
            'Authorization': f'Bearer {API_Key}'
        }
        club_tag = club_tag.content
        response = requests.get(f'https://api.brawlstars.com/v1/clubs/%23{club_tag}', headers=headers)
        data = response.json()
        club_members = data["members"]
        trophy_list = []
        for member in club_members:
            trophy_list.append(member["trophies"])
            
        club_trophy_list.append(trophy_list)
        club_list.append(data["name"])
    if number > 1:
        for i in range(len(club_trophy_list)):
            
            embed = discord.Embed(
            title=f"{club_list[i]}",
            description= f"Member Count - {str(count(club_trophy_list[i], check2d(club_trophy_list[i])))}\n Median Trophies - {str(median(club_trophy_list[i], check2d(club_trophy_list[i])))}\n The 25 percentile's Trophies - {str(firstQuatile(club_trophy_list[i], check2d(club_trophy_list[i])))}\n The 75 percentile's Trophies - {str(thirdQuatile(club_trophy_list[i], check2d(club_trophy_list[i])))} \n Mean Trophies - {str(mean(club_trophy_list[i], check2d(club_trophy_list[i])))}\n Max Trophies - {str(maximum(club_trophy_list[i], check2d(club_trophy_list[i])))}\n Min Trophies - {str(minumum(club_trophy_list[i], check2d(club_trophy_list[i])))} ",
            color=discord.Color.red()  
            )
            await ctx.send(embed=embed)
            
    
    embed1 = discord.Embed(
    title = organization_name,
    description= f"Member Count - {str(count(club_trophy_list, check2d(club_trophy_list)))}\n Median Trophies - {str(median(club_trophy_list, check2d(club_trophy_list)))}\n The 25 percentile's Trophies - {str(firstQuatile(club_trophy_list, check2d(club_trophy_list)))}\n The 75 percentile's Trophies - {str(thirdQuatile(club_trophy_list, check2d(club_trophy_list)))} \n Mean Trophies - {str(mean(club_trophy_list, check2d(club_trophy_list)))}\n Max Trophies - {str(maximum(club_trophy_list, check2d(club_trophy_list)))}\n Min Trophies - {str(minumum(club_trophy_list, check2d(club_trophy_list)))} ",
    color=discord.Color.red()  
    )
    await ctx.send(embed=embed1)

        




@client.command()
async def create_bracket(ctx, names: str, bracket_size: int):
    name_list = []
    bracket_list = []
    def checkComma(comma):
        if comma == ",":
            return True
        return False


    def sortNames(names):
        
        startingIndex = 0 
        i = 0
        while (i < len(names)):
    
                if(i + 1 == len(names) or checkComma(names[i + 1])):
                    name_list.append(names[startingIndex:i + 1])
                    startingIndex = i + 2
                i = i + 1
    
    

    
    sortNames(names)
    for i in range(bracket_size):
        bracket_list.append("bye")
    
    j = 0
    times = len(name_list)
    while j < times :        
        index = random.randint(0,len(name_list) - 1)
        index2 = random.randint(0,len(bracket_list) - 1)
        if bracket_list[index2] == "bye":
            bracket_list[index2] = name_list[index]
            name_list.remove(name_list[index])
            j = j + 1
    
  
    img = Image.new('RGB', (700, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    
    font = ImageFont.truetype("arial.ttf", 8)
    text_color = (0, 0, 0)
    
    tries = bracket_size
    if bracket_size == 16:
        
        y = 0
        y2 = 10
        y3 = 10
        x = 0
        x2 = 50
        for i in range(tries):
            draw.text((10,y),text=bracket_list[i],fill=text_color, font=font)
            y = y + 50
            draw.line((x, y2, x2, y2), fill='black', width=1)
            y2 = y2 + 50
        tries = int(tries / 2)
        for i in range(tries):
            draw.line((x2, y3, x2, y3+50), fill='black', width=1)
            y3 = y3 + 100
        x = x + 50
        x2 = x2 + 50
        
        y2 = 35
        y3 = 35
        for i in range(tries):
            draw.line((x, y2, x2, y2), fill='black', width=1)
            
            y2 = y2 + 100
        tries = int(tries/2)
        for i in range(tries):
            draw.line((x2, y3, x2, y3+100), fill='black', width=1)
            y3 = y3 + 200
        x = x + 50
        x2 = x2 + 50
        y2 = 80
        y3 = 80
        for i in range(tries):
            draw.line((x, y2, x2, y2), fill='black', width=1)
            y2 = y2 + 200
        
        tries = int(tries/2)
        
        for i in range(tries):
            draw.line((x2, y3, x2, y3+200), fill='black', width=1)
            y3 = y3 + 400
        x = x + 50
        x2 = x2 + 50
        y2 = 180
        y3 = 180
        for i in range(tries):
            draw.line((x, y2, x2, y2), fill='black', width=1)
            y2 = y2 + 400
        tries = int(tries/2)
        for i in range(tries):
            draw.line((x2, y3, x2, y3+400), fill='black', width=1)
            y3 = y3 + 400
        x = x + 50
        x2 = x2 + 50
        y2 = 400
        y3 = 180
        for i in range(tries):
            draw.line((x, y2, x2, y2), fill='black', width=1)

            
        
    
   
    img.save("generated_image.png")
    
    
    with open("generated_image.png", "rb") as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

SPECIFIC_CHANNEL_ID = 1270196994660630531
@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.channel.id == SPECIFIC_CHANNEL_ID and "hello" in message.content.lower():
        username = message.author.name
        true = True
        for i in range(len(participant_list)):
            if username == participant_list:
                true = False
        if true:
            participant_list.append(username)
            


    
    await client.process_commands(message)

@client.command()
async def giveNames(ctx):
    message = (participant_list[0])
    for i in range(len(participant_list) - 1):
        message = message + "," + participant_list[i+1]
    await ctx.send(message)

@client.command()
async def update_bracket(ctx, names: str, amount_of_people: int, image_url: str = None):
    name_list = []
    def checkComma(comma):
        if comma == ",":
            return True
        return False
    def sortNames(names):
        
        startingIndex = 0 
        i = 0
        while (i < len(names)):
    
                if(i + 1 == len(names) or checkComma(names[i + 1])):
                    name_list.append(names[startingIndex:i + 1])
                    startingIndex = i + 2
                i = i + 1
    if not image_url:
        await ctx.send("Please provide an image URL.")
        return

    try:
        
        response = requests.get(image_url)
        response.raise_for_status()  
        image_data = BytesIO(response.content)  
        image = Image.open(image_data) 
    except requests.exceptions.MissingSchema:
        await ctx.send("Invalid URL. Please provide a valid image URL.")
        return
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Failed to download the image. Error: {e}")
        return
    except Exception as e:
        await ctx.send(f"Failed to process the image. Error: {e}")
        return

    
    
    draw = ImageDraw.Draw(image)
    
    
    font = ImageFont.truetype("arial.ttf", 8)
    text_color = (0, 0, 0) 
    
    
    
    if amount_of_people == 8:
        sortNames(names)
        y = 16
        x = 40
        for i in range(amount_of_people):
            draw.text((x, y), text=name_list[i], fill=text_color, font=font)
            y = y + 72
    if amount_of_people == 4:
        sortNames(names)
        y = 49
        x = 80
        for i in range(amount_of_people):
            draw.text((x, y), text=name_list[i], fill=text_color, font=font)
            y = y + 144
    if amount_of_people == 2:
        sortNames(names)
        y = 120
        x = 110
        for i in range(amount_of_people):
            draw.text((x, y), text=name_list[i], fill=text_color, font=font)
            y = y + 288.5
    if amount_of_people == 1:
        sortNames(names)
        y = 280
        x = 145
        for i in range(amount_of_people):
            draw.text((x, y), text=name_list[i], fill=text_color, font=font)
            

    edited_image = BytesIO()
    image.save(edited_image, format="PNG")
    edited_image.seek(0)  
    file = discord.File(fp=edited_image, filename="edited_image.png")
    await ctx.send("Here is the updated bracket:", file=file)


@client.command()
async def fetch_messages(ctx, limit: int = 150):
    messages = []
    Ban_list = ""
    async for msg in ctx.channel.history(limit=limit):
        messages.append(msg)

    for message in messages:
        Ban_list = Ban_list + f"{message.content}" + ", "

    await ctx.send(Ban_list)  
        
#@client.event
#async def on_member_join(member):

    #GUILD_ID = 1241564359344394412 
    #if member.guild.id == GUILD_ID:
        #channel_id = 1316802984876970024 
        #tournament_id = 1316883731822149704
        #tickets_id = 1316892491802218578
        #clubs_id = 1316880785248227390
        #teams_id = 1316892572932767754
        #socials_id = 1316883296638079036

        #channel = client.get_channel(channel_id)
        #Socials = client.get_channel(socials_id)
        #tournaments = client.get_channel(tournament_id)
        #tickets = client.get_channel(tickets_id)
        #clubs = client.get_channel(clubs_id)
        #teams = client.get_channel(teams_id)
        #if channel:
            #await channel.send(f"Hello! {member.mention}  Welcome to the Eternal Discord Server!\nThe tournament password is in {tournaments.mention}")
#@client.event
#async def on_member_update(before, after):       
        #if len(after.roles) > len(before.roles):
         
            #new_roles = [role for role in after.roles if role not in before.roles]
            #club_role_numbers = [1316902490364444813,1316908574290608148,1316909740294406144,1316914501127503923,1316903158592831562,1274899010288877629,1316912554458615839,1316909628940095621,1316909681083547700,1316902805851865140,1310827102114680894,1306776640109547560,1316912861813018644,1316912901109317662,1316912977881862219,1316913026787708981,1311000365960925277,1316913142487584849,1306059264699404348,1241571856079917137,1325651200171048960,1325543853498830881,1328041342198349907]
            #club_mail = client.get_channel(1316886078342565988)
            #number = 0
            #i = 0
            #j = 0
            #if len(new_roles) >= 2:
                #while number < 2 and j < 2:
                    #if i > len(club_role_numbers) - 1:
                        #i = 0
                        #j = j + 1
                    #if new_roles[number].id == club_role_numbers[i]:
                        #number = number + 1
                    #i = i + 1
                #if j != 2:
                    #club_chat = client.get_channel(1316887520839204925)
                
                    #if club_chat:
                        #await club_chat.send(f"Welcome, {after.mention}! You've been granted the club member role! The password for the club tournament is in {club_mail.mention}")
          
                

        


Bot_Token = os.getenv("Bot_Token")
client.run(Bot_Token)
