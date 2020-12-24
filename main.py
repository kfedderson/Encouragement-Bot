import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()
sadWords = ["sad","depressed","unhappy","miserable","fear","evil","mad","angry"]

starterEncouragements = [
  "Don't worry, be happy",
  "Everything will be ok",
  "Jesus loves you",

]

def getQuote():
  response = requests.get("https://zenquotes.io/api/random")
  jsonData = json.loads(response.text)
  quote = jsonData[0]['q'] + " -" + jsonData[0]['a']
  return quote


def updateEncouragements(message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [message]


def deleteEncouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('{0.user} has been logged in.'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$uplift'):
    quote = getQuote()
    await message.channel.send(quote)
    print('Message sent')

  options = starterEncouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]


  if any(word in msg for word in sadWords):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    new_message = msg.split("$new ",1)[1]
    updateEncouragements(new_message)
    await message.channel.send("New message was added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      deleteEncouragements(index)
      encouragements = db["encouragements"]
      print('Message at index {0} has been deleted'.format(index))
    await message.channel.send(encouragements)

client.run(os.getenv('TOKEN'))