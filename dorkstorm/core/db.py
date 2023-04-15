import requests
import os
import json
import sqlite3
import xml.etree.ElementTree as ET
import datetime

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def execute(self, *args):
        """
        Function to execute sql query
        """
        self.cur.execute(*args)

    def commit(self):
        """
        SQL Commit
        """
        self.conn.commit()

    def fetchall(self):
        """
        Fetch all last executed query results
        """
        return self.cur.fetchall()
    
    def fetchone(self):
        """
        Fetch last executed query result
        """
        return self.cur.fetchone()

    def close(self):
        """
        Function to close sql database connection
        """
        self.conn.close()

    def create_table(self):
        """
        Create query table
        """
        self.execute('''CREATE TABLE IF NOT EXISTS queries 
                 (id INTEGER PRIMARY KEY, 
                 link TEXT, 
                 category TEXT, 
                 short_description TEXT, 
                 textual_description TEXT, 
                 query TEXT, 
                 query_string TEXT, 
                 edb TEXT, 
                 date TEXT, 
                 author TEXT)''')
    
    def query_by_attribute(self, attribute, value):
        """
        Search database by query attribute
        """
        if attribute in ["id", "link", "category", "short_description", "textual_description", "query", "query_string", "edb", "date", "author"]:
            query = f"SELECT * FROM queries WHERE {attribute} LIKE ?"
            self.execute(query, ('%' + value + '%',))
            return self.fetchall()
        else:
            return "Attribute invalid"
        
    def query_by_id(self, id):
        """
        Search database by query id
        """
        query = f"SELECT * FROM queries WHERE id = ?"
        self.execute(query, (id,))
        row = self.cur.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_max_id(self):
        self.execute('SELECT MAX(id) FROM queries')
        result = self.fetchone()
        max_id = result[0] if result[0] is not None else 0

        return max_id

    def insert_query(self, query):
        """
        Add a new query to the database
        """
        values = (query.get('id', self.get_max_id() + 1), query.get('link', None),
                  query['category'], query['short_description'], query['textual_description'],
                  query['query'], query.get('query_string', None), query.get('edb', None),
                  query.get('date', datetime.datetime.now().strftime('%Y-%m-%d')), query['author'])
        
        print("Inserting query with values:", values)
        self.execute('''INSERT INTO queries 
                 (id, link, category, short_description, textual_description, query, query_string, edb, date, author) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  values)

        
    def has_data(self):
        """
        Checks if the database has any data
        """
        self.execute('SELECT count(*) FROM queries')
        count = self.cur.fetchone()[0]
        return count > 0
    
    def query_exists(self, query_id):
        """
        Check if a query with the given ID exists in the database
        """
        self.execute('SELECT COUNT(*) FROM queries WHERE id = ?', (query_id,))
        count = self.cur.fetchone()[0]
        return count > 0
    
    def get_query_count(self):
        """
        Gets the number of queries in the database
        """
        self.execute("SELECT count(*) FROM queries")
        count = self.cur.fetchone()[0]
        return count

    def load_queries(self):
        """
        Load all queries
        """
        # Download the XML file from the URL
        url = 'https://gitlab.com/exploit-database/exploitdb/-/raw/main/ghdb.xml?inline=false'
        response = requests.get(url)
    
        # Save the file to a temporary directory
        if not os.path.exists('temp'):
            os.makedirs('temp')
        with open('temp/ghdb.xml', 'wb') as f:
            f.write(response.content)
    
        # Parse the XML file and load the queries into a list of dicts
        tree = ET.parse('temp/ghdb.xml')
        root = tree.getroot()
    
        queries = []
        for entry in root.findall('entry'):
            query = {}
            query['id'] = int(entry.find('id').text)
            query['link'] = entry.find('link').text
            query['category'] = entry.find('category').text
            query['short_description'] = entry.find('shortDescription').text
            query['textual_description'] = entry.find('textualDescription').text
            query['query'] = entry.find('query').text
            query['query_string'] = entry.find('querystring').text
            query['edb'] = entry.find('edb').text
            query['date'] = entry.find('date').text
            query['author'] = entry.find('author').text
            queries.append(query)
    
        # Save the queries to a SQLite database
        for query in queries:
            self.insert_query(query)
            
        self.commit()
    
        print(f'Successfully loaded {len(queries)} queries into the database and saved to queries.json.')
        
    def update_queries(self):
        """
        Update the database with all queries from the Exploit Database
        """
        # Download the XML file from the URL
        url = 'https://gitlab.com/exploit-database/exploitdb/-/raw/main/ghdb.xml?inline=false'
        response = requests.get(url)

        # Parse the XML file and load the queries into a list of dicts
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        queries = []
        for entry in root.findall('entry'):
            query = {}
            query['id'] = entry.find('id').text
            query['link'] = entry.find('link').text
            query['category'] = entry.find('category').text
            query['short_description'] = entry.find('shortDescription').text
            query['textual_description'] = entry.find('textualDescription').text
            query['query'] = entry.find('query').text
            query['query_string'] = entry.find('querystring').text
            query['edb'] = entry.find('edb').text
            query['date'] = entry.find('date').text
            query['author'] = entry.find('author').text
            queries.append(query)

        # Check which queries are new
        new_queries = []
        for query in queries:
            if not self.query_exists(query['id']):
                new_queries.append(query)

        # Add the new queries to the database
        for query in new_queries:
            self.insert_query(query)

        self.commit()

        print(f'Successfully loaded queries and added {len(new_queries)} new queries.')

        
    def search_query(self, attribute, value):
        """
        Main search query
        """
        if attribute in ["id", "link", "category", "short_description", "textual_description", "query", "query_string", "edb", "date", "author"]:
            results = self.query_by_attribute(attribute, value)
            temp_results = []
            for result in results:
                temp_results.append(dict(result)) 
            return temp_results
