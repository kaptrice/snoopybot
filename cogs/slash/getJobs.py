import aiohttp
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

host = "data.usajobs.gov"
authKey  = "api-key-goes-here"
userAgent  = "your-email"
headers = {"Host":host, "User-Agent":userAgent, "Authorization-Key":authKey}
global n

def makeEmbed(data, n, jobCount):
    hiring_lookup = {"fed-internal-search":"Current employees of the agency", "public":"Public", "student":"Student", "ses":"Senior Executives", "fed-competitive":"Competitive service employees", "fed-transition":"Career transition", "oversas":"Oversaes", "disability":"Schedule A", "vet":"Veterans", "peace":"Former Peace Corps","land":"Land management officials", "mspouse":"Military spouses", "special-authorities":"Special authorities"}
    embed = disnake.Embed(
        title="Job lookup",
        description=f"Opening " + str(n + 1) + " of " + jobCount,
        color=0x02bfe7,
    )
    embed.add_field(name="Position Name",
                    value=(data["SearchResultItems"][n]["MatchedObjectDescriptor"]["PositionTitle"]))
    embed.add_field(name="Centre", value=(data["SearchResultItems"][n]["MatchedObjectDescriptor"]["OrganizationName"]))

    embed.add_field(name="Posting End Date",
                        value=(data["SearchResultItems"][n]["MatchedObjectDescriptor"]["PositionEndDate"])[0:10])

    if data["SearchResultItems"][n]["MatchedObjectDescriptor"]["PositionOfferingType"][0]["Name"] != "":
        embed.add_field(name="Term",
                    value=(data["SearchResultItems"][n]["MatchedObjectDescriptor"]["PositionOfferingType"][0]["Name"]))
    else:
        embed.add_field(name="Type", value="Not Provided")

    if (data["SearchResultItems"][n]["MatchedObjectDescriptor"]["UserArea"]["Details"]["LowGrade"] == "00"):
        embed.add_field(name="Grade", value=("Not Provided"))
    elif (data["SearchResultItems"][n]["MatchedObjectDescriptor"]["UserArea"]["Details"]["LowGrade"] == data["SearchResultItems"][n]["MatchedObjectDescriptor"]["UserArea"]["Details"]["HighGrade"]):
        embed.add_field(name="Grade", value=("GS " + data["SearchResultItems"][n]["MatchedObjectDescriptor"]["UserArea"]["Details"]["LowGrade"]))
    else:
        embed.add_field(name="Grade",
                    value=(("GS " + data["SearchResultItems"][n]["MatchedObjectDescriptor"]["UserArea"]["Details"]["LowGrade"]) + " to " + data["SearchResultItems"][n]["MatchedObjectDescriptor"]["UserArea"]["Details"]["HighGrade"]))

    embed.add_field(name="Hiring path",
                    value=(hiring_lookup[(data["SearchResultItems"][n]["MatchedObjectDescriptor"]["UserArea"]["Details"]["HiringPath"][0])]))
    embed.add_field(name="URL",
                    value=(data["SearchResultItems"][n]["MatchedObjectDescriptor"]["PositionURI"]))

    return embed

class Dropdown(disnake.ui.Select):
    def __init__(self, data, counter):
        numbers = range(0, int(jobCount)-1)
        jobTitles = [data["SearchResultItems"][int(i)]["MatchedObjectDescriptor"]["PositionTitle"] for i in numbers]
        jobsList = [(str(numbers[i]+1) + ". " + jobTitles[i]) for i in numbers]
        if len(jobsList) < 25:
            options = [disnake.SelectOption(label=i) for i in jobsList]
        else:
            options = [disnake.SelectOption(label=(jobsList[i])) for i in range(25)]
        self.options = options
        self.jobsList = jobsList
        self.counter = counter
        super().__init__(
            placeholder="Choose a job... (1 to "+ str(len(options)) + ")",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):

        await msg.edit(embed=makeEmbed(data, self.jobsList.index(self.values[0]), jobCount))
        global n
        n = self.jobsList.index(self.values[0])
        try:
            await interaction.send()
        except disnake.errors.HTTPException:
            pass

