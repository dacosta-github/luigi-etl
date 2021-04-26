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
└───airflow                                               # Airflow home  
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

### 10.4. Create and active python virtual environment

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

create table names (id varchar(10) primary key, first_name text, last_name text);
insert into names values('2','john','doe');
insert into names values('3','jenny','doe');

.mode list
SELECT * from names;



sqlite3 db2
Enter the following lines:
create table salaries (id varchar(10) primary key, salary integer);
insert into salaries values('1',10000);
insert into salaries values('2',13000);
insert into salaries values('3',23000);

.mode list
SELECT * from salaries;






How we can combine Luigi, Pandas and SQLAlchemy?
If we didn't want to use an ETL framework as Luigi and use traditional methods like batch scripting we would need to worry for things like dependency handling of the various jobs that compose the pipeline, or we would need create logging mechanisms to keep metrics about the execution of each pipeline step, Luigi automatically tackles those problems with built in support for all the things we mentioned, thus that also provides a very nice web ui to visualize our pipelines.
SQLAlchemy with its support for a large number of databases is a great solution if your infrastructure has more than one type of SQL Database, you use Postgress? no problem, SQLAlchemy can connect, execute any queries you want, you Have MS SQL? the same! all without having the need to use different many Database libraries with different syntax.
Pandas can help us in the transformation part of the data, converting the rows to dataframes allows us very quickly and in a large scale to do operations like data cleaning, merging, adding or transforming things and then creating a report in any format we want, like xls or just preparing the data for a next step of our ETL pipeline
Scenario:
We have a very simple scenario just to demonstrate the combination of those libraries to create the ETL, we have two different databases db1 and db2, db1 has a table called “names” and has the id, first name and last name of our employees, and db2 has a table named “salaries” with an id and the salary, the task is to get all data from “names” and “salaries” and create a CSV with the two tables merged with the unique id.
Preparation:
We need to create the databases for this example and install the python libraries we need, we will use sqlite in this example which does not require an SQL server installed and configured.
$ sudo pip3 install pandas
$ sudo pip3 install sqlalchemy
$ sudo pip3 install luigi
on the command line enter:
$ sqlite3 db1
Enter the following lines:
create table names (id varchar(10) primary key, first_name text, last_name text);
insert into names values('2','john','doe');
insert into names values('3','jenny','doe');
Exit sqlite.
On the command line enter:
$ sqlite3 db2
Enter the following lines:
create table salaries (id varchar(10) primary key, salary integer);
insert into salaries values('1',10000);
insert into salaries values('2',13000);
insert into salaries values('3',23000);
Exit sqlite.
Create a new python file (luigi_etl.py) and enter the following:
#!/usr/bin/env python3
from sqlalchemy import create_engine
import luigi
import pandas as pd
Those lines will import sqlalchemy, luigi and pandas, you might need first to install those libraries using pip
Solution:
We need first to have a look how Luigi works, each Luigi task has three steps, the first one is to check if it needs another task(s) to be completed, needs to know where to store the data that its-self will generate and also needs instructions what commands to run to generate the data.
In the same file enter the following:
class QueryDB1(luigi.Task):
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget("DB1_output.csv")
    def run(self):
        engine = create_engine('sqlite:///db1')
        results = pd.read_sql_query('SELECT * from names',engine)
        f = self.output().open('w')
        results.to_csv(f,encoding = 'utf-8',index=False,header=True,quoting=2)
        f.close()
This class is our first task, it will connect to db1 database and will export all data from names table to DB1_output.csv
function requires() checks if it needs another task to be completed first.
output() defines where to write the ouput, on a production pipeline this could be more complex, like deleting previous files, or dropping tables, or defying files based on a datestamp.
run() is the code that will be executed in order to get/generate the data for this task
In the same file enter:
class QueryDB2(luigi.Task):
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget("DB2_output.csv")
    def run(self):
        engine = create_engine('sqlite:///db2')
        results = pd.read_sql_query('SELECT * from salaries',engine)
        f = self.output().open('w')
        results.to_csv(f,encoding = 'utf-8',index=False,header=True,quoting=2)
        f.close()
This class is just like QueryDB2 but has a different query and a different database as source, it will get all data from the salaries table.
Again in the same file:
class CreateReport(luigi.Task):
    def requires(self):
        return [QueryDB1(),QueryDB2()]
    def output(self):
        return luigi.LocalTarget("Report.csv")
    def run(self):
        df1 = pd.read_csv("DB1_output.csv", header = 0, encoding = 'utf-8',index_col = False)
        df2 = pd.read_csv("DB2_output.csv", header = 0, encoding = 'utf-8',index_col = False)
        df3 = pd.merge(df1,df2,how='inner',on=['id'])
        f = self.output().open('w')
        df3.to_csv(f,encoding = 'utf-8',index=False,header=True,quoting=2)
        f.close()
This class is a bit different, in the require function as a list with the names of the other two classes, if those two classes are not executed the CreateReport class will fail with an error.
The run function reads the data from the classes executed and creates a new dataframe which are merged with the common column named “id” and saved as a csv named Report.csv
And finally in the same file enter:
if __name__ == '__main__':
    luigi.run(main_task_cls=CreateReport,local_scheduler=False)
What this line does is to instruct luigi which class to execute, and to connect to the Web UI (luigid) in order to create a dashboard with our executed ETL pipeline with various metrics.
Start the luigi dashboard and execute the pipeline
$ nohup luigid&
$ python etl.py
If you dont have any typos you should see something like this:

On our browser enter localhost:8082, you should see something like this

On the left you can see the executed classes
Clicking on the CreateReport class will show metrics about the last execution along with a visualization of the etl pipeline.

I hope you found this article interesting :)


https://kpatronas.medium.com/python-create-an-etl-with-luigi-pandas-and-sqlalchemy-d3cdc9292bc7


https://towardsdatascience.com/create-your-first-etl-in-luigi-23202d105174

