import exceptions
import disnake
from disnake.ext import commands

class remove_notifs(commands.Cog, name="notification_remove"):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="remove-channel-notification", description="Remove notifications from a channel")
    @commands.default_member_permissions(manage_guild=True, moderate_members=True)
    async def command(self, inter: disnake.ApplicationCommandInteraction, channel_id):
        with open("cogs/slash/channels.txt", "r") as f:
            lines = f.readlines()
            if not str(channel_id) in lines:
                raise exceptions.ChannelNotInList
        with open("cogs/slash/channels.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != str(channel_id):
                    f.write(line)
        await inter.response.send_message("Removed channel " + channel_id + " from notification roll")

def setup(bot):
    bot.add_cog(remove_notifs(bot))