
import os
from github3 import GitHub


class GitHubAdaptor(object):

    def __init__(self, owner, repository, token=None):
        self.token = token or os.environ.get('WOMBLE_TOKEN')
        self.github = GitHub(token=token)
        self.repo = self.github.repository(owner, repository)

    def from_labels(self, status):
        if status == 'resolved':
            return 'complete'
        elif status == 'new':
            return 'pending'
        elif status == 'open':
            return 'in progress'
        elif status == 'abandoned':
            return 'wont fix'
            # TODO: handle all returned values
        raise ValueError(status)

    def get_issues(self):
        to_ret = {}

        for issue in self.repo.iter_issues(state='all'):
            if issue.state == 'closed':
                if 'wontfix' in issue.labels:
                    status = 'wont fix'
                else:
                    status = 'complete'
            else:
                if 'inprogress' in issue.labels:
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
        elif status == 'wont fix':
            labels = ['wontfix']
            state = 'closed'

        issue = self.repo.create_issue(
            title,
            labels = labels
        )
        if state == 'closed':
            issue.close()
        return issue.number

    def update_issue(self, number, title, status):
        issue = self.repo.issue(number)

        if status == 'complete':
            issue.edit(title, state='closed', labels=[])
        elif status == 'pending':
            issue.edit(title, state='open', labels=[])
        elif status == 'in progress':
            issue.edit(title, state='open', labels=['in progress'])
        elif status == 'wont fix':
            issue.edit(title, state='closed', labels=['wontfix'])
