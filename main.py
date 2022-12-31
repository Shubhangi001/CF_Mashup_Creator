import requests
print("Enter the number of users in mashup")
n = int(input())
print("Enter the users' handles")
handles = []
for i in range(n):
    handles.append(input())
print("Enter the number of problems")
m = int(input())
ratings = []
for i in range(m):
    print("Enter the rating of the problem")
    rating = int(input())
    ratings.append(rating)
solved_problems = set()
def get_problems(handles, ratings):
    problems_list = []
    for i in range(len(handles)):
        response = requests.get('https://codeforces.com/api/user.status?handle=' + handles[i])
        result = response.json()['result']
        for j in range(len(result)):
            try:
                if result[j]['verdict'] == 'OK' and result[j]['problem']['rating'] in ratings:
                    x = frozenset({result[j]['problem']['contestId'],result[j]['problem']['index']})
                    solved_problems.add(x)
            except:
                pass
    for i in range(len(ratings)):
        print(ratings[i],": ",end=" ")
        response = requests.get('https://codeforces.com/api/problemset.problems')
        result = response.json()['result']['problems']
        # print(result)
        cnt = 0
        for j in range(len(result)):
            try:
                if(result[j]['rating'] != ratings[i]):
                    continue
                contestid = result[j]['contestId']
                index = result[j]['index']
                x = frozenset({contestid,index})
                if x not in solved_problems and x not in problems_list:
                    problems_list.append('https://codeforces.com/problemset/problem/' + str(contestid) + '/' + str(index))
                    print(result[j]['contestId'],result[j]['index'],"  ",end="")
                    cnt += 1
                    if cnt == 5:
                        print()
                        break
            except:
                pass
    return problems_list
problems =  get_problems(handles, ratings)
