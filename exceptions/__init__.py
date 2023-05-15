from disnake.ext import commands

class ChannelNotInList(commands.CheckFailure):
    """
    Thrown when a channel is specified for deletion, but does not exist in the registry
    """

    def __init__(self, message="Channel is not configured for notifications!"):
        self.message = message
        super().__init__(self.message)


class ChannelAlreadyInList(commands.CheckFailure):

    def __init__(self, message="Channel is already configured for notifications!"):
        self.message = message
        super().__init__(self.message)