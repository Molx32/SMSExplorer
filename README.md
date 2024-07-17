
# SMS Explorer

![alt text](static/readme.jpg?raw=true)

## Warning
The use of this repository is limited to research purposes only, and the owner does not encourage nor approves illegal activities.

## About
*SMS Explorer* was designed to fecth publicly available SMSs received on Public SMS Services (PSS) platforms. It can be run with two modes : 
- **Passive mode** - SMSs collected are simply stored in a local database, and can be explored in the web interface. 
- **Agressive mode** - When running agressively, an additional process runs and tries to identify if any URL is present in SMSs. If an URL is found, it will try to access it and according to the use case it will result in :
  - *Access user account compromission* - Information is  PII (Personal Identifiable Information).
  - *Fulfill password reset procedures* - Informations added are login/password.
  - *Collect personal data with no account compromission* - Information is  PII (Personal Identifiable Information).

Is it legal?
- When running passively, yes!
- When running agressively, probably not.

⚠️ MY ~1 MILLION SMS INSTANCE WILL BE RELEASED SOON AS A PUBLIC DEMO ⚠️

### Supported PSS

| PSS                      | Legal    | State |  
|--------------------------|----------|-------|
| https://receive-smss.com | Probably |  ✅   |
| More to come             |   N/A    | 🛠️    |

### Supported data collectors
| Target        | Domain                   | Legal    | State |  
|---------------|--------------------------|----------|-------|
| Ukrwds        | https://ukrwds.com/      | Probably |  ✅   |
| JobLogic      | TODO                     | No       |  🛠️   |
| FreeAds       | TODO                     | No       |  🛠️   |
| Payfone       | TODO                     | No       |  🛠️   |
| TextsFromMyEx | TODO                     | No       |  🛠️   |
| Instagram     | TODO                     | No       |  ❌   |
| ValidaHealth  | TODO                     | No       |  ❌   |
| StickerMule   | TODO                     | No       |  🛠️   |
| BankInter     | TODO                     | No       |  🛠️   |
| Experian      | TODO                     | No       |  ❌   |

## Use

### Run the app
#### Windows (local)
```PowerShell
git clone https://github.com/Molx32/SMSExplorer.git
cd SMSExplorer/
docker  compose  build
docker  compose  up
# Web server runs on 127.0.0.1:80
```

#### Linux (local)
```bash
git clone https://github.com/Molx32/SMSExplorer.git
cd SMSExplorer/
docker  compose  build
docker  compose  up
# Web server runs on 127.0.0.1:80
```

#### Linux (local)
```bash
# Docker install
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo install -m 0755 -d /etc/apt/keyrings

# Add Docker's official GPG key and repo
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update repo and install docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

git clone https://github.com/Molx32/SMSExplorer.git
cd SMSExplorer/
docker  compose  build
docker  compose  up
# Web server runs on 127.0.0.1:80
```

### Access database
On the database container, access the terminal and type the following.
```
-- Spawn bash in a container
-- Get container name and connect to database container (<name> should be smsexplorer-database-1)
docker container ls 
sudo docker exec -it <name> bash

-- Connect to database server
psql -u postgres 

-- List all databases
# \l

-- Connect to a database (<db_name> should be postres)
# \c <db_name>

-- List all tables in the database
# \dt

-- Dump the entire data table
# SELECT * FROM DATA;
```

### Backlog
Coming soon...



### Authors
Molx32