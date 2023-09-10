# About
Next step :
    - Add field "URL" to database
        - Add field "Code" to database

# About
OpenSMS was designed to fecth publicly available SMSs received though public receivers such as https://receive-smss.com.

## Architecture
The project uses docker to instanciate the following containers :

- Python main code
- Redis server
- Redis queue
- PostgreSQL database

# Use
## Run prod
```bash
docker compose build --no-cache
docker compose up
```


## Access database
Scrapy to look for files on non indexed domains
```
sudo -u postgres psql

-- List all databases
# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 files     | postgres | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 |
 postgres  | postgres | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 |

-- Connect to a database
# \c <db_name>

-- List all tables in the database
# \dt

```