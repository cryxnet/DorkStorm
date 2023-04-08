from prettytable import PrettyTable

def print_query_table(data):
    """
    Function to print a table for queries
    """
    headers = ["id", "category", "short_description", "author"]
    rows = []
    
    split_row = ['—' * x for x in [3, 8, 10, 5]]
    
    for row in data:
        rows.append([row[h] if len(str(row[h])) <= 50 else '\n'.join([str(row[h])[i:i+50] for i in range(0, len(str(row[h])), 50)]) for h in headers])
        
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
        table.add_row(split_row)
            
    print(table)
        
def print_url_table(data):
    """
    Function to print a table for google search result
    """
    headers = ["title", "url"]
    rows = []
    split_row = ['—' * x for x in [3, 50]]
    for row in data:
        rows.append([row["title"], row["url"]])

    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
        table.add_row(split_row)

    print(table)

    
def print_configs_table(configs):
    """
    Function to print a table for configs
    """
    headers = ["config_name", "config_value"]
    rows = []

    split_row = ['—' * x for x in [25, 50]]

    for key, value in configs.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                rows.append([sub_key, sub_value])
        else:
            rows.append([key, value])

    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
        table.add_row(split_row)

    print(table)
