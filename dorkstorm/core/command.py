from core.utils import print_query_table, print_url_table, print_configs_table
import os, datetime

class CommandHandler():
    def __init__(self, context):
        self.context = context
            
    # Define the command handling function
    def handle_command(self, command):
        if command == "help":
            print("""
                DorkStorm - A tool for Google dorks

                Commands:
                    help          Show this help message | help
                    search        Search the Google dorks database | search <attribute> <value>
                    set           Sets an extra query parameter | set <key> <value>
                    unset         Unsets an extra query parameter | unset <key>
                    get           Gets an extra query parameter | get <key> (or configs to get all)
                    use           Sets an base google dorks attack | use <dork_query_id>
                    update query  Updates the query database | update query
                    build query   Builds the query and outputs it | build query
                    execute       Executes the query | execute <flag> (--headless (--limit pages), --browser)
                    pentest site  Execute all queries to a website | pentest site <domain>
                    
                    quit / exit   Exit the program
                """)
            
        elif command.startswith("search "):
            tokens = command.split()
            if len(tokens) != 3:
                print("Invalid command. See 'help' for usage.")
            else:
                attribute = tokens[1]
                value = tokens[2]
                print(attribute, value)
                result = self.context.database.search_query(attribute, value)
                print_query_table(result)
     
        elif command.startswith("set "):
            cmdValues = command.split(" ")
            key = cmdValues[1]
            value = command.replace(f"set {key} ", "")

            if key in self.context.query["configs"]["extra_query_params"]:
                self.context.query["configs"]["extra_query_params"][key] = value
                print(f"{key} set to {value}")
            else:
                print(f"[ERROR] Not a valid query parameter: {key}")

                
        elif command.startswith("unset "):
            cmdValues = command.split(" ")
            key = cmdValues[1]
            
            if key in self.context.query["configs"]["extra_query_params"]:
                self.context.query["configs"]["extra_query_params"][key] = None
                print(f"{key} is cleared")
            else:
                print(f"{key} does not exists")
                
        elif command.startswith("get "):
            cmdValues = command.split(" ")
            key = cmdValues[1]
            
            if key == "configs":
                print_configs_table(self.context.query["configs"])
            else:
                if key in self.context.query["configs"]["extra_query_params"]:
                     value = self.context.query["configs"]["extra_query_params"][key]
                     print(f"{key} is set to {value}")
                else:
                     print("f{key} is not a valid query parameter}")
                
        elif command.startswith("use "):
            cmdValues = command.split(" ")
            
            query_id = int(cmdValues[1])
            
            try:
                query = self.context.database.query_by_id(query_id)

                self.context.query["configs"]["base_query_params"] = query["query"]
                self.context.query["configs"]["base_query_id"] = query_id

                print(f"Using {query['short_description']} as base query parameter")
            except:
                print(f"[ERROR] A query with the id {query_id} does not exist")
                
        elif command == "build query":
            result = self.context.dork_engine.build_query(self.context.query)
            print(f"The query is builded: %s" % result)
            
        elif command.startswith("execute"):
            flag = command.split(" ")[1]
    
            if self.context.query["configs"]["base_query_params"]:
                builded_query = self.context.dork_engine.build_query(self.context.query)

                if flag == "--headless":
                    page_limit = 1
                    
                    if "--limit" in command:
                        try:
                            page_limit = int(command.split(" ")[3])
                        except:
                            print("[ERROR] Invalid limit parameter")
                            return 0
                    
                    result = self.context.dork_engine.google_search(query=builded_query, limit=page_limit)
                    
                    print_url_table(result)
                    
                elif flag == "--browser":
                    os.system(f"start msedge {builded_query}")
                
                else:
                    print("[ERROR] Please select an valid flag (--headless, --browser)")
       
            else:
                print("[ERROR] Please set a query (use <query_id>)")
                
        elif command == "save query":
            print("[INFO] The query you wan't to save: " + "")
            
            category = input("Enter the category for this query: ")
            description = input("Enter a short description for this query: ")
            textual_description = input("Enter a textual description for this query: ")
            author = input("Enter your name as the author of this query: ")
            
            builded_query = self.context.dork_engine.build_query(self.context.query, param_only=True)
            
            query = {
                'category': category,
                'short_description': description,
                'textual_description': textual_description,
                'query': builded_query,
                'author': author
            }
            
            self.context.database.insert_query(query)
            
            print("[~] Added query to the database")
            
        elif command == "update query":
            self.context.database.update_queries()
            
        elif command.startswith("pentest site"):
            site = command.split(" ")[2]
            
            self.context.penetration_test_engine.test_website(context=self.context, domain=site)
            
        elif command == "exit" or command == "quit":
            print("Goodbye!")
            exit()
            
        else:
            print("[ERROR] Invalid command. Please try again.")
