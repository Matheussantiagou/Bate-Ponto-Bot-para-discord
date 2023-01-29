import discord
import asyncio
from datetime import datetime

import pytz

br_tz = pytz.timezone('America/Sao_Paulo')

client = discord.Client(intents=discord.Intents.all())

last_message_date_entry = {}
last_message_date_out = {}


@client.event
async def on_ready():
  print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
  user = message.author
  today = datetime.now(br_tz).date()
  if message.content.startswith('!entrada'):
    if user.id in last_message_date_entry:
      if last_message_date_entry[user.id] == today:
        bot_msg = await message.channel.send(
          f"{user.mention}, você já enviou uma mensagem hoje.")
        await message.delete(delay=3)
        await bot_msg.delete(delay=3)
        return
    last_message_date_entry[user.id] = today

    time = datetime.now(br_tz).strftime(":clock9: %H:%M:%S no dia %d/%m/%y")
    if not message.channel.permissions_for(message.author).send_messages:
      print("Usuário não tem permissão para enviar mensagens no canal.")
      return

    try:
      await message.channel.send(
        f':green_square:  {user.mention} marcou a entrada às {time} :green_square:  '
      )
      await message.delete()
    except discord.Forbidden:
      print("Não tenho permissão para enviar mensagens neste canal.")
    except discord.HTTPException as e:
      print(f'Erro ao enviar mensagem: {e}')

  if message.content.startswith('!saida'):
    if user.id in last_message_date_out:
      if last_message_date_out[user.id] == today:
        bot_msg = await message.channel.send(
          f"{user.mention}, você já enviou uma mensagem hoje.")
        await message.delete(delay=3)
        await bot_msg.delete(delay=3)
        return
    last_message_date_out[user.id] = today

    time = datetime.now(br_tz).strftime(":clock9: %H:%M:%S no dia %d/%m/%y")
    if not message.channel.permissions_for(message.author).send_messages:
      print("Usuário não tem permissão para enviar mensagens no canal.")
      return

    try:
      await message.channel.send(
        f':red_square: {user.mention} marcou a saída às {time} :red_square: ')
      await message.delete()
    except discord.Forbidden:
      print("Não tenho permissão para enviar mensagens neste canal.")
    except discord.HTTPException as e:
      print(f'Erro ao enviar mensagem: {e}')


client.run('YOUR_TOKEN_HERE')
