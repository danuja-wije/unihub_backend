import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd

skills = ["Python", "Java", "C++", "Javascript", "SQL"]
students = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Judy", "Karl", "Lily", "Mike", "Nancy", "Oscar", "Peggy", "Quinn", "Ralph"]

G = nx.Graph()
G.add_nodes_from(skills, bipartite=0)
G.add_nodes_from(students, bipartite=1)


skill_levels = {
        "Alice":{ "Python": 5, "Java": 4, "C++": 3, "Javascript": 2, "SQL": 1},
        "Bob":{ "Python": 4, "Java": 3, "C++": 2, "Javascript": 1, "SQL": 5},
        "Charlie":{ "Python": 3, "Java": 2, "C++": 1, "Javascript": 5, "SQL": 4},
        "David":{"Python": 2, "Java": 1},
        "Eve":{"Python": 1, "Java": 5, "C++": 4, "Javascript": 3},
        "Frank":{"Python": 5, "C++": 4, "SQL": 3},
        "Grace":{"Java": 5, "Javascript": 4},
        "Hannah":{"SQL": 5},
        "Ivan":{"C++": 5},
        "Judy":{"Javascript": 5},
        "Karl":{ "Java": 5, "C++": 4, "Javascript": 3, "SQL": 2},
        "Lily":{ "Java": 4, "C++": 3, "Javascript": 2, "SQL": 1},
        "Mike":{ "SQL": 4, "Javascript": 3, "C++": 2, "Java": 1},
        "Nancy":{ "C++": 5, "Java": 4, "SQL": 3},
        "Oscar":{"Python": 5,"SQL": 4},
        "Peggy":{"Javascript": 5, "SQL": 4},
        "Quinn":{"Java": 5, "C++": 4},
        "Ralph":{"Python": 5, "Java": 4, "C++": 3, "Javascript": 2, "SQL": 1},
 }

collaboration_potential = {}

for student,skills in skill_levels.items():
        # print(student)
        for skill,point in skills.items():
                # print(skill,point)
                if student not in collaboration_potential:
                        collaboration_potential[student] = {}
                        if skill not in collaboration_potential[student]:
                                collaboration_potential[student][skill] = 10 - point
                else:
                        if skill not in collaboration_potential[student]:
                                collaboration_potential[student][skill] = 10 - point

for student,skills in collaboration_potential.items():
        for skill,point in skills.items():
                G.add_edge(student, skill,capacity=float(point),weight=(skill_levels[student][skill])/10)

G.add_edge("Alice", "Bob",weights= 0.1)
G.add_edge("Alice", "Charlie",weights= 0.5)
G.add_edge("Alice", "David",weights= 0.3)
G.add_edge("Alice", "Eve",weights= 0.4)
G.add_edge("Alice", "Frank",weights= 0.9)
G.add_edge("Alice", "Ralph",weights= 0.4)
G.add_edge("Lily", "Karl",weights=0.7)
G.add_edge("Lily", "Grace",weights= 0.2)
G.add_edge("Judy", "Mike",weights= 0.8)
G.add_edge("Judy", "Hannah",weights= 0.6)
G.add_edge("Judy", "Peggy",weights= 0.3)
G.add_edge("Judy", "Oscar",weights= 0.6)
G.add_edge("Judy", "Ivan",weights= 0.8)
G.add_edge("Judy", "Quinn",weights= 0.5)


project_complexity = {}

project_complexity["Python"] = 2
project_complexity["Javascript"] = 2
project_complexity["SQL"] = 2
project_complexity["C++"] = 5
team_size = 10

team = {}
team_experts = []
under_avg_students = []

domain_students = []

