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
        pass

    def set(self, user_id, skills):
        """set skill set of user_id. return a dict"""
        pass

    def filter_skill(self, skill, max_nums):
        # XXX
        return [1, 2, 3], [0.3, 0.2, 0.1]

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
        return [], []

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

