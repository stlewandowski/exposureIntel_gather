import configparser
import os
import subprocess

import datetime


class GithubDMCA:
    """ Class to pull DMCA information from Github, update, get new data, and format it """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf.ini')
        repo_dir = config['GithubDMCA']['directory']
        self.github_repo = "https://github.com/github/dmca.git"
        os.chdir(repo_dir)
        # check if repository exists on machine, if not clone, if exists, git pull
        self.repo_path = os.path.join(repo_dir, 'dmca')
        if not os.path.isdir(self.repo_path):
            print("Cloning...")
            subprocess.run(["git", "clone", self.github_repo], check=True)

    def update_repo(self):
        """ Update DMCA repository with 'git pull' """
        os.chdir(self.repo_path)
        x = subprocess.run(["git", "pull"], check=True, capture_output=True, encoding="utf8")
        print("Git Pull result:")
        print(x.stdout)

    def gen_commit_log(self):
        """ Generate a Git Commit Log file from the latest commit to the last one checked """

    def search_commit_log(self):
        """ Pull out new files from commit log file
        """
""" So far it looks like each file is a takedown notice
    2020-09-01-<company_name>.md
    And within this file there are links to the offending github content
    Among other information.
"""


if __name__ == "__main__":
    x = GithubDMCA()

    x.update_repo()