for language in project_complexity.keys():
    neighbors = [n for n in G.neighbors(language) if  n not in domain_students]
    print(language," : ",neighbors)
    weight_list = []
    for node in G.edges(data=True):
        if node[0] == language:
            for i in neighbors:
                if i == node[1]:
                    weight_list.append(node[2]['weight'])

    avg_weight = sum(weight_list) / len(neighbors)
    print('weight list : ',weight_list)
    print('avg weight : ',avg_weight)

    temp_flow = {}
    for neighbor in neighbors:
        # print(neighbor," : ",G[node][neighbor]['weight'])
        flow_value = nx.maximum_flow(G, language,neighbor , capacity='capacity')[1][language][neighbor]
        # print("flow value = ",flow_value)
        # print("expected complexity = ",project_complexity[node])
        # print("collected skill = ",skill_levels[neighbor])

        temp_flow[neighbor] = flow_value
    print("team flow",temp_flow)
    
    # sG = G.subgraph(neighbors)
    # nx.draw(sG,pos, with_labels=True)

    under = [n for n in neighbors if G[language][n]['weight'] < avg_weight]
    print("Under avg : ",under)
    
    for i in under:
        del temp_flow[i]
    print("New temp_flow : ",temp_flow)
    domain_students = []
    
    conn = True
    sum_project_complexity = 0
    while conn:
        print("came to while loop")
        print("domain_students : ",domain_students)
        if len(domain_students) > 0:
            # print("domain students : ",[temp_flow[domain_student] for domain_student in domain_students])
            for domain_student in domain_students:
                if domain_student in temp_flow_keys:
                    if len(temp_flow) > 1 and (domain_student in temp_flow.keys()):
                        del temp_flow[domain_student]
                        print("del : ",domain_student)
        temp_flow_keys = list(temp_flow.keys())
        temp_flow_values = list(temp_flow.values())
            
        print("temp_flow_keys : ",temp_flow_keys)
        print("temp_flow_values : ",temp_flow_values)

        max_flow = max(temp_flow_values)
        print("max-flow : ",max_flow)
        max_persons = [i for i in temp_flow_keys if temp_flow[i] == max(temp_flow_values)]
        print("max-person : ",max_persons)

            # if len(temp_flow) > 1:
            #     if G[node][temp_flow[max_flow]]['weight'] > avg_weight:
            #         print("student : ",temp_flow[max(temp_flow_keys)])
            #         break
            #     else:
            #         # print("remove : ",temp_flow[max_flow]," : ",max_flow," : ",G[node][temp_flow[max_flow]]['weight']," : ",avg_weight)
            #         del temp_flow[max_flow]
        # print("max-flow : ",temp_flow)
        # print("student : ",temp_flow[max(temp_flow.keys())])

        if len(domain_students) > 0:
            for domain_student in domain_students:
                sum_project_complexity += skill_levels[domain_student][language]
        else:
            sum_project_complexity = 0

        if len(max_persons) > 1:
            sum_persons = 0
            for max_person in max_persons:
                if max_person not in domain_students:
                    domain_students.append(max_person)
                    sum_persons += skill_levels[max_person][language]
            sum_project_complexity += sum_persons
        else:
            # print(max_persons[0])
            sum_project_complexity += skill_levels[max_persons[0]][language]
            domain_students.append(max_persons[0])


        print("sum_project_complexity : ",sum_project_complexity)
        print("requested complexity : ",project_complexity[language])
        if sum_project_complexity < project_complexity[language]:
            conn = True
        else:
            conn = False

    team[language] = domain_students

print(team)

alltogether_team = []
for k,v in team.items():
    alltogether_team += v

close_centrality = nx.closeness_centrality(G)


closeness_df = pd.DataFrame.from_dict(close_centrality, orient='index', columns=['closeness'])
closeness_df.drop(skills, inplace=True)
closeness_df.sort_values(by=['closeness'], ascending=False,inplace=True)

messure = {}
for name in alltogether_team:
    l = closeness_df.index == name
    for i in range(len(l)):
        if l[i]:
            messure[name] = closeness_df.iloc[i,0]

val = list(messure.values())
val.sort(reverse=True)

team_experts = [k for k,v in messure.items() if v in val[:3]]

print("Team experts : ",team_experts)