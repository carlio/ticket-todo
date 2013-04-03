import re

TICKET_RE = re.compile('^(.*) \((\d+)\)$')

STATUS = {
  '+': 'complete',
  '-': 'in progress',
  ' ': 'pending',
}

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
    subject = remainder
    ticket_number = None

  return status, subject, ticket_number
