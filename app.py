import json
import math
import uuid
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import bson.json_util as json_util
import skill_extractor as SK
import skill_scraper as SC
import random
import teamFormation as TF

app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://admin:admin@unihub.2jsvdwq.mongodb.net/?retryWrites=true&w=majority')
db = client['unihub_mongo_db']
CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def auth():
    if request.method == 'POST':
        body = request.json
        print(body)
        email = body['email']
        password = body['password']
        if db['Users'].find_one({'_id': email, 'password': password}):
            print("auth success")
            d = db['Users'].find_one({'_id': email, 'password': password})
            d["status"] = "Success"
            return jsonify(d)
        else:
            return jsonify({"status": "failed"})


def all_skill_finder():
    d = list(db['Users'].find({}, {'git': 1}))
    all_skill = {}
    print("all user names :", d)
    for i in d:
        if 'git' in i.keys():
            userName = i['git'].split('/')[-1]
            print(userName)
            s, fc, f = SC.get_github_info(userName)
            for k, v in s.items():
                if k in all_skill.keys():
                    all_skill[k] += v
                else:
                    all_skill[k] = v
    print(all_skill)

    return all_skill

@app.route('/Project',methods=['POST','GET'])
def createProject():
    if request.method == 'POST':
        body = request.json
        print(body)
        topic = body['title']
        project = body['project']
        company = body['company']
        creator = body['creator']
        skills = body['skills']
        print("type of skills is ",type(skills))
        logo = body['logo']
        uu = uuid.uuid4()
        db['Projects'].insert_one({
            "_id": str(uu),
            "project": project['path'],
            "topic": str(topic),
            "company": company,
            "creator": creator,
            "skills": skills,
            "logo":logo
        })
        p = {
            "Status": "Success",
        }
        return jsonify(p)

@app.route('/admin/allSkills',methods=['GET'])
def getallskills():
    if request.method == 'GET':
        d = list(db['Users'].find({},{'git':1}))
        all_skill ={}
        print("all user names :",d)
        for i in d:
            if 'git' in i.keys():
                userName = i['git'].split('/')[-1]
                print(userName)
                s,fc,f = SC.get_github_info(userName)
                for k,v in s.items():
                    if k in all_skill.keys():
                        all_skill[k] += v
                    else:
                        all_skill[k] = v
        print(all_skill)

        return jsonify(d)
@app.route('/Company/project/<id>',methods=['GET'])
def getProjectById(id):
    if request.method == "GET":
        d = db["Projects"].find_one({'_id':id})
        return jsonify(d)
@app.route('/Company',methods=['POST'])
def createcompany():
    if request.method == 'POST':
        body = request.json
        name = body['name']
        location = body['location']
        logo = body['logo']
        about = body['about']

        db['Companies'].insert_one({
            "name":name,
            "location":location,
            "logo":logo['path'],
            about :about
        })
        p = {
            "Status":"Success"
        }
        return jsonify(p)

@app.route('/UserProject',methods=['POST'])
def createUserProject():
    if request.method == "POST":
        body = request.json
        userId = body['userId']
        projectId = body['projectId']
        team = body['team']
        status = 'pending'
        logo = body['logo']
        title = body['title']
        db['UserProject'].insert_one({
            '_id':projectId,
            'userId':userId,
            'topic':title,
            'logo':logo,
            'team':team,
            'status':status
        })
        return jsonify({
            'Status':"Success"
        })
@app.route('/Project/company/all',methods=['POST'])
def getallcompanyprojects():
    if request.method == 'POST':
        body = request.json
        print(body)
        type = body['type']
        userId = body['userId']
        if type == "selected":
            name = body['companyName']
            d = db['Projects'].find({'company':name})
            return jsonify([todo for todo in d])
        elif type == "all":
            d = db['Projects'].find()
            return jsonify([todo for todo in d])
        elif type == 'pending':
            d = list(db['UserProject'].find({'userId':userId,'status':'pending'}))
            return jsonify([todo for todo in d])

