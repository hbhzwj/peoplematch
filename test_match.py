from match import *
mt = Matcher()
print(mt.get_matched_persons(1, 2))

BIO = 'Jing (Conan) Wang is a Ph.D. Student in Boston University advised by Professor Yannis Paschalidis. He got his B.E degree from Huazhong Univ. of Sci. and Tech., where he did some research about p2p network. In BU, he switched research interests to Internet traffic analysis and reinforcement learning, both of which are combination of machine learning and control theory. \n He has good knowledge of mathematical modelling. He received prize of Honorable Mention in Mathematical Contest in Modelling (MCM) 2009, and Second Prize inChinese Undergradute Mathematical Contest in Modelling (CUMCM) 2009. He is also a good programmer with extensive experience of open source development. He was a student developer for Google Summer of Code 2012 and a mentor for Goolge Summer of Code 2013. He also joined Camp of Microsoft Young Fellow in 2009.'

print mt.analyze_bio(BIO)

