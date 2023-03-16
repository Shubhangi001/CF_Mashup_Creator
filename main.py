
def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)
# print(link(''))
import requests
print("Enter the ratings of the problems you want to add to the mashup separated by a space")
ratings = input().split()
for i in range(len(ratings)):
    ratings[i] = int(ratings[i])
solved_problems = set()
problems_list = []
print("Enter the users' profile handles separated by a space")
handles = input().split()
n = len(handles)
def get_problems(handles, ratings):
    problems_list = []
    for i in range(len(handles)):
        response = requests.get('https://codeforces.com/api/user.status?handle=' + handles[i])
        result = response.json()['result']
        # print(result)
        for j in range(len(result)):
            try:
                if result[j]['verdict'] == 'OK' and result[j]['problem']['rating'] in ratings:
                    x = frozenset({result[j]['problem']['contestId'],result[j]['problem']['index']})
                    solved_problems.add(x)
            except:
                pass
        # print("Solved problems: ",solved_problems)
    # x = frozenset({139,'A'})
    # print(x in solved_problems)
    response = requests.get('https://codeforces.com/api/problemset.problems')
    result = response.json()['result']['problems']
    print(result)
    # for i in range(len(ratings)):
    #     print(ratings[i],": ",end=" ")
    #     cnt = 0
    #     for j in range(len(result)):
    #         try:
    #             if(result[j]['rating'] != ratings[i]):
    #                 continue
    #             contestid = result[j]['contestId']
    #             index = result[j]['index']

    #             x = frozenset({contestid,index})
    #             print(x)
    #             if x not in solved_problems and x not in problems_list:
    #                 problems_list.append('https://codeforces.com/problemset/problem/' + str(contestid) + '/' + str(index))
    #                 print(link('https://codeforces.com/problemset/problem/' + str(contestid) + '/' + str(index), str(contestid) + str(index)),end=" ")
    #                 # print(result[j]['contestId'],result[j]['index'],"  ",end="")
    #                 cnt += 1
    #                 if cnt == 3:
    #                     print()
    #                     break
    #         except:
    #             pass
    return problems_list
problems_list = get_problems(handles, ratings)
