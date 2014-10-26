#!/usr/bin/env python
# XXX need to implement a real data object, implement judge_skills, and
# analyze_bio

from __future__ import print_function, division, absolute_import
import sets

# import numpy as np
def argsort(seq):
    return sorted(range(len(seq)), key = seq.__getitem__, reverse=True)

class Data(object):
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

def set_dict(d, v, w):
    d.update(dict(zip(v, w)))

class Matcher(object):
    def __init__(self):
        self.data = Data()

    def judge_skills(self, user_id, skills):
        # XXX IMPLEMENT ME
        # the skill rate is based on the frequence of skill words in this
        # person's description
        return [1] * len(skills)

    def analyze_bio(self, bio):
        # XXX IMPLEMENT ME
        # identify skills from bio. identify some interesting topics from bio.
        # cv = sklearn.feature_extraction.text.CountVectorizer()
        # cv.fit_transform(bio)
        # import ipdb;ipdb.set_trace()
        no_special_char_bio = ''.join(e if e.isalnum() else ' ' for e in bio)

        # count frequency in tokens
        tokens = no_special_char_bio.rsplit()
        from collections import defaultdict
        d = defaultdict(int)
        for token in tokens:
            d[token] += 1

        skill_counts = dict()
        all_skill_set = self.data.get_all_skill_set()
        for k in all_skill_set:
            tmp = d.get(k, 0)
            if tmp:
                skill_counts[k] = tmp

        return skill_counts.keys(), skill_counts.values()

    def store_skill_dist(self, user_id):
        skills = self.get_skill_dist(user_id)
        self.data.set(user_id, skills)

    def get_skill_dist(self, user_id):
        """ each skill is a dictionary mapping skill to weight"""
        skills = dict()

        # analyze skills
        bio = self.data.get(user_id, 'bio')
        bio_skills, bio_skills_weights = self.analyze_bio(bio)
        set_dict(skills, bio_skills, bio_skills_weights)

        # check user boasted skills
        boasted_skills = self.data.get(user_id, 'skills')
        skill_weights = self.judge_skills(user_id, boasted_skills)
        set_dict(skills, boasted_skills, skill_weights)

        # skills confirmed by user's friends
        confirmed_skills = self.data.get(user_id, 'confirmed_skills')
        set_dict(skills, confirmed_skills, [1] * len(confirmed_skills))

        return skills

    def merge_users(self, users_list, ratings_list, all_users):
        result = dict(zip(all_users, [0] * len(all_users)))
        # import ipdb;ipdb.set_trace()
        weights = [1] * len(users_list) # FIXME change to more dynamic weights
        for users, ratings, w in zip(users_list, ratings_list, weights):
            for i in xrange(len(users)):
                result[users[i]] += ratings[i] * w
        return result.keys(), result.values()

    def get_matched_persons(self, user_id, max_nums):
        skill_dist = self.get_skill_dist(user_id)
        needs = self.data.get(user_id, 'needs')
        users_list = []
        ratings_list = []
        all_users = sets.Set()
        for skill in needs:
            users, ratings = self.data.filter_skill(skill, max_nums)
            all_users = all_users.union(users)
            users_list.append(users)
            ratings_list.append(ratings)

        users, ratings = self.merge_users(users_list, ratings_list, all_users)
        # print('ratings', ratings)

        # idx = argsort(ratings)[::-1]
        idx = argsort(ratings)
        users = [users[i] for i in idx]
        # users = np.array(users)[idx]
        return users[0:max_nums]

    def query(self, user_id, max_nums):
        return {
            'matched_ids': self.get_matched_persons(user_id, max_nums),
        }

if __name__ == "__main__":
    mt = Matcher()
    print(mt.get_matched_persons(1, 2))
    pass