@app.route('/Project/<path>', methods=['GET'])
def getSkills(path):
    if request.method == 'GET':
        # print(body)
        p ={
            "Status":"Success",
            "Data":SK.exctractor(path)
        }
        return jsonify(p)


@app.route('/Users/<id>', methods=['GET'])
def getUserbyid(id):
    if request.method == 'GET':
        d = db['Users'].find_one({'_id': id})
        return jsonify(d)
    else:
        return "error"

@app.route('/Posts',methods=['GET'])
def getallposts():
    posts = db['Posts'].find({})
    p = []
    for post in posts:
        print(post)
        p.append(post)
    return jsonify(p)


def getAllCommunities():
    leader, experts, team, communities = TF.Formate()

@app.route('/Project/teamformation/<projectId>',methods=["GET"])
def teamFormation(projectId):
    leader,experts,team,communities = TF.Formate()
    roles = team.keys()
    members = {}
    for r in roles:
        t_mem = team[r]
        for i in t_mem:
            if i == leader:
                members[i]="Leader"
            elif i in experts:
                members[i] = "Co-Leader"
            else:
                members[i] = str(r) + " specialist"

    p = {
        "members":members
    }
    return jsonify(p)
@app.route('/<userId>/post',methods=['GET','POST'])
def getpostbyuser(userId):
    if request.method == 'GET':
        posts = db['Posts'].find({'owner':userId})
        p = []
        for post in posts:
            print(post)
            p.append(post)
        return jsonify(p)
    elif request.method == 'POST':
        uu = uuid.uuid4()
        body = request.json
        owner = userId
        title = body['title']
        img_path = body['picture']
        content = body['content']

        db['Posts'].insert_one({
            "_id":str(uu),
            "owner" : owner,
            "title":title,
            "img_path":img_path['path'],
            "content":content
        })
        posts = db['Posts'].find({})
        p = []
        for post in posts:
            print(post)
            p.append(post)
        return jsonify(p)
@app.route('/Users', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        body = request.json
        # print(body)
        fName = body['firstName']
        lName = body['lastName']
        emailId = body['email']
        userType = body['userType']

        if userType == "Student":
            password = body['password']
            gitHubLink = body['githubLink']
            img_path = body['picture']
            university = body['university']
            git_name = gitHubLink.split('/')[-1]
            skills,friend_count,git_friends = SC.get_github_info(git_name)
            print("skills : ",skills)
            all_skills = all_skill_finder()
            print(all_skills)
            scores = {}
            for k,v in skills.items():
                if k in all_skills.keys():
                    temp = (v / all_skills[k]) * 5
                    scores[k]=math.ceil(temp)
                else:
                    scores[k] = 5
            single_domain = "https://github.com/"
            friends = {}
            for f in git_friends:
                git = single_domain+f
                if db['Users'].find_one({'git':git}):
                    ran = random.uniform(0,1)
                    u = db['Users'].find_one({'git':git})['_id']
                    friends[u] = ran
            print(friends)
            db['Users'].insert_one({
                "fName": fName,
                "lName": lName,
                "_id": emailId,
                "skills":scores,
                "friends":friends,
                "userType": userType,
                "password": password,
                "git": gitHubLink,
                "img_path": img_path['path'],
                "university":university
            })
            return jsonify({
                'status': 'Data is posted to mongo Db',
                "fName": fName,
                "lName": lName,
                "_id": emailId,
                "userType": userType,
                "password": password,
                "git": gitHubLink,
                "img_path": img_path['path'],
                "university":university
            })
        else:
            password = body['password']
            img_path = body['picture']
            companyName = body['companyName']
            db['Users'].insert_one({
                "fName": fName,
                "lName": lName,
                "_id": emailId,
                "userType": userType,
                "password": password,
                "img_path": img_path['path'],
                "companyName" : companyName
            })
            return jsonify({
                'status': 'Data is posted to mongo Db',
                "fName": fName,
                "lName": lName,
                "_id": emailId,
                "userType": userType,
                "password": password,
                "img_path": img_path['path'],
                "companyName" : companyName
            })


if __name__ == '__main__':
    app.run(debug=True)
