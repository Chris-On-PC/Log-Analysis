#!/usr/bin/env python3
import psycopg2


def popular_articles():
    """Returns a list of the most popular three articles of all time."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """select title, count(path) as num from articles, log
                where substring(log.path, 10, 100) = articles.slug
                group by articles.title order by num desc limit 3"""
    c.execute(query)
    rows = c.fetchall()
    db.close()
    print("A list of the most popular three articles of all time")
    print("{} - {} views" .format(rows[0][0], rows[0][1]))
    print("{} - {} views" .format(rows[1][0], rows[1][1]))
    print("{} - {} views" .format(rows[2][0], rows[2][1]))
    print("")  # Empty space
    return rows


def popular_authors():
    """Returns a list of most popular article authors of all time."""

    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """create view pop_art as select title, count(path) as num
                from articles, log
                where substring(log.path, 10, 100) = articles.slug
                group by articles.title order by num desc"""
    c.execute(query)
    query = """select name, sum(num) as numb
                from (authors join articles on articles.author = authors.id)
                as art_auth, pop_art group by name order by numb desc"""
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

    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """create view error as (select date(log.time) as
                date_error, count(*) as num from log
                where status = '404 NOT FOUND' group by date_error)"""
    c.execute(query)
    query = """create view good as (select date(log.time)
                as date_ok, count(*) as num from log
                where status = '200 OK' group by date_ok)"""
    c.execute(query)
    query = """select to_char(good.date_ok, 'Mon DD YYYY'),
            round(cast(error.num as numeric)/cast(good.num as numeric)*100, 1)
            as perecentage from good, error
            where error.date_error = good.date_ok and
            cast(error.num as numeric)/cast(good.num as numeric)*100 >1"""
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
