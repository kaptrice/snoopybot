import exceptions
import disnake
from disnake.ext import commands

class addNotifs(commands.Cog, name="notification_add"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="add-channel-notification", description="Add new job notifications to a channel")
    @commands.default_member_permissions(manage_guild=True, moderate_members=True)
    async def command(self, inter: disnake.ApplicationCommandInteraction, channel_id):
        with open("cogs/slash/channels.txt", "r") as f:
            lines = f.readlines()
            if str(channel_id) in lines:
                raise exceptions.ChannelAlreadyInList
            f.write("\n")
            f.write(str(channel_id))
        await inter.response.send_message("Added channel " + channel_id + " to notification roll")


def setup(bot):
    bot.add_cog(addNotifs(bot))