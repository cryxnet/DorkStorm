from config.header import header
from colorama import Fore, init, Back
from core.db import Database
from core.command import CommandHandler
from core.context import Context
from core.dork import DorkEngine
from core.pentest import PentestEngine

# === Settings === #
init(autoreset=True) # colorama autoreset text color

# === Database === #
db = Database('queries.db')
db.create_table()

# === Dork Service === #
dork_engine = DorkEngine()

# === Penetration Testing Module === #
penetration_test_engine = PentestEngine()

# === Context === #
context = Context(database=db, dork_engine=dork_engine, penetration_test_engine=penetration_test_engine)

# === Command Handling === #
cmdHandler = CommandHandler(context=context)

# === Data Preperation === #
if not db.has_data():
    db.load_queries()

if __name__ == '__main__':
    print(Fore.RED + header)
    # Loop to keep asking for commands until the user exits
    while True:
        # Get the command from the user
        command = input(Fore.RED + f"@-~dorkstorm ~({context.query['configs']['base_query_id'] if context.query['configs']['base_query_id'] else '$'}) ")
        # Handle the command
        cmdHandler.handle_command(command)
