#!/usr/bin/env python
# XXX need to implement a real data object, implement judge_skills, and
# analyze_bio

from __future__ import print_function, division, absolute_import
import sets
from Data import Data

# import numpy as np
def argsort(seq):
    return sorted(range(len(seq)), key = seq.__getitem__, reverse=True)

def set_dict(d, v, w):
    d.update(dict(zip(v, w)))

class Matcher(object):
    def __init__(self):
        self.data = Data(dbname='d7n331rt3gahc0', user='jutwvmlolgopxw',
                   host='ec2-54-83-199-115.compute-1.amazonaws.com',
                   password='s2PhdUKIYrB1dx1MeCBfSADQo5')

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

        # get the frequency of all skill_set keyworlds
        skill_counts = dict()
        all_skill_set = self.data.get_all_skill_set()
        for k in all_skill_set:
            tmp = d.get(k, 0)
            if tmp:
                skill_counts[k] = tmp

        return skill_counts.keys(), skill_counts.values()

    def store_skill_dist(self, user_id):
        skills = self.get_skill_dist(user_id)
        self.data.set_skill_dist(user_id, skills)

    def get_skill_dist(self, user_id):
        """ each skill is a dictionary mapping skill to weight"""
        skills = dict()

        # analyze skills
        bio = self.data.get(user_id, 'bio')
        if bio:
            bio_skills, bio_skills_weights = self.analyze_bio(bio)
            set_dict(skills, bio_skills, bio_skills_weights)

        # check user boasted skills
        boasted_skills = self.data.get(user_id, 'skills')
        if boasted_skills:
            boasted_skills = boasted_skills.rsplit(',')
            skill_weights = self.judge_skills(user_id, boasted_skills)
            set_dict(skills, boasted_skills, skill_weights)

        # skills confirmed by user's friends
        confirmed_skills = self.data.get(user_id, 'confirmed_skills')
        if confirmed_skills:
            confirmed_skills = confirmed_skills.rsplit(',')
            set_dict(skills, confirmed_skills, [1] * len(confirmed_skills))

        print('skills', skills)
        return skills

    def merge_users(self, users_list, ratings_list, all_users):
        result = dict(zip(all_users, [0] * len(all_users)))
        weights = [1] * len(users_list) # FIXME change to more dynamic weights
        for users, ratings, w in zip(users_list, ratings_list, weights):
            for i in xrange(len(users)):
                result[users[i]] += ratings[i] * w
        return result.keys(), result.values()

    def get_matched_persons(self, user_id, max_nums, needs):
        skill_dist = self.get_skill_dist(user_id)
        # needs = self.data.get(user_id, 'needs')
        needs = needs.split(',')
        if not needs or needs == [''] or needs == ['all']:
            needs = self.data.get_all_skill_set()
        return needs
        users_list = []
        ratings_list = []
        all_users = sets.Set()
        for skill in needs:
            users, ratings = self.data.filter_skill(skill, max_nums)
            all_users = all_users.union(users)
            users_list.append(users)
            ratings_list.append(ratings)

        users, ratings = self.merge_users(users_list, ratings_list, all_users)

        idx = argsort(ratings)
        users = [users[i] for i in idx]
        return users[0:max_nums]

    def query(self, user_id, max_nums):
        return {
            'matched_ids': self.get_matched_persons(user_id, max_nums),
        }

if __name__ == "__main__":
    mt = Matcher()
    mt.data.init_skill_dist()
    mt.store_skill_dist(1)
    mt.store_skill_dist(2)
    # print(mt.get_matched_persons(2, 2, ''))
    print(mt.get_matched_persons(2, 2, 'all'))
    pass

