import os
from github import Github

token = os.getenv("GITHUB_TOKEN")
g=Github(token)

def get_repos(username):
    user=g.get_user(username)
    repos=user.get_repos()
    repo_list=[]
    for repo in repos:
        repo_list.append({
            "name":repo.name,
            "description":repo.description,
            "stars":repo.stargazers_count,
            "forks":repo.forks_count,
            "watchers":repo.watchers_count,
            "language":repo.language,
            "size":repo.size
        })
    return repo_list
for repo in repositories:
    repo_path = f"C:/Users/harsh/Desktop/github_repos/{repo['name']}"
    files = filter_files(repo_path)

username="hk2317"
repositories=get_repos(username)
print(repositories)    

priority_file_types=['.py','.js','.cpp']
def filter_files(repo_path):
    files_to_analyze=[]
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in priority_file_types):
                files_to_analyze.append(os.path.join(root, file))
    return files_to_analyze

import subprocess

def analyze_file(file_path):
    pylint_output=subprocess.run(['pylint',file_path],capture_output=True, text=True)
    radon_output=subprocess.run(['radon','cc',file_path],capture_output=True, text=True)

    return pylint_output.stdout,radon_output.stdout

def calculate_score(repo,pylint_score,complexity_score):
    score=repo['stars']*0.4+repo['forks']*0.3+(100-pylint_score)*0.2+complexity_score*0.1
    return score

import pandas as pd

def generate_report(repo_data):
    df=pd.DataFrame(repo_data)
    df=df.sort_values(by='score',ascending=False)
    df.to_csv('github_repo_analyses.csv',index=False)
    print(df)
