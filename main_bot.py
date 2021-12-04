import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord.flags import Intents
import helpers

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)



@bot.command()
async def hello_world(ctx, arg):
    await ctx.send(f'Hello, {ctx.author}. {arg}.')



class ChannelHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coreID = 0
        self.coreDict = dict()
        self.guild = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Here {member.mention}, you are. May the force be with you.')
    
    def populateCoreList(self, member):
        print(type(self))
        curr_guild = member.guild

        for i in curr_guild.roles:
            if str(i) == 'OG':
                self.coreID = i.id
        
        self.coreDict = {str(i) : i.id for i in curr_guild.members if 'OG' in list(map(str, i.roles))}
        ''' 
        Alternate, easier method:  
            for i in curr_guild.members:
                member_roles = list(map(str, i.roles))
                if 'Core' in member_roles:
                    self.coreDict[str(i)] = i.id
                    await curr_guild.system_channel.send(f'Name = {str(i)}\nID = {self.coreID}')
        '''

    def checkIfUserIsCore(ctx):
        curr_cog = ctx.cog
        curr_cog.populateCoreList(ctx.author)
        if str(ctx.author) in curr_cog.coreDict.keys():
            return True
        else:
            return False

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def createGeneralRole(self, ctx, role_name:str):
        '''
        Creates a new Role
        Usage: $createGeneralRole <role_name>
        '''
        try:
            curr_guild = ctx.guild
            role_permissions = discord.Permissions(change_nickname=True, add_reactions=True, connect=True, attach_files=True, embed_links=True, read_message_history=True, read_messages=True, send_messages=True, speak=True, stream=True, use_external_emojis=True, use_voice_activation=True, view_channel=True)
            await curr_guild.create_role(name=role_name, permissions=role_permissions, mentionable=True)
        except:
            await ctx.send('Sorry, this action could not be completed. Error in Role-Creation.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def deleteGeneralRole(self, ctx, role_name:str):
        '''
        Deletes a Role
        Usage: $deleteGeneralRole <role_name>
        '''
        act_role = helpers.getRole(ctx, role_name)
        if act_role == None:
            await ctx.send(f'Could not delete the {role_name} category. CodeWars was unable to find it')
        else:
            try:
                self.guild = ctx.guild
                await act_role.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            except:
                await ctx.send(f'Could not delete the {role_name} role. CodeWars was unable to delete it.')


    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def createCategory(self, ctx, cat_name:str, *kwargs):
        '''
        Create a new Category
        Usage: $createCategory <cat_name>
        '''
        curr_guild = ctx.guild
        self.guild = ctx.guild
        role_to_sync_with = None
        print(kwargs)
        for i in kwargs:
            if helpers.getRoleString(i) != None:
                role_to_sync_with = helpers.getRoleString(i)
        if type(role_to_sync_with) is str:
            role_to_sync_with = helpers.getRole(ctx, role_to_sync_with)
        try:
            if role_to_sync_with is None: 
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                }
                await curr_guild.create_category_channel(cat_name, overwrites=overwrites, reason=f"This category was made by CodeWars, under command of '{ctx.author}'")
            else:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                    role_to_sync_with: discord.PermissionOverwrite(read_messages=True),
                }
                await curr_guild.create_category_channel(cat_name, overwrites=overwrites, reason=f"This category was made by CodeWars, under command of '{ctx.author}'")
        except:
            await ctx.send(f'Could not create the {cat_name} category.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def deleteCategory(self, ctx, cat_name:str):
        '''
        Deletes a Category
        Usage: $deleteCategory <cat_name>
        '''
        act_category = helpers.getCategory(ctx, cat_name)
        if act_category == None:
            await ctx.send(f'Could not delete the {cat_name} category. CodeWars was unable to find it')
        try:
            await act_category.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        except:
            await ctx.send(f'Could not delete the {cat_name} category.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def createTC(self, ctx, text_channel_name:str, *kwargs):
        '''
        Create a Text Channel
        Usage: $createTC <text_channel_name>
        Keyword Args:
            1) category : (str) Specify category to apply membership of Text Channel
            2) role_to_sync_with : (str) Specify Server Role to sync Channel Permissions with
        '''
        category = None
        role_to_sync_with = None
        self.guild = ctx.guild
        print(kwargs)
        for i in kwargs:
            if helpers.getCatString(i) != None:
                category = helpers.getCatString(i)
            if helpers.getRoleString(i) != None:
                role_to_sync_with = helpers.getRoleString(i)

        curr_guild = ctx.guild
        overwrites = dict()
        if type(category) is str:
            category = helpers.getCategory(ctx, category)
        if type(role_to_sync_with) is str:
            role_to_sync_with = helpers.getRole(ctx, role_to_sync_with)
        try:
            if category is None and role_to_sync_with is None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=True),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                }
                tc = await curr_guild.create_text_channel(text_channel_name, bitrate=64000, user_limit=4, overwrites=overwrites, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            elif category is not None and role_to_sync_with is None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=True),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                }
                tc = await curr_guild.create_text_channel(text_channel_name, bitrate=64000, user_limit=4, overwrites=overwrites, category=category, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            elif category is None and role_to_sync_with is not None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                    role_to_sync_with: discord.PermissionOverwrite(read_messages=True),
                }
                tc = await curr_guild.create_text_channel(text_channel_name, bitrate=64000, user_limit=4, overwrites=overwrites, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            elif category is not None and role_to_sync_with is not None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                    role_to_sync_with: discord.PermissionOverwrite(read_messages=True),
                }
                tc = await curr_guild.create_text_channel(text_channel_name, bitrate=64000, user_limit=4, overwrites=overwrites, category=category, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        except:
            await ctx.send(f'Could not create the {text_channel_name} Text Channel.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def deleteTC(self, ctx, text_channel_name:str):
        '''
        Deletes a created Text Channel
        Usage: $deleteTC <text_channel_name>
        '''
        curr_guild = ctx.guild
        self.guild = ctx.guild
        try:
            for i in curr_guild.text_channels:
                if str(i) == text_channel_name:
                    await i.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            else:
                await ctx.send('Could not delete the channel. CodeWars couldn\'t detect it')
        except:
            await ctx.send(f'Could not delete the {text_channel_name} Text Channel.')


    
    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def createVC(self, ctx, vc_name:str, *kwargs):
        '''
        Create a Voice Channel
        Usage: $createVC <text_channel_name>
        Keyword Args:
            1) category : (str) Specify category to apply membership of Text Channel
            2) role_to_sync_with : (str) Specify Server Role to sync Channel Permissions with
        '''
        category = None
        role_to_sync_with = None
        self.guild = ctx.guild
        print(kwargs)
        for i in kwargs:
            if helpers.getCatString(i) != None:
                category = helpers.getCatString(i)
            if helpers.getRoleString(i) != None:
                role_to_sync_with = helpers.getRoleString(i)
        curr_guild = ctx.guild
        overwrites = dict()
        print(type(self.bot))
        if type(category) is str:
            category = helpers.getCategory(ctx, category)
        if type(role_to_sync_with) is str:
            role_to_sync_with = helpers.getRole(ctx, role_to_sync_with)
        try: 
            if category is None and role_to_sync_with is None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=True),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                }
                vc = await curr_guild.create_voice_channel(vc_name, bitrate=64000, user_limit=4, overwrites=overwrites, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            elif category is not None and role_to_sync_with is None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=True),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                }
                vc = await curr_guild.create_voice_channel(vc_name, bitrate=64000, user_limit=4, overwrites=overwrites, category=category, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            elif category is None and role_to_sync_with is not None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                    role_to_sync_with: discord.PermissionOverwrite(read_messages=True),
                }
                vc = await curr_guild.create_voice_channel(vc_name, bitrate=64000, user_limit=4, overwrites=overwrites, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            elif category is not None and role_to_sync_with is not None:
                overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                    role_to_sync_with: discord.PermissionOverwrite(read_messages=True),
                }
                vc = await curr_guild.create_voice_channel(vc_name, bitrate=64000, user_limit=4, overwrites=overwrites, category=category, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        except:
            await ctx.send('Sorry, this action was not completed. Error during creation of Voice channel')


    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def deleteVC(self, ctx, vcToDelete:str):
        '''
        Deletes a created Voice Channel
        Usage: $deleteVC <vcToDelete>
        '''
        curr_guild = ctx.guild
        try:
            for i in curr_guild.voice_channels:
                if str(i) == vcToDelete:
                    await i.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        except:
            await ctx.send('Sorry, this action was not completed. Error during deletion of Voice channel')


    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def createAllTeamReqs(self, ctx, name1:str, name2:str, team_name:str, *kwargs):
        '''
        Creates a Role, Category, Text and Voice Channel made for a specific team
        Usage: $createAllTeamReqs <name1> <name2> <team_name>
        '''
        try:
            curr_guild = ctx.guild
            role_permissions = discord.Permissions(change_nickname=True, add_reactions=True, connect=True, attach_files=True, embed_links=True, read_message_history=True, read_messages=True, send_messages=True, speak=True, stream=True, use_external_emojis=True, use_voice_activation=True, view_channel=True)
            role = await curr_guild.create_role(name=team_name, permissions=role_permissions, mentionable=True)
            overwrites = {
                    curr_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    curr_guild.me: discord.PermissionOverwrite(read_messages=True),
                    role: discord.PermissionOverwrite(read_messages=True),
                }
            cat = await curr_guild.create_category_channel(team_name, overwrites=overwrites, reason=f"This category was made by CodeWars, under command of '{ctx.author}'")
            await curr_guild.create_text_channel(team_name, overwrites=overwrites, category=cat, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            await curr_guild.create_voice_channel(team_name, bitrate=64000, user_limit=4, overwrites=overwrites, category=cat, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        except:
            await ctx.send('Sorry, this action was not completed. Error during creation of Team-specific Assets')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def deleteAllTeamReqs(self, ctx, team_name):
        '''
        Deletes a Role, Category, Text and Voice Channel made for a specific team
        Usage: $deleteAllTeamReqs <team_name>
        '''
        try:
            curr_guild = ctx.guild
            for i in curr_guild.voice_channels:
                if str(i) == team_name:
                    await i.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            for i in curr_guild.text_channels:
                if str(i) == team_name:
                    await i.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            act_category = helpers.getCategory(ctx, team_name)
            await act_category.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
            act_role = helpers.getRole(ctx, team_name)
            await act_role.delete(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        except:
            await ctx.send('Sorry, this action was not completed. Error during deletion of Team-specific Assets')


    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def removeUser(self, ctx, username):
        '''
        Removes requested user from the server.
        Usage: $removeUser <username>
        '''
        curr_member = helpers.getMember(ctx, username)
        if type(curr_member) == discord.member.Member:
            await curr_member.kick(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        else:
            await ctx.send('Sorry, could not kick user. The member was not found.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def banUser(self, ctx, username):
        '''
        Bans requested user.
        Usage: $banUser <username>
        '''
        curr_member = helpers.getMember(ctx, username)
        if type(curr_member) == discord.member.Member:
            await curr_member.ban(reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'")
        else:
            await ctx.send('Sorry, could not ban user. The member was not found.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def addRole(self, ctx, username:str, role_to_add:str):
        '''
        Adds pre-defined role on requested user.
        Usage: $addRole <username> <role_to_add>
        '''
        curr_member = helpers.getMember(ctx, username)
        act_role = helpers.getRole(ctx, role_to_add)
        if type(curr_member) == discord.member.Member and type(act_role) == discord.role.Role:
            await curr_member.add_roles(act_role, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'", atomic=True)
        else:
            await ctx.send('Sorry, could not add the role. Either the role or the member was not found.')


    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def removeRole(self, ctx, username:str, role_to_remove:str):
        '''
        Removes specified role of requested user.
        Usage: $removeRoles <username> <role_to_remove>
        '''
        curr_member = helpers.getMember(ctx, username)
        act_role = helpers.getRole(ctx, role_to_remove)
        if type(curr_member) == discord.member.Member and type(act_role) == discord.role.Role:
            await curr_member.remove_roles(act_role, reason=f"This action was performed by the CodeWars bot, under command of '{ctx.author}'", atomic=True)
        else:
            await ctx.send('Sorry, could not remove the role. Either the role or the member was not found.')


    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def serverDeafenActive(self, ctx, username:str):
        '''
        Activates Server Deafen on requested user.
        Usage: $serverDeafenActive <username>
        '''
        curr_member = helpers.getMember(ctx, username)
        if type(curr_member) == discord.member.Member:
            await curr_member.edit(deafen=True)
        else:
            await ctx.send('Sorry, could not deafen. User was not found.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def serverDeafenDeactive(self, ctx, username:str):
        '''
        Deactivates Server Deafen on requested user.
        Usage: $serverDeafenDeactive <username>
        '''
        curr_member = helpers.getMember(ctx, username)
        if type(curr_member) == discord.member.Member:
            await curr_member.edit(deafen=False)
        else:
            await ctx.send('Sorry, could not undeafen. User was not found.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def serverMuteActive(self, ctx, username:str):
        '''
        Activates Server Mute on requested user.
        Usage: $serverMuteActive <username>
        '''
        curr_member = helpers.getMember(ctx, username)
        print("type=",type(curr_member))
        if type(curr_member) == discord.member.Member:
            await curr_member.edit(mute=True)
        else:
            await ctx.send('Sorry, could not mute. User was not found.')

    @commands.command()
    @commands.check(checkIfUserIsCore)
    async def serverMuteDeactive(self, ctx, username:str):
        '''
        Deactivates Server Mute on requested user.
        Usage: $serverMuteDeactive <username>
        '''
        curr_member = helpers.getMember(ctx, username)
        if type(curr_member) == discord.member.Member:
            await curr_member.edit(mute=False)
        else:
            await ctx.send('Sorry, could not unmute.  User was not found.')
    
    

@bot.command()
async def help_wanted(ctx):
    channel_handler = ChannelHandler(bot)
    comm_list = channel_handler.get_commands()
    await ctx.send('```\nCodeWars Bot : Help\n```')
    for i in comm_list:
        await ctx.send(f'```\nCommand : {i.name}\nDescription :\n{i.help}\n\n```')

bot.add_cog(ChannelHandler(bot))
bot.run('OTE0ODExMDIzODQyNzYyNzc0.YaSeKA.RVUgiPXE5GS0b1Z154dXpxRy__A')