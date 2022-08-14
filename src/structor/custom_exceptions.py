class CommandDoesNotExist(Exception):
    """Empty directory exception"""
    def __init__(self, command: str):
        super(CommandDoesNotExist, self).__init__(f"The command {command} does not exist")