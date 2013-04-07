#!/usr/bin/env python
import re

from bitbucket.bitbucket import Bitbucket
from bitbucket.issue import Issue

TICKET_RE = re.compile('^(.*) \((\d+)\)$')

STATUS = {
  '+': 'complete',
  '-': 'in progress',
  ' ': 'pending',
}


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
        issues = Issue(self.bitbucket).all()[1]['issues']
        to_ret = {}
        for issue in issues:
            to_ret[issue['local_id']] = {'title': issue['title'],
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


class GitHubAdaptor(object):
    # TODO: this!
    pass


def parse_issues(lines):
    for line in lines:
        yield(parse_issue(line))


def parse_issue(line):
    """
    Expected format:
  
     | + this is the subject of the issue (512)
     |   this issue is not completed (560)
     |   this issue has no issue number yet
    """
    status = STATUS[line[0]]

    remainder = line[2:]
  
    match = TICKET_RE.match(remainder)

    if match:
        subject = match.group(1)
        ticket_number = int(match.group(2))
    else:
      subject = remainder.strip()
      ticket_number = None

    return status, subject, ticket_number


def symbol_for(status):
    for symbol, name in STATUS.iteritems():
        if name == status:
            return symbol
    raise ValueError(status)


def sync(*args):
    # for now, use positional arguments (argparse etc to come later)
    # ./sync.py /path/to/file repo username password host
    # ./sync.py /home/carl/ticket-todo-tickets ticket-todo carlio myawesomepassword github
    # TODO: argparse
    # TODO: better error handling
    filepath, repo, username, password, host = args[1:]
    if host == 'bitbucket':
        Adaptor = BitBucketAdaptor
    elif host == 'github':
        Adaptor = GitHubAdaptor

    api = Adaptor(username, password, repo)

    remote_issues = api.get_issues()

    with open(filepath) as f:
        file_content = f.readlines()

    new_file_content = []

    for status, title, number in parse_issues(file_content):
        if number is None:
            # locally, we think this is new
            # first, check the title in case it somehow ended up on remote
            for remote_number, remote_data in remote_issues.iteritems():
                if remote_data['title'] == title:
                    # we found this remotely!
                    new_line = '%s %s (%s)' % (symbol_for(remote_data['status']), title, remote_number)
                    new_file_content.append(new_line)
                    break
            else:
                # this wasn't found remotely... so create it!
                number = api.create_issue(title, status)
                new_line = '%s %s (%s)' % (symbol_for(status), title, number)
        else:
            # we already know about this, check it is also remote
            # TODO: sync titles?
            # TODO: what if the remote issue is missing?
            remote_status = remote_issues[number]['status']
            new_line = '%s %s (%s)' % (symbol_for(remote_status), title, number)

        new_file_content.append(new_line)

    with open(filepath, 'w') as f:
        for line in new_file_content:
            f.write(line)
            f.write('\n')


if __name__ == '__main__':
    import sys
    sync(*sys.argv)
