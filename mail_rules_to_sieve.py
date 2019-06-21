import plistlib

p = plistlib.readPlist('MessageRules.plist')

print '''
require ["fileinto", "reject"];
'''
stmt = 'if'
def handle(header, expression, mbox):
    global stmt
    if header in ('To', 'Cc', 'From'):
        print stmt, 'address :contains ["%s"]  "%s" { fileinto "INBOX.%s"; }' % (header, expression, mbox)
    elif header == 'Subject':
        print stmt, 'header :matches "Subject" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'List-Id':
        print stmt, 'header :matches "List-Id" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'X-LSV-ListID':
        print stmt, 'header :matches "X-LSV-ListID" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Mailing-List':
        print stmt, 'header :matches "Mailing-List" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'List-Help':
        print stmt, 'header :matches "List-Help" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'List-Unsubscribe':
        print stmt, 'header :matches "List-Unsubscribe" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Sender':
        print stmt, 'header :matches "Sender" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Approved-By':
        print stmt, 'header :matches "Approved-By" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Delivered-To':
        print stmt, 'header :matches "Delivered-To" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Return-Path':
        print stmt, 'header :matches "Return-Path" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Message-Id':
        print stmt, 'header :matches "Message-Id" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'X-Quarantine-Id':
        print stmt, 'header :matches "X-Quarantine-Id" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Received':
        print stmt, 'header :matches "Received" ["*%s*"] { fileinto "INBOX.%s"; }' % (expression, mbox)
    elif header == 'Account':
        print "# Account is %s and %s" % (expression, mbox)
    else:
        raise ValueError(header)
    stmt = 'elsif'

for rule in p['rules']:
    if 'Mailbox' not in rule: continue
    mbox = rule['Mailbox'].split('/')[-1].split('.')[0]
    print '#', rule['RuleName'], '->', mbox
    if rule['Active'] != 1:
        print '# ',
    for criteria in rule['Criteria']:
        if criteria['Header'] == 'AnyRecipient':
            handle('To', criteria['Expression'], mbox)
            handle('Cc', criteria['Expression'], mbox)
        elif criteria['Header'] == 'IsJunkMail':
            print "# IsJunkMail for %s" % (mbox)
        else:
            handle(criteria['Header'], criteria['Expression'], mbox)

print '''
else {
     keep;
}
'''
