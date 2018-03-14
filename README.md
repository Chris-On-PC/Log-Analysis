# Log-Analysis

Building an informative summary from logs is a real task that comes up very often in software engineering. In this project, various SQL database techniques were implemented. A live database was used and interacted with through both the command line and from python code. Complex queries were used to draw business conclusions from data.

## Getting Started

You will need PostgreSQL to run the Python code for this project. Udacity provided a Linux virtual machine (VM) configuration that already contains the PostgreSQL database software. The software consist of:
 Markup : * The VirtualBox VM environment
          * The Vagrant configuration program

The database for this project was also provided by Udacity, newsdata.sql, and should be placed the vagrant directory, which is shared with your virtual machine.     

##Python Program

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

### Question 2

For question 2 the most popular artist had to be displayed along with the number of times their articles were viewed. 

A new view of question 1's query was created since it sorted the articles by the number of times it was viewed. On top of that all that had to be done was link the article's author by their id from the "articles" table with the authors name through their id on the "author" table. They were then grouped by their name and ordered by the number of times the author's articles were viewed in descending order.


```
create view pop_art as select title, count(path) as num
from articles, log
where substring(log.path, 10, 100) = articles.slug
group by articles.title order by num desc

select name, sum(num) as numb
from (authors join articles on articles.author = authors.id)
as art_auth, pop_art group by name order by numb desc
```
### Question 3

Question 3 asked to determine which days more than 1% of the request lead to errors.

For this question two views were created. The first view counted the number of times a request lead to an error every day by checking fot the '404 NOT FOUND' status. 
The secoond view counted the number of times a request lead to an seccessful response from the server every day by checking for the '200 OK' status.  
The two views were then compared and the number of error responses were devided by the number of good repsonses to get a percentage of error responses for each day. If the percentage was more than 1 percent it would be displayed along with the date it occured.

```
create view error as (select date(log.time) 
as date_error, count(*) as num from log
where status = '404 NOT FOUND' group by date_error)

create view good as (select date(log.time)
as date_ok, count(*) as num from log
where status = '200 OK' group by date_ok)

select to_char(good.date_ok, 'Mon DD YYYY'),
round(cast(error.num as numeric)/cast(good.num as numeric)*100, 1)
as perecentage from good, error
where error.date_error = good.date_ok and
cast(error.num as numeric)/cast(good.num as numeric)*100 >1
```

## Running the Queries

To execute the python program and gather the information from the database, make sure your virtual machine is running. From the command line running vagrant, execute the python program named "main.py". The will run the various queries against the database and return the onformation required. 