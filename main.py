import discord
from discord.ext import commands
import random
from discord.utils import get
import asyncio


PREFIX = '+'
emojiCrackCat = ':clap:'

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event
async def on_ready():
    print( 'Bot ready to work, logged as {0.user}'.format(client) )
    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'Насилование Дениски' ) )

@client.command(pass_context = True)
async def help( ctx ):
    emb = discord.Embed( title = 'Список команд', colour = discord.Color.dark_green())

    emb.add_field( name = '{}guess'.format(PREFIX), value = 'Игра "Угадай число"\n')
    emb.add_field( name ='{}dice'.format(PREFIX), value='Крутануть кубик\n')
    emb.add_field( name ='{}hardtroll'.format(PREFIX), value='Троллинг(нужен ключ)\n')
    emb.add_field( name ='{}RPS'.format(PREFIX), value='Камень, Ножницы, Бумага\n')
    emb.add_field( name ='{}math'.format(PREFIX), value='Матеша на скорость')

    await ctx.send( embed = emb )

@client.command(pass_context = True)
async def guess(ctx):
    emb = discord.Embed( title = 'Угадай число от 1 до 100.', colour = discord.Color.gold())
    await ctx.send( embed = emb )

    answer = random.randint(1, 100)
    trys = 0

    try:
        while trys < 10:
            trys += 1
            guess = await client.wait_for('message')
            if int(guess.content) < answer:
                emb1 = discord.Embed( title = 'Меньше чем нужно...', colour = discord.Color.teal())
                await ctx.send( embed = emb1 )
            elif int(guess.content) > answer:
                emb2 = discord.Embed( title = 'Больше чем нужно...', colour = discord.Color.orange())
                await ctx.send( embed = emb2 )
            elif int(guess.content) == answer:
                break
        if int(guess.content) == answer:
            emb3 = discord.Embed( title = 'Ты угадал! Попыток ушло: {}'.format(trys), colour = discord.Color.green())
            await ctx.send( embed = emb3 )
        else:
            emb4 = discord.Embed( title = 'Ты проиграл. Я загадал число {}'.format(answer), colour = discord.Color.red())
            await ctx.send( embed = emb4 )
    except Exception:
        emb5 = discord.Embed( title = 'Ошибка! Перезапустите игру.', colour = discord.Color.dark_grey())
        await ctx.send( embed = emb5 )


@client.command(pass_context = True)
async def dice(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split(','))
    except Exception:
        emb = discord.Embed( title = 'Команда должа записана в формате Число,Число!', colour = discord.Color.red())
        await ctx.send( embed = emb )
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    emb1 = discord.Embed( title = result, colour = discord.Color.green())
    await ctx.send( embed = emb1 )

@client.command( pass_context = True )
async def hardtroll(ctx, troll: str, content='@everyone'):
    allow = 1
    try:
        key, times = map(int, troll.split(','))
        if key != 236751654453:
            emb = discord.Embed( title = 'Неверный ключ!', colour = discord.Color.red())
            await ctx.send(embed = emb)
            allow = 0

        if allow == 1:
            for i in range(times):
                await ctx.send(content)
        else:
            pass
    except Exception:
        emb = discord.Embed( title = 'Ошибка! Введит команду в формате Ключ,Число.', colour = discord.Color.red())
        await ctx.send(embed = emb)

@client.command(pass_context = True)
async def RPS(ctx):
    emb = discord.Embed( title = 'Камень, ножницы или бумага?(1/2/3)', colour = discord.Color.gold())
    emb1 = discord.Embed( title = 'Ничья!', colour = discord.Color.dark_gray())
    emb2 = discord.Embed( title = 'Ты выиграл!', colour = discord.Color.green())
    emb3 = discord.Embed( title = 'Ты лох. Как можно слить боту?', colour = discord.Color.dark_red())
    emb5 = discord.Embed( title = 'А не много ли?)', colour = discord.Color.red())

    try:
        botAnsw = random.randint(1, 3)
        await ctx.send(embed = emb)
        clientAnsw = await client.wait_for('message')
        if botAnsw == int(clientAnsw.content):
            await ctx.send(embed = emb1)

        elif int(clientAnsw.content) == 1 and botAnsw == 2 \
            or int(clientAnsw.content) == 2 and botAnsw == 3 \
            or int(clientAnsw.content) == 3 and botAnsw == 1:
            await ctx.send(embed = emb2)

        elif int(clientAnsw.content) > 3 and int(clientAnsw.content) != 666:
            await ctx.send(embed = emb5)

        elif int(clientAnsw.content) == 666:
            await ctx.send(':japanese_ogre:')

        else:
            await ctx.send(embed = emb3)

    except Exception:
        if str(clientAnsw.content) == '+RPS':
            await ctx.send('Эм... Ну типо перезапускаю.')
        else:
            emb4 = discord.Embed( title = '{} - ПОЛНАЯ хуйня'.format(str(clientAnsw.content)), colour = discord.Color.red())
            await ctx.send(embed = emb4)

@client.command( pass_context = True )
async def math(ctx):
    RightAnsw = 0
    run = True

    try:
        while run:
            a = random.randint(1, 30)
            b = random.randint(1, 30)
            sign = random.randint(1, 2)
            if sign == 1:
                c = a + b
                emb = discord.Embed( title = str(a) + ' + ' + str(b) + ' ? :', colour = discord.Color.gold())
                await ctx.send(embed = emb)
                HumAnsw = await client.wait_for('message', timeout = 5.0)
                if int(HumAnsw.content) == c:
                    RightAnsw += 1
                else:
                    await ctx.send('Ты проиграл! Ты смог решить примеров!: ' + str(RightAnsw))
                    run = False
            else:
                c = a - b
                emb1 = discord.Embed( title = str(a) + ' - ' + str(b) + ' ? :', colour = discord.Color.gold())
                await ctx.send(embed = emb1)
                HumAnsw = await client.wait_for('message', timeout = 5.0)
                if int(HumAnsw.content) == c:
                    RightAnsw += 1
                else:
                    await ctx.send('Ты проиграл! Ты смог решить примеров!: ' + str(RightAnsw))
                    run = False

    except asyncio.TimeoutError:
        await ctx.send('Время вышло! Ты смог решить {} примеров!'.format(RightAnsw))
    except ValueError:
        await ctx.send('Цифру нужно вводить лол. Ты смог решить {} примеров!'.format(RightAnsw))



token = 'ODA4NDIyNTAyNjUyMzEzNjMz.YCGUIA.vmNgIdw2GZ853XAd-k7cYsLK0xA'
client.run( token )
