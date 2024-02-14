import gdb
import re

def stop_handler(event):
    mappings = gdb.execute("info proc mappings", to_string=True)
    S = mappings.split('objfile\n')[1].split('\n')[0]
    match = re.search(r'(0x[0-9a-fA-F]+)', S)
    BA = match.group(1)
    print("Base Address: ", BA)
    gdb.parse_and_eval(f"$B = {BA}")
    gdb.events.stop.disconnect(stop_handler)

gdb.events.stop.connect(stop_handler)

class FastBreakPoint(gdb.Command):
    def __init__(self):
        super().__init__("bb", gdb.COMMAND_USER)

    def invoke(self, argument, from_tty):
        if not argument:
            print("Argument Please!")
            return

        if 'x' not in argument:
            argument = "0x" + argument

        command = f"b *$B+{argument}"
        gdb.execute(command)

FastBreakPoint()
