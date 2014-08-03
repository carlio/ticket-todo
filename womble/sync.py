from .parse import parse_issues, symbol_for
from .bb import BitBucketAdaptor
from .gh import GitHubAdaptor


def sync(*args):
    # for now, use positional arguments (argparse etc to come later)
    # TODO: argparse
    # TODO: better error handling
    filepath, host, username, repo = args[1:]
    if host == 'bitbucket':
        Adaptor = BitBucketAdaptor
    elif host == 'github':
        Adaptor = GitHubAdaptor
    else:
        raise ValueError(host)

    api = Adaptor(username, repo)

    remote_issues = api.get_issues()

    with open(filepath) as f:
        file_content = f.readlines()

    new_file_content = []

    for is_issue, line in parse_issues(file_content):
        if not is_issue:
            new_file_content.append(line)
            continue

        status, title, number = line

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
            issue = remote_issues[number]

            # if the status has changed, update remote
            if issue['status'] != status or issue['title'] != title:
                print '%s -> %s  ::  %s -> %s' % (issue['status'], status, issue['title'], title)
                api.update_issue(number, title, status)

            new_line = '%s %s (%s)' % (symbol_for(status), title, number)

        new_file_content.append(new_line)

    with open(filepath, 'w') as f:
        for line in new_file_content:
            f.write(line)
            f.write('\n')


if __name__ == '__main__':
    import sys
    sync(*sys.argv)
