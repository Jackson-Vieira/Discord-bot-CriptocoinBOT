import discord 

from discord.ext import tasks  
from os import linesep

from settings import KEY_CHANNEL, TOKEN
from api_binance import api_binance


client = discord.Client()

"""
Função primária que Inicializa todas as funções requeridas para o funcionamento do bot
"""
@client.event
async def on_ready():
    print(f"I'm ready {client.user.name}!")
    bot_presence.start()
    bot_chat.start()

"""
Função geradora que é ativada quando um usuario digita "$info "
"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    name = message.author.name
    if message.content.startswith('$info '):
        await message.channel.send(f'Hello, {name}!')
        
"""
Função que é ativada a cada 4 horas e mostrar as cotações atualizadas no canal expecificado
"""
@tasks.loop(hours = 4)
async def bot_chat():
    coins = api_binance()
    
    try:
        response = ['{} $ {:.3f} '.format(coin, float(price)) for coin, price in coins.items()]
        channel = client.get_channel(KEY_CHANNEL)
        message = linesep.join(response)
        await channel.send(message)

    except:
        print("UNABLE TO CONNECT TO API")
        
"""
Função que mostra as cotações atualizadas a cada minuto na atividade do bot
"""
@tasks.loop(minutes=1)
async def bot_presence():
    coins = api_binance()

    try:
        BTC, ETH = coins['BTCDAI'], coins['ETHDAI']
        activity = "BTC ₿$ {:.2f} & ETH ⟠$ {:.2f}".format(float(BTC), float(ETH))
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))

    except:
        print("UNABLE TO CONNECT TO API")

client.run(TOKEN) 
