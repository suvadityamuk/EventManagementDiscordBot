import discord
from discord import user

def getCategory(ctx, cat_name):
    for i in ctx.guild.categories:
        if str(i) == cat_name or i.name == cat_name:
            return i
    else:
        return None
    
def getRole(ctx, role_name:str):
    curr_guild = ctx.guild
    for i in curr_guild.roles:
        if str(i) == role_name or i.mention == role_name or i.name == role_name:
            return i
    else: 
        return None

def getMember(ctx, username:str):
    curr_guild = ctx.guild
    for i in curr_guild.members:
        if i.nick == username or i.mention == username or i.name.lower() == username.lower() or str(i) == username:
            return i
    else:
        return None

def getCatString(arg:str):
    res = arg.split('category=')
    if len(res) != 2:
        return None
    else:
        return res[1]

def getRoleString(arg:str):
    res = arg.split('role_to_sync_with=')
    if len(res) != 2:
        return None
    else:
        return res[1]