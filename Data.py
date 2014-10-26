#!/usr/bin/env python
from __future__ import print_function, division, absolute_import
import psycopg2

# try:
# conn = psycopg2.connect("dbname='template1' user='wangjing' host='localhost' password='123456'")
# except:
#     print "I am unable to connect to the database"

# cur = conn.cursor()
# cur.execute("""SELECT datname from pg_database""")
# rows = cur.fetchall()

# print "\nShow me the databases:\n"
# for row in rows:
#     print "   ", row[0]

class Data(object):
    def __init__(self, dbname='template1', user='wangjing', host='localhost',
                 password='123456'):
        self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"
                                % (dbname, user, host, password))
        self.cur = self.conn.cursor()

    def get(self, user_id, field):
        query = 'SELECT %s FROM users WHERE id=%i;' % (field, user_id)
        print(query)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        # print('rows', rows)
        # return [r[0] for r in rows]
        return rows[0][0]


    def init_skill_dist(self):
        asd = ['python', 'ruby', 'machinelearning', 'student', 'analysis',
                'development']
        asd_query = ',\n'.join(self.escape(a, 'skill') + ' real' for a in asd)
        self.cur.execute("DROP TABLE IF EXISTS skill_sets;")
        query = """CREATE TABLE skill_sets (id integer unique, %s);""" % (asd_query)
        print(query)
        self.cur.execute(query)

    def escape(self, d, tp):
        if tp == 'skill':
            d = ''.join(e.lower() if e.isalnum() else '_' for e in d)
            return d

    def set_skill_dist(self, user_id, skills):
        all_skills = self.get_all_skill_set()
        skill_names = [self.escape(k, 'skill') for k in skills.keys()]
        new_skills = set(skill_names) - set(all_skills)
        if new_skills:
            for a in new_skills:
                # create a new column
                query = 'ALTER TABLE skill_sets ADD COLUMN %s real NOT NULL DEFAULT(0);' % (a)
                self.cur.execute(query)
            self.conn.commit()

        if len(skills) == 0:
            return

        keys = [self.escape(k, 'skill') for k in skills.keys()]
        values = skills.values()
        from collections import defaultdict
        d = defaultdict(float)
        for k, v in zip(keys, values):
            d[k] += v
        keys = d.keys()
        values = d.values()

        query = """INSERT INTO skill_sets (id, %s) VALUES (%i, %s)""" % \
                (','.join(keys),
                 user_id,
                 ','.join(str(v) for v in values))
        print('query', query)

        self.cur.execute(query)
        self.conn.commit()
        # print('skills', skills)
        # print('user_id', user_id)
        # """set skill set of user_id. return a dict"""
        # pass



    def filter_skill(self, skill, max_nums):
        # return [1, 2, 3], [0.3, 0.2, 0.1]
        skill = self.escape(skill, 'skill')
        query = """SELECT id, %s FROM skill_sets ORDER BY %s desc limit %i""" % \
                (skill, skill, max_nums)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        ids = []
        ratings = []
        for i, r in rows:
            if not r: break
            ids.append(i)
            ratings.append(r)
        return ids, ratings

    def get_all_skill_set(self):
        # return None
        query = """SELECT column_name FROM information_schema.columns where
                   table_name='skill_sets'"""
        self.cur.execute(query)
        rows = self.cur.fetchall()
        all_skill_set = [r[0] for r in rows if r[0] != 'id']
        return all_skill_set

    def get_all_user_id(self):
        query = """SELECT id FROM users;"""
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return [r[0] for r in rows]


class TestData(object):
    def get(self, user_id, field):
        if field == "confirmed_skills":
            return ['python', 'javascript']
        elif field == "skills":
            return []
        elif field == 'needs':
            return ['python', 'design']
        elif field == 'bio':
            return 'Jing (Conan) Wang is a Ph.D. Student in Boston University advised by Professor Yannis Paschalidis. He got his B.E degree from Huazhong Univ. of Sci. and Tech., where he did some research about p2p network. In BU, he switched research interests to Internet traffic analysis and reinforcement learning, both of which are combination of machine learning and control theory. \n He has good knowledge of mathematical modelling. He received prize of Honorable Mention in Mathematical Contest in Modelling (MCM) 2009, and Second Prize inChinese Undergradute Mathematical Contest in Modelling (CUMCM) 2009. He is also a good programmer with extensive experience of open source development. He was a student developer for Google Summer of Code 2012 and a mentor for Goolge Summer of Code 2013. He also joined Camp of Microsoft Young Fellow in 2009.'

    def set(self, user_id, skills):
        """set skill set of user_id. return a dict"""
        pass

    def filter_skill(self, skill, max_nums):
        # XXX
        return [1, 2, 3], [0.3, 0.2, 0.1]

    def get_all_skill_set(self):
        return ['python', 'ruby', 'machine learning', 'student', 'analysis',
                'development']



if __name__ == "__main__":
     dt = Data()
     print(dt.get(1, 'linkedin_username'))
