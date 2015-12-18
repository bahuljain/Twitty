import csv
import json
import collections

class Matcher:

    def __init__(self, items):
        self.usersInfo = items
        self.usersInfoDict = dict()
        self.getUsersInfoDynamo(items)
        self.commonInterests = collections.defaultdict(list)

    def getUsersInfoDynamo(self, items):
        for item in items:
            self.usersInfoDict[item['user_id']] = item

    def getUsersInfo(self):
        with open('db/twitty-users.csv','rb') as fin:
            dr = csv.DictReader(fin)
            for row in dr:
            	self.usersInfo.append(row)
                self.usersInfoDict[str(row['user_id (N)'])] = row

    def getUsersCount(self):
        return len(self.usersInfo)

    def getUserMatches(self, user_id):
        return self.commonInterests[user_id]

    # finds matches for all users in db with all other users in the database 
    def doMatching(self):
        for i in range(0,self.getUsersCount()-1):
            self.match(self.usersInfo[i], self.usersInfo[i+1:])

    # Given a user and an array of users it finds out what common interests each user in the array
    # shares with the given user
    def match(self, cur_user, all_users):
        for user in all_users:
            commonInterests = self.findCommonInterests(cur_user['interests'], user['interests'])
            
            if len(commonInterests) > 0:
                
                self.commonInterests[user['user_id']].append({
                    'with': cur_user['user_id'],
                    'interests': commonInterests,
                })

                self.commonInterests[cur_user['user_id']].append({
                    'with': user['user_id'],
                    'interests': commonInterests,
                })

    def findCommonInterests(self, dict1, dict2):
        # dict1 = json.loads(dict1)
        # dict2 = json.loads(dict2)
     
        commonInterests = dict()
        for id in dict1:
            if id in dict2:
                commonInterests[id] = dict1[id]
                
        return commonInterests    

    def getCommonInterests(self):
        return self.commonInterests
        
    def getTwitterGraph(self):
        nodes = list()
        edges = list()
        visited = collections.defaultdict(bool)

        for user in self.usersInfo:
            visited[user['user_id']] = True

            nodes.append({
                'id': int(user['user_id']), 
                'title': user['name'], 
                'image': user['profile_image_url'],
            });

            if self.commonInterests[user['user_id']]:
                for match in self.commonInterests[user['user_id']]:
                    if not visited[match['with']]:
                        if len(match['interests']) > 1:
                            title = ', '.join(match['interests'][id] for id in match['interests'])

                            edges.append({
                                'from': int(user['user_id']),
                                'to': int(match['with']), 
                                'title': title,
                            });

        return (nodes, edges)

    def getUserSocialGraph(self, user_id):
        nodes = list()
        edges = list()
        user = self.usersInfoDict[user_id]

        nodes.append({
            'id': int(user['user_id']), 
            'title': user['name'], 
            'image': user['profile_image_url'],
        });

        for match in self.getUserMatches(user_id):
            to_id = match['with']
            
            nodes.append({
                'id': int(to_id),
                'title': self.usersInfoDict[to_id]['name'],
                'image': self.usersInfoDict[to_id]['profile_image_url'],    
            })

            title = ', '.join(match['interests'][id] for id in match['interests'])

            edges.append({
                'from': int(user['user_id']),
                'to': int(to_id),
                'title': title,    
            })

        return (nodes, edges)    

# matcher = Matcher(1412174058)

# matcher.getUsersInfo()
# matcher.getUserInfoDict()
# matcher.doMatching()
# interests = matcher.getCommonInterests()
# print matcher.getUserMatches()
# result = matcher.getUserMatchesGraph()
# print len(result[0])
# print len(result[1])