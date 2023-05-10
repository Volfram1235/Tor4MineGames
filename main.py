import discord
from discord.ext import commands
import random
import asyncio
import json
import time

# префикс бота
PREFIX = '!'

# Права бота
rights = discord.Intents.all()

# типо тут переменная такая клиент
client = commands.Bot(command_prefix=PREFIX, intents=rights)
client.remove_command('help')

#данные об игроках
with open('discord_math_records.json', 'r') as file:
    data_stats = json.load(file)

# запускаем бота
@client.event
async def on_ready():
    print('Bot ready to work, logged as {0.user}'.format(client))
    # и пишем чем занимается бот
    activity = discord.Activity(name='на мужские яица', type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)

# команда help
@client.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Список команд', colour=discord.Color.dark_green())

    emb.add_field(name='{}guess'.format(PREFIX), value='Игра "Угадай число"',inline= False)
    emb.add_field(name='{}dice'.format(PREFIX), value='Крутануть кубик',inline= False)
    emb.add_field(name='{}math'.format(PREFIX), value='Матеша на скорость',inline= False)
    emb.add_field(name='{}choose'.format(PREFIX), value='Выберу что-нибудь из списка',inline= False)
    emb.add_field(name='{}mathstat'.format(PREFIX), value='Рекорды игры "Матеша на скорость"',inline= False)

    await ctx.send(embed=emb)

# команда для старта игры угадай число
@client.command(pass_context=True)
async def guess(ctx):
    emb = discord.Embed(title='Угадай число от 1 до 100.', colour=discord.Color.gold())
    await ctx.send(embed=emb)

    answer = random.randint(1, 100)
    trys = 0

    # try нужно, чтобы бот смог дедектить ошибки
    try:
        while trys < 10:
            trys += 1
            guess = await client.wait_for('message')
            if int(guess.content) < answer:
                emb1 = discord.Embed(title='Меньше чем нужно...', colour=discord.Color.teal())
                await ctx.send(embed=emb1)
            elif int(guess.content) > answer:
                emb2 = discord.Embed(title='Больше чем нужно...', colour=discord.Color.orange())
                await ctx.send(embed=emb2)
            elif int(guess.content) == answer:
                break
        if int(guess.content) == answer:
            emb3 = discord.Embed(title='Ты угадал! Попыток ушло: {}'.format(trys), colour=discord.Color.green())
            await ctx.send(embed=emb3)
        else:
            emb4 = discord.Embed(title='Ты проиграл. Я загадал число {}'.format(answer), colour=discord.Color.red())
            await ctx.send(embed=emb4)
    except Exception:
        emb5 = discord.Embed(title='Ошибка! Перезапустите игру.', colour=discord.Color.dark_grey())
        await ctx.send(embed=emb5)

# команда для броска кубика
@client.command(pass_context=True)
@commands.cooldown(1, 3)
async def dice(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split(','))
    except Exception:
        emb = discord.Embed(title='Команда должа записана в формате Число,Число!', colour=discord.Color.red())
        await ctx.send(embed=emb)
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    emb1 = discord.Embed(title=result, colour=discord.Color.green())
    await ctx.send(embed=emb1)