class Dropdown2(disnake.ui.Select):
    def __init__(self, data):
        numbers = range(0, int(jobCount))
        jobTitles = [data["SearchResultItems"][int(i)]["MatchedObjectDescriptor"]["PositionTitle"] for i in numbers]
        jobsList = [(str(numbers[i]+1) + ". " + jobTitles[i]) for i in numbers]
        if int(jobCount) < 50:
            options = [disnake.SelectOption(label=(jobsList[i])) for i in range(25, int(jobCount))]
        else:
            options = [disnake.SelectOption(label=(jobsList[i])) for i in range(25, 50)]
        self.options = options
        self.jobsList = jobsList
        super().__init__(
            placeholder="Choose a job... (26 to "+ str(len(options)+25) + ")",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):

        await msg.edit(embed=makeEmbed(data, self.jobsList.index(self.values[0]), jobCount))
        global n
        n = self.jobsList.index(self.values[0])

        try:
            await interaction.send()
        except disnake.errors.HTTPException:
            pass

class Dropdown3(disnake.ui.Select):
    def __init__(self, data):
        numbers = range(0, int(jobCount))
        jobTitles = [data["SearchResultItems"][int(i)]["MatchedObjectDescriptor"]["PositionTitle"] for i in numbers]
        jobsList = [(str(numbers[i]+1) + ". " + jobTitles[i]) for i in numbers]
        if int(jobCount) < 75:
            options = [disnake.SelectOption(label=(jobsList[i])) for i in range(50, int(jobCount))]
        else:
            options = [disnake.SelectOption(label=(jobsList[i])) for i in range(50, 75)]
        self.options = options
        self.jobsList = jobsList
        super().__init__(
            placeholder="Choose a job... (51 to "+ str(len(options)+50) + ")",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):

        await msg.edit(embed=makeEmbed(data, self.jobsList.index(self.values[0]), jobCount))
        global n
        n = self.jobsList.index(self.values[0])

        try:
            await interaction.send()
        except disnake.errors.HTTPException:
            pass

class Dropdown4(disnake.ui.Select):
    def __init__(self, data):
        numbers = range(0, int(jobCount))
        jobTitles = [data["SearchResultItems"][int(i)]["MatchedObjectDescriptor"]["PositionTitle"] for i in numbers]
        jobsList = [(str(numbers[i]+1) + ". " + jobTitles[i]) for i in numbers]
        if int(jobCount) < 100:
            options = [disnake.SelectOption(label=(jobsList[i])) for i in range(75, int(jobCount))]
        else:
            options = [disnake.SelectOption(label=(jobsList[i])) for i in range(75, 100)]
        self.options = options
        self.jobsList = jobsList
        super().__init__(
            placeholder="Choose a job... (76 to "+ str(len(options)+75) + ")",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        await msg.edit(embed=makeEmbed(data, self.jobsList.index(self.values[0]), jobCount))
        global n
        n = self.jobsList.index(self.values[0])

        try:
            await interaction.send()
        except disnake.errors.HTTPException:
            pass


class navButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        global data
        self.data = data
        global n
        self.n = n
        self.add_item(Dropdown(data, 1))
        if int(jobCount) > 25:
           self.add_item(Dropdown2(data))
        if int(jobCount) > 50:
           self.add_item(Dropdown3(data))
        if int(jobCount) > 75:
           self.add_item(Dropdown4(data))

    @disnake.ui.button(label="Back", style=disnake.ButtonStyle.blurple)
    async def first_button(
            self, button: disnake.ui.Button, interaction: disnake.MessageInteraction,
    ):
        global n
        if n >= 1:
            n -= 1

        await msg.edit(embed=makeEmbed(data, n, jobCount))
        try:
            await interaction.send()
        except disnake.errors.HTTPException:
            pass


    @disnake.ui.button(label="Forward", style=disnake.ButtonStyle.blurple)
    async def second_button(
            self, button: disnake.ui.Button, interaction: disnake.MessageInteraction,
    ):
        global n
        if n <= int(jobCount):
            n += 1
        await msg.edit(embed=makeEmbed(data, n, jobCount))
        try:
            await interaction.send()
        except disnake.errors.HTTPException:
            pass


class jobGetter(commands.Cog, name="getJobs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="nasajobs",
        description="Fetch a NASA job opening",
    )
    async def nasajobs(self, interaction: ApplicationCommandInteraction):
        """
        Find NASA jobs.
        :param interaction: The application command interaction.
        """
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://data.usajobs.gov/api/search?Organization=NN&ResultsPerPage=99") as request:
                global data
                data = (await request.json())["SearchResult"]
                global jobCount
                jobCount = str(data["SearchResultCountAll"])
                global n
                n = 0
                global selChoices
                selChoices = range(1, data["SearchResultCountAll"])

        first_embed = makeEmbed(data, n, jobCount)
        global msg
        await interaction.send(embed=first_embed, view=navButtons())
        msg = await interaction.original_message()


def setup(bot):
    bot.add_cog(jobGetter(bot))