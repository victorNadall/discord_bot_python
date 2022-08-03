import json
import discord
from discord.ext import commands


with open('config.json') as e:
    infos = json.load(e)
    TOKEN = infos['token']
    prefixo = infos['prefix']

client = commands.Bot(command_prefix=prefixo, intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"Client Online!\nID: {client.user.id}\nNome: {client.user.name}")


@client.event
async def on_member_join(member):
    guild = member.guild
    canal = discord.utils.get(guild.channels, id='Canal que você quer que o usuário entre pela primeira vez')
    embed = discord.Embed(title="Olá! Bem-vindo(a)!", color=0xff0000,
    description=f'{member.mention}, seja bem-vindo ao servidor {guild.name}! Divirta-se!!!')
    embed.set_author(name=member.name, icon_url=member.avatar_url)

    await canal.send(embed=embed)

    # Adiciona um cargo de Membro para o usuário recém logado
    membro = discord.utils.get(member.guild.roles, id='Crie um cargo de Membro e adicione o id do cargo')
    await member.add_roles(membro)

    # Adiciona um cargo de Não Verificado para o usuário recém logado
    naoverificado = discord.utils.get(member.guild.roles, id='Crie um cargo de Não Verificado e adicione o id do cargo')
    await member.add_roles(naoverificado)


@client.command()
async def ola(ctx):
    await ctx.send(f"Olá {ctx.author.name}, tudo bem com você meu querido?")


@client.command()
async def enviar1(ctx, *, mensagem=None):
    if ctx.author.guild_permissions.administrator:
        if mensagem is None:
            await ctx.send("Não posso enviar uma mensagem em branco!")
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.author.name}:** {mensagem}")


@client.command()
async def enviar2(ctx, *, mensagem=None):
    if ctx.author.guild_permissions.administrator:
        if mensagem is None:
            await ctx.send("Não posso enviar uma mensagem em branco!")
        else:
            await ctx.message.delete()
            await ctx.send(f"**{client.user.name}:** {mensagem}")


@client.command()
async def enviar3(ctx, *, mensagem=None):
    if ctx.author.guild_permissions.administrator:
        if mensagem is None:
            await ctx.send("Não posso enviar uma mensagem em branco!")
        else:
            await ctx.message.delete()
            await ctx.send(f"**{mensagem}**")


@client.command()
async def anunciar(ctx, *, mensagem=None):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title=f'{ctx.author.name}', description=f'{mensagem}', color=discord.Color.blue())
        await ctx.message.delete()
        await ctx.send(embed=embed)


@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(title=f'Usuário expulso: {member.name}', description=f'Motivo da expulsão: {reason}')
    await ctx.send(embed=embed)
    await ctx.message.delete()
    user = discord.Embed(title=f'Você foi expulso!', description=f'Motivo da expulsão: {reason}')
    await member.send(embed=user)
    await member.kick(reason=reason)


@client.command()
async def verificar(ctx, membro: discord.Member, cargo: discord.Role):
    verificado = discord.utils.get(membro.guild.roles, id='Crie um cargo de Verificado e adicione o id do cargo')
    if cargo == verificado:
        await membro.add_roles(cargo)
        await ctx.send(f'{membro.name} foi Verificado :white_check_mark:')
        naoverificado = discord.utils.get(membro.guild.roles, id='Adicione o ID do cargo de não verificado aqui para removê-lo')
        await membro.remove_roles(naoverificado)


@client.command(aliases=['c'])
async def clear(ctx, amount=100):
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)
        await ctx.send('As mensagens foram apagadas com sucesso!', delete_after=20)
    else:
        falta = 'Você não tem permissão para usar esse comando!'
        embed = discord.Embed(title=f'{falta}')
        await ctx.send(embed=embed)


client.run(TOKEN)
