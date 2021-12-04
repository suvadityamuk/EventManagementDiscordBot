# Event Management Discord Bot

A *Discord bot* written in Python that can be used to control event management on a Discord server.  

Commands List:
----
- ### Create a new Role
`$createGeneralRole <role_name>`

Can be used to create a new role. As of now, the permission level of this role is static and cannot be changed without making changes to the script

- ### Delete an existing Role
`$deleteGeneralRole <role_name>`  

Can be used to delete a previously-existing role.

- ### Create a new Category
`$createGeneralRole <role_name>`

Can be used to create a new category. 

- ### Delete an existing Category
`$deleteGeneralRole <role_name>`

Can be used to delete a previously-existing category.

- ### Create a new Text Channel
`$createTC <text_channel_name> category=<optional_arg> role_to_sync_with=<optional_arg>`

Can be used to create a new Text Channel.
  
- ### Delete an existing Text Channel
`$deleteTC <text_channel_name>`

Can be used to delete a previously-existing Text Channel.

- ### Create a new Voice Channel
`$createVC <text_channel_name> category=<optional_arg> role_to_sync_with=<optional_arg>`

Can be used to create a new Voice Channel.
  
- ### Delete an existing Voice Channel
`$deleteVC <text_channel_name>`

Can be used to delete a previously-existing Voice Channel.

- ### Create a new Team
`$createAllTeamReqs <name1> <name2> <team_name>`

Can be used to create a new team, which includes a private Role and a private category synced with the role, containing 1 Text and 1 Voice Channel
  
- ### Delete an existing Team
`$deleteVC <text_channel_name>`

Can be used to delete a previously-existing Team.
  
- ### Kick/Remove a user
`$removeUser <username>`
  
Can be used to kick/remove a user from the server.
  
- ### Ban a user
`$banUser <username>`
  
Can be used to ban a user from the server.

- ### Add an existing role to a user
`$addRole <username> <role_to_add>`
  
Adds pre-defined role on requested user.
  
- ### Remove an existing role present with a user
`$removeRole <username> <role_to_remove>`
  
Removes specified role of requested user.
  
- ### Server Mute a user
`$serverMuteActive <username>`
  
Activates Server Mute on requested user. Has no effect if user is already server-muted.
  
- ### Server Deafen a user
`$serverDeafenActive <username>`
  
Activates Server Deafen on requested user. Has no effect if user is already server-deafened.
  
- ### Remove Server Mute from a user
`$serverMuteDeactive <username>`
  
Deactivates Server Mute on requested user. Has no effect if user is not server-muted already.
  
- ### Remove Server Deafen from a user
`$serverDeafenDeactive <username>`
  
Deactivates Server Deafen on requested user. Has no effect if user is not server-deafened already.

- ### Get commands help
`$help_wanted`

Generates this documentation within your Discord server Text channel

Feel free to make PRs or issues on this to improve the code quality.
