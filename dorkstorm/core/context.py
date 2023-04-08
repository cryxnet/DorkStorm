class Context:
    def __init__(self, database, dork_engine, penetration_test_engine):
        self.database = database
        self.dork_engine = dork_engine
        self.penetration_test_engine = penetration_test_engine
        self.query = {
            "builded_query": None,
            "configs": {
                "base_query_params": None,
                "base_query_id": None,
                "extra_query_params": {
                    "inurl": None,
                    "intitle": None,
                    "site": None,
                    "filetype": None,
                    "link": None,
                    "related": None,
                    "info": None,
                    "cache": None,
                    "define": None,
                    "stocks": None,
                    "weather": None,
                    "movie": None,
                    "map": None,
                    "book": None,
                    "patent": None,
                    "phonebook": None,
                    "rphonebook": None,
                    "bphonebook": None,
                    "city": None,
                    "country": None,
                    "language": None,
                    "daterange": None,
                    "excluded_terms": None,
                    "included_terms": None,
                    "num_results": None,
                    "search_type": None,
                    "safe_search": None
                }
            }
        }
        