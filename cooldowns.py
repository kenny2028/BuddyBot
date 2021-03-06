import datetime
from discord.ext import commands

on_cooldown = {}  # A dictionary mapping user IDs to cooldown ends


def cooldown(seconds):
    def predicate(context):
        if (cooldown_end := on_cooldown.get(context.author.id)) is None or cooldown_end < datetime.datetime.now():  # If there's no cooldown or it's over
            if context.valid and context.invoked_with in (*context.command.aliases, context.command.name):  # If the command is being run as itself (not by help, which runs checks and would end up creating more cooldowns if this didn't exist)
                on_cooldown[context.author.id] = datetime.datetime.now() + datetime.timedelta(seconds=seconds)  # Add the datetime of the cooldown's end to the dictionary
            return True  # And allow the command to run
        else:
            raise commands.CommandOnCooldown(commands.BucketType.user, (cooldown_end - datetime.datetime.now()).seconds)  # Otherwise, raise the cooldown error to say the command is on cooldown

    return commands.check(predicate)
