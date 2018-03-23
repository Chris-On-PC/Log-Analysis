#!/usr/bin/env python3
import psycopg2


def connect(database_name="news"):

    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error")


def popular_articles():
    """Returns a list of the most popular three articles of all time."""
    db, c = connect()

    query = """select title, count(path) as num from articles, log
                where substring(log.path, 10, 100) = articles.slug
                group by articles.title order by num desc limit 3"""

    c.execute(query)
    rows = c.fetchall()
    db.close()
    print("A list of the most popular three articles of all time")

    for i in rows:
        print("{} - {} views" .format(i[0], i[1]))
    print("")  # Empty space
    return rows


def popular_authors():
    """Returns a list of most popular article authors of all time."""

    db, c = connect()

    query = """select name, count(path) as num
                from articles, log, authors
                where substring(log.path, 10, 100) = articles.slug
                and articles.author = authors.id
                group by name order by num desc """
    c.execute(query)
    rows = c.fetchall()
    db.close()
    print("A list of the most popular article authors of all time")
    for i in rows:
        print("{} - {} views" .format(i[0], i[1]))
    print("")  # Empty space
    return rows


def error_days():
    """Returns the days on which more than 1% of requests lead to errors."""

    db, c = connect()

    # query = """create view error as (select date(log.time) as
    #            date_error, count(*) as num from log
    #            where status = '404 NOT FOUND' group by date_error)"""
    # c.execute(query)
    # query = """create view alldata as (select date(log.time)
    #            as date_all, count(*) as num from log
    #            group by date_all)"""
    # c.execute(query)

    query = """select to_char(alldata.date_all, 'Mon DD YYYY'),
            round(cast(error.num as numeric)/cast(alldata.num as numeric)*
            100, 1)
            as perecentage from alldata, error
            where error.date_error = alldata.date_all and
            cast(error.num as numeric)/cast(alldata.num as numeric)*100 >1"""
    c.execute(query)
    rows = c.fetchall()
    db.close()
    print("The days on which more than 1% of requests lead to errors")
    for i in rows:
        print("{} - {}%" .format(i[0], i[1]))
    print("")  # Empty space
    return rows


popular_articles()
popular_authors()
error_days()
