# DorkStorm

DorkStorm is a powerful tool for hacking with Google dorks. DorkStorm allows security researchers, penetration testers, and ethical hackers to easily search and discover hidden information on the internet. By leveraging advanced Google search operators, DorkStorm can uncover vulnerabilities and sensitive data that may be exposed online, helping security professionals to identify potential attack vectors and assess the security posture of their targets. DorkStorm is designed to be customizable, allowing users to create their own dork queries and save them for future use. It also includes a number of built-in search templates for common use cases, such as finding vulnerable web applications or leaked passwords. DorkStorm is built with security in mind and takes care to protect user privacy and data confidentiality. It includes a range of safety features to ensure that users are not accidentally exposing sensitive information, such as blacklists for known malicious websites and automatic detection of potentially harmful queries. Whether you're a seasoned security professional or a beginner just starting out with Google dorks, DorkStorm is the perfect tool for hacking and discovering hidden information on the internet.

## Installation

To install the project and its dependencies, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/cryxnet/dorkstorm.git
```

2. Navigate to the project directory:

```bash
cd dorkstorm
```

3. Create a virtual environment for the project:

```bash
python -m venv venv
```

4. Activate the virtual environment:

**On Windows:**

```bash
venv\Scripts\activate
```

**On macOS or Linux:**

```bash
source venv/bin/activate
```

5. Install the project dependencies:

```bash
pip install -r requirements.txt
```

6. Go the directory where the main file is located and execute it

```bash
cd dorkstorm &&
python dorkstorm.py
```

## Usage

```bash
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
        save query    Saves the current query that is stored in context | save query
        execute       Executes the query | execute <flag> (--headless (--limit pages), --browser)
        pentest site  Execute all queries to a website | pentest site <domain>

        quit / exit   Exit the program
```

## Data

-   We are using the [ExploitDB | GHDB](https://www.exploit-db.com/google-hacking-database) database for all the base queries.
-   We get the data from the ghdb.xml file that is stored in the [Gitlab | Exploit-DB](https://gitlab.com/exploit-database/exploitdb/-/blob/main/ghdb.xml) repository

## Disclaimer

YOUR USAGE OF THIS PROJECT CONSTITUTES YOUR AGREEMENT TO THE FOLLOWING TERMS:

    THE MISUSE OF THE DATA PROVIDED BY THIS PROJECT AND ITS MALWARES MAY LEAD TO CRIMINAL CHARGES AGAINST THE PERSONS CONCERNED.

    I DO NOT TAKE ANY RESPONSIBILITY FOR THE CASE. USE THIS PROJECT ONLY FOR RESEARCH PURPOSES, EDUCATIONAL PURPOSES & ETHICAL ONLY.

    DorkStorm is a project related to Computer Security and for Educational Purposes and not a project that promotes illegal activities.

    Don't use this Project for any illegal activities.

    If something happens, we do not take any liability.

    DorkStorm should be considered as a project for educational purposes.

## Author

Created by [cryxnet](https://cryxnet.com/)

If you find this project helpful, please give it a ⭐️ on GitHub to show your support.
I would also appreciate it if you shared it with others who might find it useful!
