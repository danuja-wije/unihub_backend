import requests
def get_github_info(username):
    url = f'https://api.github.com/users/{username}'
    user_data = requests.get(url).json()
    followers_count = user_data['followers']

    url = f'https://api.github.com/users/{username}/followers'
    followers_data = requests.get(url).json()
    followers = [follower['login'] for follower in followers_data]

    url = f'https://api.github.com/users/{username}/repos'
    repos_data = requests.get(url).json()
    skills = {}
    for repo in repos_data:
        if 'language' in repo and repo['language'] is not None:
            if repo['language'] not in skills:
                skills[repo['language']] = 0
            skills[repo['language']] += repo['size']

    return skills, followers_count, followers


# username = "danuja-wije"
# skills, followers_count, followers = get_github_info(username)
# print(f'Skills: {skills}')
# print(f'Followers: {followers_count}')
# print(f'Followers usernames: {followers}')