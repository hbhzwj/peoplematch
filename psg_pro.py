#!/usr/bin/env python

import psycopg2
import json
import glob
import os

class DBLoader(object):
    def __init__(self, dbname='template1', user='wangjing', host='localhost',
                 password='123456'):
        # conn = psycopg2.connect("dbname='template1' user='wangjing' host='localhost' password='123456'")
        self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"
                                % (dbname, user, host, password))
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE IF EXISTS users;")
        query = """CREATE TABLE users (
    first_name varchar(40),
    last_name varchar(40),
    name varchar(50),
    registered_user boolean,
    data_sources varchar(100),
    id integer unique,
    bio varchar(5000),
    skills varchar(1000),
    skill_string varchar(100),
    needs varchar(100),
    need_string varchar(100),
    linkedin_token varchar(40),
    github_token varchar(40),
    linkedin_username varchar(100),
    github_username varchar(40),
    linkedin_data_api varchar(1000),
    linkedin_data_scrape varchar(1000),
    linkedin_contact varchar(100),
    github_data varchar(1000),
    photo varchar(100),
    memberships varchar(50),
    jobs varchar(50),
    past_employers varchar(500),
    confirmed_skills varchar(300));"""
        print(query)
        self.cur.execute(query)

    def load_data(self):
        # initialize database
        i = 0
        for f_name in glob.glob('json/*.json'):
            i += 1
            f = open(f_name)
            p_data = json.loads(f.read())
            # print('data', p_data)
            f.close()
            self.write(p_data, i)

    def g(self, d, field):
        if field == 'skills':
            return ','.join(v.rsplit('\n')[0] for v in d.get(field, '').rsplit(','))
        return d.get(field, '').replace("'", '')


    def write(self, d, id):
        # bio = '%s %s %s' % (d['current_position'], d['past_positions'], d['location'])
        # import ipdb;ipdb.set_trace()
        # print(d)
        bio = ' '.join([
            self.g(d, 'current_position'),
            self.g(d, 'past_positions'),
            self.g(d, 'location'),
            self.g(d, 'current_employer'),
            self.g(d, 'past_employers')
        ])
        bio = bio.replace("'", '')
        query = """
        INSERT INTO users (id, name, linkedin_username, bio, past_employers, skills)
                    VALUES (%i, '%s', '%s', '%s', '%s', '%s');
        """ % (id, self.g(d, 'name'), self.g(d, 'linkedin_url'), bio,
               self.g(d, 'past_employers'), self.g(d, 'skills'))
        # print(query)
        self.cur.execute(query)

    def commit(self):
        self.conn.commit()


if __name__ == "__main__":

    # def __init__(self, dbname='template1', user='wangjing', host='localhost',
    #              password='123456'):
     db = DBLoader(dbname='d7n331rt3gahc0', user='jutwvmlolgopxw',
                   host='ec2-54-83-199-115.compute-1.amazonaws.com',
                   password='s2PhdUKIYrB1dx1MeCBfSADQo5')
     db.commit()
     db.load_data()
     db.commit()



# except:
#     print "I am unable to connect to the database"

# cur = conn.cursor()
# cur.execute("""SELECT datname from pg_database""")
# rows = cur.fetchall()

# print "\nShow me the databases:\n"
# for row in rows:
#     print "   ", row[0]