# матеша на скорость
@client.command(pass_context=True)
@commands.max_concurrency(1, wait=True)
@commands.guild_only()
async def math(ctx):
    RightAnsw = 0
    run = True

    #Сама игра
    try:
        while run:
            a = random.randint(1, 30)
            b = random.randint(1, 30)
            sign = random.randint(1, 2)
            if sign == 1:
                c = a + b
                emb = discord.Embed(title=str(a) + ' + ' + str(b) + ' ? :', colour=discord.Color.gold())
                await ctx.send(embed=emb)
                HumAnsw = await client.wait_for('message', timeout=5.0)
                if int(HumAnsw.content) == c:
                    RightAnsw += 1
                else:
                    if RightAnsw == 0:
                        emb3 = discord.Embed(
                            title=f'Правильный ответ был {c}. Ты ничего не решил >:( Такой позор даже в рейтинг не внести.',
                            colour=discord.Color.dark_red())
                        await ctx.send(embed=emb3)
                        break

                    emb3 = discord.Embed(
                        title=f'Ты проиграл! Правильный ответ был {c}. Ты смог решить {RightAnsw} примеров!',
                        colour=discord.Color.dark_red())
                    await ctx.send(embed=emb3)
                    run = False
            else:
                c = a - b
                emb1 = discord.Embed(title=str(a) + ' - ' + str(b) + ' ? :', colour=discord.Color.gold())
                await ctx.send(embed=emb1)
                HumAnsw = await client.wait_for('message', timeout=5.0)
                if int(HumAnsw.content) == c:
                    RightAnsw += 1
                else:
                    if RightAnsw == 0:
                        emb3 = discord.Embed(
                            title=f'Правильный ответ был {c}. Ты ничего не решил >:( Такой позор даже в рейтинг не внести.',
                            colour=discord.Color.dark_red())
                        await ctx.send(embed=emb3)
                        break

                    emb3 = discord.Embed(
                        title=f'Ты проиграл! Правильный ответ был {c}. Ты смог решить {RightAnsw} примеров!',
                        colour=discord.Color.dark_red())
                    await ctx.send(embed=emb3)
                    run = False

    #Ошибки
    except asyncio.TimeoutError:
        emb4 = discord.Embed(title=f'Время вышло! Правильный ответ был {c}. Ты смог решить {RightAnsw} примеров!',
                             colour=discord.Color.red())
        await ctx.send(embed=emb4)
    except ValueError:
        emb5 = discord.Embed(
            title=f'Даже не близко... Правильный ответ был {c}. Ты смог решить {RightAnsw} примеров!',
            colour=discord.Color.red())
        await ctx.send(embed=emb5)

    #Вносим результаты в список
    if RightAnsw != 0:
        list = data_stats['users_played']['users']

        for i in range(len(list)):
            if ctx.author.id != list[i]['id']: #Есть ли игрок в базе?
                continue
            if RightAnsw > list[i]['record']: #был ли побит рекорд?
                 data_stats['users_played']['users'][i]['record'] = RightAnsw
            else:
                break

            # получаем список рекордов
            range_list = []
            for j in list:
                 range_list.append(j['record'])
            else:
                range_list.append(RightAnsw)  # в конце добавляем наш правильный ответ

                # распределяем данные
                range_list.sort(reverse=True)
                place = range_list.index(RightAnsw) + 1
                user_info = {'id': ctx.author.id, 'place': place, 'record': RightAnsw}
                l = len(list)

                # Вносим данные в json файл
                data_stats['users_played']['count'] = l
                data_stats['users_played']['users'][i] = user_info

                # получем список мест из рейтинга
                place_list = []
                for h in list:
                    place_list.append(h['place'])
                l1 = len(place_list)

                # проверка на одинаковые места в рейтинге
                for i in range(l1 - 1):
                     for j in range(i + 1, l1):
                        if place_list[i] == place_list[j]:

                            for x in data_stats['users_played']['users']:
                                if x['place'] > place or x['id'] == ctx.author.id:
                                    continue
                                else:
                                    x['place'] += 1
                            else:
                                break
            break

        #если игрока нет в базе
        else:
            #получаем список рекордов
            range_list = []
            for j in list:
                range_list.append(j['record'])
            else:
                range_list.append(RightAnsw) #в конце добавляем наш правильный ответ

            #распределяем данные
            range_list.sort(reverse=True)
            place = range_list.index(RightAnsw) + 1
            user_info = {'id': ctx.author.id, 'place': place, 'record': RightAnsw}
            l = len(list)

            #Вносим данные в json файл
            data_stats['users_played']['count'] = l
            data_stats['users_played']['users'].append(user_info)

            #получем список мест из рейтинга
            place_list = []
            for h in list:
                place_list.append(h['place'])
            l1 = len(place_list)

            #проверка на одинаковые места в рейтинге
            for i in range(l1 - 1):
                for j in range(i + 1, l1):
                    if place_list[i] == place_list[j]:
                        for x in data_stats['users_played']['users']:
                            if x['place'] > place or x['id'] == ctx.author.id:
                                continue
                            else:
                                x['place'] += 1
                        else:
                            break

    #Редактируем файл json
    with open('discord_math_records.json', 'w') as file:
        json.dump(data_stats, file, indent=2)

    time.sleep(3)
    if RightAnsw == 0:
        limit = 3
    else:
        limit = (RightAnsw*2) + 4
    await ctx.channel.purge(limit= limit )

#Рекорды матешы на скорость
@client.command(pass_context=True)
async def mathstat(ctx):
    emb = discord.Embed(title='Лучшие математики!', colour=discord.Color.gold())

    list = data_stats['users_played']['users']

    if len(list) == 0:
        return await ctx.send('Ничего нет(')

    for i in range(len(list)):
        for j in list:
            if j['place'] == i + 1:
                memb = client.get_user(j["id"])
                emb.add_field(name=f'{j["place"]} место - {memb}', value=f'{j["record"]} примера(ов)', inline=False)
            else:
                continue

    else:
        await ctx.send(embed=emb)

#что выбрать?
@client.command(pass_context=True)
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))

#Сообщение в лс
@client.command(pass_context=True)
async def DM(ctx, user: discord.User, content: str):

    await user.send(content)
    await ctx.channel.purge(limit=1)

@client.event
async def on_command_error( ctx, error ):
    await ctx.send('Не позорься пожалуйста :nerd:')
    time.sleep(1)
    await ctx.channel.purge(limit=2)


# тут мы с помощью токена запускаем бота
token = open('token.txt', 'r').readline()
client.run(token)

#https://discord.com/api/oauth2/authorize?client_id=808422502652313633&permissions=0&scope=bot%20applications.commands