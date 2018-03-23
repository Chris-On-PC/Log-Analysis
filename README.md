# Log-Analysis

Building an informative summary from logs is a real task that comes up very often in software engineering. In this project, various SQL database techniques were implemented. A live database was used and interacted with through both the command line and from python code. Complex queries were used to draw business conclusions from data.

## Getting Started

You will need PostgreSQL to run the Python code for this project. Udacity provided a Linux virtual machine (VM) configuration that already contains the PostgreSQL database software. The software consist of:
 Markup : * The VirtualBox VM environment
          * The Vagrant configuration program

The database for this project was also provided by Udacity, newsdata.sql, and should be placed the vagrant directory, which is shared with your virtual machine. 

###Starting your VirtualBox

To start your virtual machine run "vagrant up" from inside your vagrant directory. Once the procedure has completed, log into it with vagrant ssh. You will then need to navigate to the shared vagrant directory "cd \vagrant"

### The database

The database for this project can be found at the following link: Markup :  [Download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

To load the data, cd into the vagrant directory and use the command psql -d news -f newsdata.sql.
Here's what this command does:

psql — the PostgreSQL command line program
-d news — connect to the database named news which has been set up for you
-f newsdata.sql — run the SQL statements in the file newsdata.sql
Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

## Explore the data
Once you have the data loaded into your database, connect to your database using psql -d news and explore the tables using the \dt and \d table commands and select statements.

\dt — display tables — lists the tables that are available in the database.
\d table — (replace table with the name of a table) — shows the database schema for that particular table.
Get a sense for what sort of information is in each column of these tables.

The database includes three tables:

The authors table includes information about the authors of articles.
The articles table includes the articles themselves.
The log table includes one entry for each time a user has accessed the site.
As you explore the data, you may find it useful to take notes! Don't try to memorize all the columns. Instead, write down a description of the column names and what kind of values are found in those columns.

## Python Program

Three questions had to be answered from the database. 

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

### Question 1

For question 1 the most popular article, along with its number of views had to be displayed. 

To accomplish this the "slug" column, containing the abbriviated/web-link version of the article title, from the articles table had to be compared with paths of the website visited. The "log" table contains the information saved on all the web activity. If the slugs matched, excluding the path of the specific article on the website, it would count towards the number of times that article was view. The articles were then grouped by their name and ordered by the number of times it was view in descending order. The top 3 most viewed articles were then displayed.

```
select title, count(path) as num 
from articles, log
where substring(log.path, 10, 100) = articles.slug
group by articles.title order by num desc limit 3
```

To execute this query the main.py file saved in the shared directory needs to be run by typing "python main.py" in your virtual machine's command line.
```
vagrant@vagrant:/vagrant$ python main.py

```

### Question 2

For question 2 the most popular artist had to be displayed along with the number of times their articles were viewed. 

This question built on the previous question. It required additional conditions to be added to the SQL query. On top of the previous question all that had to be done was link the article's author by their id from the "articles" table with the authors name through their id on the "author" table. They were then grouped by their name and ordered by the number of times the author's articles were viewed in descending order. 

```
select name, count(path) as num
from articles, log, authors
where substring(log.path, 10, 100) = articles.slug
and articles.author = authors.id
group by name order by num desc
```

To execute this query the main.py file saved in the shared directory needs to be run by typing "python main.py" in your virtual machine's command line.
```
vagrant@vagrant:/vagrant$ python main.py

```

### Question 3

Question 3 asked to determine which days more than 1% of the request lead to errors.

For this question two views were created. The first view counted the number of times a request lead to an error every day by checking fot the '404 NOT FOUND' status. 
The secoond view counted the number of requests to the server every day.  
The two views were then compared and the number of error responses were devided by the total number repsonses to get a percentage of error responses for each day. If the percentage was more than 1 percent it would be displayed along with the date it occured.

VIEWS
```
create view error as (select date(log.time) as
date_error, count(*) as num from log
where status = '404 NOT FOUND' group by date_error)

reate view alldata as (select date(log.time)
as date_all, count(*) as num from log
group by date_all)
```
The views were created by running the above SQL in the news databse. 
example:
```
news=> create view alldata as (select date(log.time) as date_all, count(*) as num from log group by date_all);
CREATE VIEW
```

Python
```
    query = """select to_char(alldata.date_all, 'Mon DD YYYY'),
            round(cast(error.num as numeric)/cast(alldata.num as numeric)*
            100, 1)
            as perecentage from alldata, error
            where error.date_error = alldata.date_all and
            cast(error.num as numeric)/cast(alldata.num as numeric)*100 >1"""
```
To execute this query the main.py file saved in the shared directory needs to be run by typing "python main.py" in your virtual machine's command line.
```
vagrant@vagrant:/vagrant$ python main.py

```
## Running the Queries

To execute the python program and gather the information from the database, make sure your virtual machine is running. From the command line running vagrant, execute the python program named "main.py". The will run the various queries against the database and return the onformation required. 