import re

TICKET_RE = re.compile('^(.*) \((\d+)\)$')

STATUS = {
  '+': 'complete',
  '-': 'in progress',
  ' ': 'pending',
  '!': 'wontfix',
}


def parse_issues(lines):
    for line in lines:
        if line.strip() == '' or line.startswith(';'):
            yield(False, line.strip())
            continue
        yield(True, parse_issue(line))


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
