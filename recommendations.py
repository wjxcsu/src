# -*- coding: utf-8 -*-
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}
import math
#计算距离 欧式距离
def sim_distance(prefs,person1,person2):
	sum=0
	for item in prefs[person1]:
		if item in prefs[person2]:
			sum+=math.pow(prefs[person1][item]-prefs[person2][item],2)
	return 1/(1+math.sqrt(sum))
	
#计算距离 皮尔逊相关度
def sim_person(prefs,p1,p2):
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1
	n=len(si)
	if n==0:return 1

	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	sum1Sq=sum([math.pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([math.pow(prefs[p2][it],2) for it in si])

	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	num=pSum-(sum1*sum2/n)
	den=math.sqrt((sum1Sq-math.pow(sum1,2)/n)*(sum2Sq-math.pow(sum2,2)/n))	
	if den==0:return 0
	return num/den 

#计算前n个与自己相似的人
def topMatches(prefs,person,n=5,similarity=sim_person):
	score=[(similarity(prefs,person,people),people) for people in prefs if people!=person]
	score.sort(reverse=True)
	return score[0:n]
#获得推荐的电影
def getRecommendations(prefs,person,similarity=sim_person):
	totals={}
	simSums={}
	for other in prefs:
		if other!=person:
			sim=similarity(prefs,person,other)
			if sim<0:continue
		for item in prefs[other]:
			if item not in prefs[person]:
				totals.setdefault(item,0)
				totals[item]+=sim*prefs[other][item]
				simSums.setdefault(item,0)
				simSums[item]+=sim
	ranking=[(totals[item]/simSums[item],item) for item in totals]
	ranking.sort(reverse=True)
	return ranking
	
	
	
#对critics进行转置，得到以影片为主键的词典
def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person]=prefs[person][item]
	return result
	
	
	
#计算每部影片的与别的影片的相似度
def calculateSimilarItems(prefs,n=10):
	result={}
	itemPrefs=transformPrefs(prefs)
	c=0
	for item in itemPrefs:
		c+=1
		if c%100==0:
			print '%d/%d'%(c,len(itemPrefs))
		scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
		result[item]=scores
	return result
	
	
def getRecommendedItems(prefs,itemMatch,user):
	userRatings=prefs[user]
	score={}
	totalSim={}
	for (item,rating) in userRatings.items():
		for (similarity,item2) in itemMatch[item]:
			if item2 in userRatings:continue
			score.setdefault(item2,0)
			score[item2]+=similarity*rating
			totalSim.setdefault(item2,0)
			totalSim[item2]+=similarity
	ranking=[(score/totalSim[item],item) for item,score in score.items()]
	ranking.sort(reverse=True)
	return ranking
	
	
	
print 'git learning...'