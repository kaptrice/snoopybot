from disnake.ext import tasks, commands
import aiohttp


class looper(commands.Cog, name="looper"):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.bot = bot
        self.host = "data.usajobs.gov"
        self.authKey = "your-api-key"
        self.userAgent = "your-api-key-linked-email"
        self.headers = {"Host": self.host, "User-Agent": self.userAgent, "Authorization-Key": self.authKey}
        self.diff = []
        self.oldData = []


    async def originalData(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            #NN is the organisation code for NASA
            async with session.get("https://data.usajobs.gov/api/search?Organization=NN&ResultsPerPage=99") as request:
                self.oldData = ((await request.json())["SearchResult"]);

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(minutes=60.0)
    async def printer(self):
        if self.index == 0:
            await self.originalData()
        print(self.index)
        self.index += 1
        with open("cogs/slash/channels.txt", 'r') as filehandle:
            channel_ids = [current_place.rstrip() for current_place in filehandle.readlines()]
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get("https://data.usajobs.gov/api/search?Organization=NN&ResultsPerPage=99") as request:
                newData = (await request.json())["SearchResult"]
        positionNames = []
        for i in newData["SearchResultItems"]:
            positionNames.append(i["MatchedObjectDescriptor"]["PositionTitle"])
        oldNames = []
        for i in self.oldData["SearchResultItems"]:
            oldNames.append(i["MatchedObjectDescriptor"]["PositionTitle"])

        indices = []
        for i in positionNames:
            if i not in oldNames:
                indices.append(positionNames.index(i))

        if not(len(indices) == 0):
            try:
                for i in channel_ids:
                    for j in indices:
                        try:
                            await self.bot.get_channel(int(i)).send("A new NASA job has been posted: " + positionNames[j] + " at " + newData["SearchResultItems"][j]["MatchedObjectDescriptor"]["OrganizationName"]+".")
                            break
                        except:
                            await self.bot.get_channel(int(i)).send("Oops! I had an error processing a job posting. Please contact the bot owner.")

            except:
                print("invalid channel haha")
        self.oldData = newData

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(a := looper(bot))
    a.printer.start()
