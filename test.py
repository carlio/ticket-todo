from sync_issues import parse_issue


def test_issue_parsing():
    print parse_issue("+ this is a test issue (512)")
    print parse_issue("- this is a test issue also (513)")
    print parse_issue("  and this")

if __name__ == '__main__':
    test_issue_parsing()
