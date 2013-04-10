
from bitbucket.bitbucket import Bitbucket
from bitbucket.issue import Issue



class BitBucketAdaptor(object):

    def __init__(self, username, password, repository_name):
        self.bitbucket = Bitbucket(username, password, repository_name)

    def from_status(self, status):
        if status == 'resolved':
            return 'complete'
        elif status == 'new':
            return 'pending'
        elif status == 'open':
            return 'in progress'
        # TODO: handle all returned values
        raise ValueError(status)

    def get_issues(self):
        # TODO: error handling and request failure handling etc
        offset = 0
        limit = 50
        to_ret = {}

        while True:
            issues = Issue(self.bitbucket).all(params={'start': offset, 'limit': limit})[1]['issues']
            if len(issues) == 0:
                break
            offset += limit
            for issue in issues:
                to_ret[int(issue['local_id'])] = {'title': issue['title'],
                                                  'status': self.from_status(issue['status'])}
        return to_ret

    def create_issue(self, title, status):
        if status == 'complete':
            status = 'resolved'
        elif status == 'pending':
            status = 'new'
        elif status == 'in progress':
            status = 'open'
        data = Issue(self.bitbucket).create(title=title, status=status)[1]
        return data['local_id']

    def update_issue(self, number, title, status):
        if status == 'complete':
            status = 'resolved'
        elif status == 'pending':
            status = 'new'
        elif status == 'in progress':
            status = 'open'
        Issue(self.bitbucket).update(number, title=title, status=status)

