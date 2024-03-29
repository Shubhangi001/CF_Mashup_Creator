import discord
import requests
import os
import random
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
from datetime import datetime


# from keep_alive import keep_alive

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_member_join(member):
  #When a member joins the discord, they will get mentioned with this welcome message
  await member.create_dm()
  await member.dm_channel.send(
    f'Hi {member.name}, welcome to our Discord server!\nYou can start with $help command to start using the Mashup Bot.'
  )


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$mashup'):

    def check(m):
      return m.author == message.author and m.channel == message.channel

    helpC = discord.Embed(
      title="CF Mashup Bot\n",
      description=
      "Enter the ratings of problems you want to add to the mashup separated by a space",
      color=0x00ff00)
    await message.channel.send(embed=helpC)
    # await message.channel.send("Enter the ratings of problems you want to add to the mashup separated by a space")
    try:
      try:
        try:
          ratings = await client.wait_for('message', check=check, timeout=300)
        except:
          helpC = discord.Embed(title="CF Mashup Bot\n",
                                description="Timeout error",
                                color=0xff0000)
          await message.channel.send(embed=helpC)
          return

        ratings = ratings.content.split()
        m = len(ratings)
        for i in range(m):
          ratings[i] = int(ratings[i])
      except:
        helpC = discord.Embed(title="CF Mashup Bot\n",
                              description="Invalid ratings",
                              color=0xff0000)
        await message.channel.send(embed=helpC)
        # await message.channel.send("Invalid ratings")
        return
      solved_problems = set()
      problems_list = []
      helpC = discord.Embed(
        title="CF Mashup Bot\n",
        description="Enter the users' profile handles separated by a space",
        color=0x00ff00)
      await message.channel.send(embed=helpC)
      # await message.channel.send("Enter the users' profile handles separated by a space")
      # handles = []
      handles = await client.wait_for('message', check=check)
      t1 = datetime.now()

      # print(h)
      # if (handles.startswith("```")):
      #   handles = handles[3:-3]
      handles = handles.content.split()
      # print(handles)
      n = len(handles)
      for i in range(n):
        try:
          response = requests.get(
            'https://codeforces.com/api/user.status?handle=' + handles[i])
          result = response.json()['result']
        except:
          helpC = discord.Embed(title="CF Mashup Bot\n",
                                description="Invalid handle: " + handles[i],
                                color=0xff0000)
          await message.channel.send(embed=helpC)
          # await message.channel.send("Invalid handle: "+handles[i])
          return
        for j in range(len(result)):
          try:
            if result[j]['verdict'] == 'OK' and result[j]['problem'][
                'rating'] in ratings:
              x = frozenset({
                result[j]['problem']['contestId'],
                result[j]['problem']['index']
              })
              solved_problems.add(x)
          except:
            pass
      response = requests.get('https://codeforces.com/api/problemset.problems')
      result = response.json()['result']['problems']
      helpC = discord.Embed(title="CF Mashup Bot\n",
                            description="Problems for given ratings are",
                            color=0x00ff00)
      for i in range(len(ratings)):
        problems = ""
        problems_list.append(str(ratings[i]) + ": ")
        cnt = 0
        for j in range(len(result)):
          try:
            if (result[j]['rating'] == ratings[i]):
              contestid = result[j]['contestId']
              index = result[j]['index']
              x = frozenset({contestid, index})
              if x not in solved_problems and x not in problems_list:
                problems_list.append(x)
                x = '(https://codeforces.com/problemset/problem/' + str(
                  contestid) + '/' + str(index) + ')'
                y = '[' + str(contestid) + str(index) + ']'
                problems += (y + x)
                cnt += 1
                if (cnt != 3):
                  problems += " , "
                if cnt == 3:
                  break
          except:
            pass
        # +str((datetime.now()-t1).total_seconds())   #5.93 seconds
        helpC.add_field(name=str(ratings[i]), value=problems, inline=False)
      await message.channel.send(embed=helpC)
    except:
      #red color embed

      helpC = discord.Embed(title="CF Mashup Bot\n",
                            description="Some unknown error occured",
                            color=0xff0000)
      await message.channel.send(embed=helpC)
      # await message.channel.send("Invalid inputs given")

    happyemojis = [
      '\U0001F600', '\U0001f600', '\U0001F917', '\U0001F607', '\U0001F60A'
    ]
    await message.channel.send("Thank you for using me!" +
                               random.choice(happyemojis))

  if message.content.startswith('$help'):
    helpC = discord.Embed(
      title="CF Mashup Bot \nHelp Guide",
      description=
      "Discord bot built for the purpose of assistance in creating a mashup of problems from codeforces with a given set of ratings which are unsolved by the given set of users.",
      color=0x00ff00)
    helpC.add_field(
      name="Mashup",
      value=
      "To use this command type $mashup, then mention the ratings of problems and the users participating in the mashup.",
      inline=False)
    helpC.add_field(name="Help",
                    value="To use this command type $help",
                    inline=False)
    await message.channel.send(embed=helpC)



load_dotenv(".env")
TOKEN = os.getenv("DISC_TOKEN")
client.run(TOKEN)
