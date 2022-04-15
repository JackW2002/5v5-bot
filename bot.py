#League 5v5 bot
#by Jack Westmoreland
from os import environ
import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='-', intents=intents)

@client.event
async def on_ready():
    print('ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


@client.command(aliases=['c'])
async def clear(ctx, amount=10):
    roles = []
    for role in ctx.message.author.roles:
        roles.append(role.id)

    if 709342907164917831 not in roles:
        await ctx.send('You must have the mod role for this command!')
        return
    await ctx.channel.purge(limit=amount+1)


@client.command(aliases=['5v5'])
async def _5v5(ctx, time: str = None):

    roles = []
    for role in ctx.message.author.roles:
        roles.append(role.id)

    if 919613294719930369 not in roles:
        await ctx.send('You must have the league role for this command!')
        return
    global signup_yes
    global signup_maybe

    if time is None:
        await ctx.send("You must specify a time!")
        return

    signup_yes = []
    signup_maybe = []

    yes_button = Button(label="Yes", style=discord.ButtonStyle.green,
                        emoji="👍")
    maybe_button = Button(label="Maybe", style=discord.ButtonStyle.gray,
                                emoji="🤞")
    no_button = Button(label="No", style=discord.ButtonStyle.red, emoji="👎")

    def create_message():
        if len(signup_maybe) > 0:
            message = f'<@&919613294719930369> 5v5s at {time}! ({len(signup_yes)}-{len(signup_yes)+len(signup_maybe)}/10)\n'
        else:
            message = f'<@&919613294719930369> 5v5s at {time}! ({len(signup_yes)}/10)\n'
        for yes in signup_yes:
            message += f'{yes.name}\n'
        message += '\nMaybe:\n'
        for maybe in signup_maybe:
            message += f'{maybe.name}\n'
        return message

    async def yes_callback(interaction):
        print(interaction.id)
        if interaction.user in signup_yes:
            await interaction.response.send_message('Your already signed up!',
                                                    ephemeral=True)
            return

        if interaction.user in signup_maybe:
            signup_maybe.remove(interaction.user)

        signup_yes.append(interaction.user)
        await interaction.response.edit_message(content=create_message())

    async def maybe_callback(interaction):
        print(interaction.id)
        if interaction.user in signup_maybe:
            await interaction.response.send_message('Your already signed up!',
                                                    ephemeral=True)
            return

        if interaction.user in signup_yes:
            signup_yes.remove(interaction.user)

        signup_maybe.append(interaction.user)
        await interaction.response.edit_message(content=create_message())

    async def no_callback(interaction):
        if interaction.user in signup_yes:
            signup_yes.remove(interaction.user)
        if interaction.user in signup_maybe:
            signup_maybe.remove(interaction.user)

        await interaction.response.edit_message(content=create_message())

    yes_button.callback = yes_callback
    maybe_button.callback = maybe_callback
    no_button.callback = no_callback

    view = View(timeout=10800)
    view.add_item(yes_button)
    view.add_item(maybe_button)
    view.add_item(no_button)

    await ctx.send(content=create_message(), view=view)

@client.command(aliases=['l'])
async def list(ctx):
    await ctx.send('''```
-ping                Responds with bot latency
-clear amount -c Clears amount of messages (mod only)
-5v5 time            starts a 5v5 (league only)
-list -l             lists all commands```''')

#Set your own token
client.run(environ.get('BOTTOKEN'))
