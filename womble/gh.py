
import os
from github3 import GitHub


class GitHubAdaptor(object):

    def __init__(self, owner, repository, token=None):
        self.token = token or os.environ.get('WOMBLE_TOKEN')
        self.github = GitHub(token=self.token)
        self.repo = self.github.repository(owner, repository)

    def get_issues(self):
        to_ret = {}

        issues = list(self.repo.iter_issues(state='closed'))
        issues += list(self.repo.iter_issues(state='open'))

        for issue in issues:
            cur_labels = [l.name for l in issue.labels]
            if issue.state == 'closed':
                if 'wontfix' in cur_labels:
                    status = 'wontfix'
                else:
                    status = 'complete'
            else:
                if 'in progress' in cur_labels:
                    status = 'in progress'
                else:
                    status = 'pending'

            to_ret[issue.number] = {
                'title': issue.title,
                'status': status
            }

        return to_ret

    def create_issue(self, title, status):
        if status == 'complete':
            labels = []
            state = 'closed'
        elif status == 'pending':
            labels = []
            state = 'open'
        elif status == 'in progress':
            labels = ['in progress']
            state = 'open'
        elif status == 'wontfix':
            labels = ['wontfix']
            state = 'closed'

        issue = self.repo.create_issue(
            title,
            labels=labels
        )
        if state == 'closed':
            self.update_issue(issue.number, title, status)
        return issue.number

    def update_issue(self, number, title, status):
        issue = self.repo.issue(number)

        if status == 'complete':
            issue.edit(title, state='closed', labels=[])
        elif status == 'pending':
            issue.edit(title, state='open', labels=[])
        elif status == 'in progress':
            issue.edit(title, state='open', labels=['in progress'])
        elif status == 'wontfix':
            issue.edit(title, state='closed', labels=['wontfix'])
