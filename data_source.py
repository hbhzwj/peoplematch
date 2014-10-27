#!/usr/bin/env python
from __future__ import print_function, division, absolute_import
import psycopg2
from util import escape_keyword as ek

class Table(object):
    def __init__(self, conn, table_name, scheme):
        self.conn = conn
        self.cur = conn.cursor()
        self.table_name = table_name
        self.scheme = scheme

    def init_table(self):
        self.cur.execute("DROP TABLE IF EXISTS %s;" % (self.table_name))
        fields = ','.join(name + ' ' + tp for name, tp in self.scheme)
        query = """CREATE TABLE %s (%s);""" % (self.table_name, fields)
        self.cur.execute(query)
        self.conn.commit()
        print(query)

    def get_col_names(self):
        query = """SELECT column_name FROM information_schema.columns where
                   table_name='%s'""" % (self.table_name)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return [r[0] for r in rows]

    def add_col(self, col_name, tp='real', desc='NOT NULL', default='DEFAULT(0)'):
        query = 'ALTER TABLE %s ADD COLUMN %s %s %s %s;' %\
                (self.table_name, col_name, tp, desc, default)
        self.cur.execute(query)

    def select(self, row, col):
        query = 'SELECT %s FROM %s WHERE %s;' % (col, self.table_name, row)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows



class UserTable(Table):
    # def __init__(self, dbname='template1', user='wangjing', host='localhost',
    #              password='123456'):
    #     self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"
    #                             % (dbname, user, host, password))
        # self.cur = self.conn.cursor()

    def get(self, user_id, field):
        rows = self.select('id=%i' % (user_id), field)
        return rows[0][0]

    def get_all_user_id(self):
        query = """SELECT id FROM users;"""
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return [r[0] for r in rows]


class SkillTable(Table):
    def set_skill_dist(self, user_id, skills):
        print('user_id', user_id)
        all_skills = self.get_all_skill_set()
        skill_names = [ek(k) for k in skills.keys()]
        new_skills = set(skill_names) - set(all_skills)
        for a in new_skills:
            self.add_col(a, tp='real', desc='NOT NULL', default='DEFAULT(0)')
            # self.conn.commit()

        if len(skills) == 0:
            return

        keys = [ek(k) for k in skills.keys()]
        values = skills.values()
        from collections import defaultdict
        d = defaultdict(float)
        for k, v in zip(keys, values):
            d[k] += v
        keys = d.keys()
        values = d.values()

        query = """INSERT INTO %s (id, %s) VALUES (%i, %s)""" % \
                (self.table_name, ','.join(keys),
                 user_id,
                 ','.join(str(v) for v in values))
        print('query', query)

        self.cur.execute(query)
        self.conn.commit()

    def filter_skill(self, skill, max_nums):
        skill = ek(skill)
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
        col_names = self.get_col_names()
        col_names.remove('id')
        return col_names


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
