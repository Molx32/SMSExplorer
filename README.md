
 # PROJECT NAME

## About
TODO was designed to fecth publicly available SMSs received on Public SMS Services (PSS) platforms. It can be run with two modes : 
- **Passive mode** - SMSs collected are simply stored in a local database, and can be explored in the web interface. 
- **Agressive mode** - When running agressively, an additional process runs and tries to identify if any URL is present in SMSs. If an URL is found, it will try to access it and according to the use case it will result in :
  -  *Access user account compromission* - Information is  PII (Personal Identifiable Information).
  - *Fulfill password reset procedures* - Informations added are login/password.
  - *Collect personal data with no account compromission* - Information is  PII (Personal Identifiable Information).

Is it legal?
- When running passively, yes!
- When running agressively, probably not.

### Supported PSS

| PSS                      | Legal    | State |  
|--------------------------|----------|-------|
| https://receive-smss.com | Probably |  ✅   |
| More to come             |   N/A    | 🛠️    |

### Supported data collectors
| Target        | Legal    | State |  
|---------------|----------|-------|
| AirIndia      | Probably |  ✅   |
| JobLogic      | No       |  🛠️   |
| FreeAds       | No       |  🛠️   |
| Payfone       | No       |  🛠️   |
| TextsFromMyEx | No       |  🛠️   |
| Instagram     | No       |  ❌   |
| ValidaHealth  | No       |  ❌   |
| StickerMule   | No       |  🛠️   |
| BankInter     | No       |  🛠️   |
| Experian      | No       |  ❌   |

  

## Use

### Run the app
```bash
docker  compose  build
docker  compose  up
```
### Access the website
Navigate to 127.0.0.1:9000.

### Access database
On the database container, access the terminal and type the following.
```
-- Connect to database server
psql -u postgres 

-- List all databases
# \l

-- Connect to a database
# \c <db_name>

-- List all tables in the database
# \dt

-- Dump the entire data table
# SELECT * FROM DATA;
```

## Architecture

The project uses docker to instanciate the following containers :

- Python main code
- Redis server
- Redis queue
- PostgreSQL database


### TODO
✅
🛠️
❌

- Everything
    - Add proper data handling (reassigned values e.g. 'YES' becomes True) - In progress
    - Add security for every endpoint - In progress
    - Handle error pages
- Automated 'About' tables based on database
- Statistics
    - 'Contains URLs'     --> Display statistics with only SMSs with URLs
    - 'Known valid URLs'  --> Display statistics with only SMSs with URLs known to hide data
    - 'Data URL'          --> Display statistics with only SMSs with URLs with automated data collection
- Collection
  - Add new data sources
- RESOLVE THE RACE CONDITION CASE...

### Authors
Molx32