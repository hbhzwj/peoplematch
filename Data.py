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
    def __init__(self):
        self.conn = psycopg2.connect("dbname='template1' user='wangjing' host='localhost' password='123456'")
        self.cur = self.conn.cursor()

    def get(self, user_id, field):
        query = 'SELECT %s FROM users WHERE id=%i;' % (field, user_id)
        print(query)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        # return [r[0] for r in rows]
        return rows[0][0]

    def set_skill_dist(self, user_id, skills):
        print('skills', skills)
        print('user_id', user_id)
        """set skill set of user_id. return a dict"""
        pass

    def filter_skill(self, skill, max_nums):
        return [1, 2, 3], [0.3, 0.2, 0.1]

    def get_all_skill_set(self):
        return ['python', 'ruby', 'machine learning', 'student', 'analysis',
                'development']


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
