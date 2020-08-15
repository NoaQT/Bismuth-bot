class helpCommand(object):
    def init(self, commandsdict):
        self.commandsdict = commandsdict
        self.command_list = "```"
        for command in commandsdict:
            self.command_list += command + (20 - len(command)) * " " + commandsdict[command].desc() + "\n"
        self.command_list += "```"

    async def Command(self, message, args):
        if args == None:
            await message.channel.send(self.command_list)

        elif len(args) != 1:
            message.channel.send("Invalid usage")
            return

        else:
            if args[0] in self.commandsdict:
                command = self.commandsdict[args[0]]
                await message.channel.send("```" + command.usage() + "\n\n" + command.desc() + "```")

            else:
                message.channel.send("`Command not found`")

    def desc(self): return "Shows a list of commands and details on them"
    
    def usage(self): return "help command_name"