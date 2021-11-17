# Create an ETL with Luigi, Pandas and SQLAlchemy in Python


## Luigi

Luigi is a Python module that helps you build complex pipelines of batch jobs. It handles dependency resolution, workflow management, visualization etc.

## Pandas

Pandas is a software library written for the Python programming language for data manipulation and analysis. In particular, it offers data structures and operations for manipulating numerical tables and time series.

## SQLAlchemy

SQLAlchemy is an open-source SQL toolkit and object-relational mapper for the Python programming language


## 9. Project repository structure

The following folders and files are contained in the project repository:

```
. capstone-project
│
│   README.md                                             # Project description and documentation
│   .gitignore                                            # Files and extension ignored in commited
│   requirements.txt                                      # Python requirements and libraries for project
│   docker-compose.yml                                    # Airflow and PostgresSQL containers
│   Markfile                                              # Install localy or use Composer
│   start.sh                                              # start services
│   stop.sh                                               # stop services
└───examples                                              # Luigi examples home  
```

<br/>

## How to use the Repository (for running locally in your machine)

<br/>

### Clone repository

``` bash
git clone https://github.com/dacosta-github/luigi-etl 
```

<br/>

### Change directory to local repository

```bash
cd luigi-etl
```

<br/>

### Start docker container

_Run this command in new terminal window or tab_

```bash
docker-compose up
```

_check containers_
```bash
docker ps # run in new terminal
```

<br/>

### Create and active python virtual environment

_Run these following commands in new terminal window or tab_
```bash
python3 -m venv venv            
source venv/bin/activate 
```

<br/>
   
### Install requirements

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt  
```

<br/>

## Preparation

```bash
sqlite3 db1
```

# References

https://kpatronas.medium.com/python-create-an-etl-with-luigi-pandas-and-sqlalchemy-d3cdc9292bc7
https://towardsdatascience.com/create-your-first-etl-in-luigi-23202d105174

