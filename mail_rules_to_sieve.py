import plistlib
from urlparse import urlparse
import codecs
import sys 
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

prefix = '' # INBOX
myAccount = '<my_account_path>'

p = plistlib.readPlist('SyncedRules.plist')
activestate = plistlib.readPlist('RulesActiveState.plist')

print '''
require ["fileinto", "reject", "body", "mailbox"];
'''
def handleAnyRecipient(matchType, match, expression):
    print 'address %s %s  "%s"' % (matchType, match, expression),
    
def handle(matchType, header, expression):
    if header in ('To', 'Cc', 'From'):
        print 'address %s ["%s"]  "%s"' % (matchType, header, expression),
    elif header == 'Subject':
        print 'header %s "Subject" "%s"' % (matchType, expression),
    elif header == 'List-Id':
        print 'header %s "List-Id" "%s"' % (matchType, expression),
    elif header == 'X-LSV-ListID':
        print 'header %s "X-LSV-ListID" "%s"' % (matchType, expression),
    elif header == 'Mailing-List':
        print 'header %s "Mailing-List" "%s"' % (matchType, expression),
    elif header == 'List-Help':
        print 'header %s "List-Help" "%s"' % (matchType, expression),
    elif header == 'List-Unsubscribe':
        print 'header %s "List-Unsubscribe" "%s"' % (matchType, expression),
    elif header == 'Sender':
        print 'header %s "Sender" "%s"' % (matchType, expression),
    elif header == 'Approved-By':
        print 'header %s "Approved-By" "%s"' % (matchType, expression),
    elif header == 'Delivered-To':
        print 'header %s "Delivered-To" "%s"' % (matchType, expression),
    elif header == 'Return-Path':
        print 'header %s "Return-Path" "%s"' % (matchType, expression),
    elif header == 'Message-Id':
        print 'header %s "Message-Id" "%s"' % (matchType, expression),
    elif header == 'X-Quarantine-Id':
        print 'header %s "X-Quarantine-Id" "%s"' % (matchType, expression),
    elif header == 'Received':
        print 'header %s "Received" "%s"' % (matchType, expression),
    elif header == 'Body':
        print 'body :text %s "%s"' % (matchType, expression),
    elif header == 'Account':
        pass
    else:
        raise ValueError(header)

def bool_is_true(b):
    #print '# b is ' + str(b) + ' and ' + str((b in ['YES', 'true', 'True', '1', True]))
    if b is None:
        return False
    return (b in ['YES', 'true', 'True', '1', True])

# like imap://alexr@localhost/LLVM/llvm-lab-wg
def imap_mbox_path(u):
    o = urlparse(u)
    return o.path.strip('/')

stmt = 'if'
for rule in p:
    if 'Mailbox' not in rule: continue
    mbox = rule['Mailbox'].split('/')[-1].split('.')[0]
    mbox_path = prefix + imap_mbox_path(rule['CopyToMailboxURL'])

    keep = ' keep;' if bool_is_true(rule.get('ShouldCopyMessage')) else ''
    stop = ' stop;' if bool_is_true(rule.get('StopEvaluatingRules')) else ''
    action = '{ fileinto :create "%s";%s%s }' % (mbox_path, keep, stop)
    
#    print '#', rule['RuleName'], '->', mbox
    isActive = True
    #if not bool_is_true(rule.get('Active', '0')):
    #    isActive = False
    #print '# Rule %s is %s' % (rule['RuleId'], activestate[rule['RuleId']])
    if not bool_is_true(activestate[rule['RuleId']]):
        isActive = False
    if (not isActive): print '# ',
    print stmt,
    stmt = 'elsif'
    
    isAll = (bool_is_true(rule['AllCriteriaMustBeSatisfied']))
    if isAll:
        print 'allof (',
    else:
        print 'anyof (',
    
    firstCriteria = True
    for criteria in rule['Criteria']:
        header = criteria['Header']
        expression = criteria.get('Expression')
        matchType = ':matches'

        qual = criteria.get('Qualifier')
        if qual == 'BeginsWith':
            expression = expression + '*'
        elif qual == 'EndsWith':
            expression = '*' + expression
        elif qual == 'IsEqualTo':
            matchType = ':is'
        else:
            matchType = ':contains'
            
        # do we have an AllCriteria where one is a match for the account we're processing?
        if (isAll and (criteria['Header'] == 'Account') and (expression == myAccount)):
            isAll = 0
            continue
            
        if (not firstCriteria): print ', '
        if (not firstCriteria) and (not isActive): print '# ',
        firstCriteria = False
        if header == 'AnyRecipient':
            handleAnyRecipient(matchType, '[\"To\", \"CC\"]', expression)
        elif header == 'IsJunkMail':
            print "# IsJunkMail for %s" % (mbox_path)
        else:
            if 'Expression' in criteria:
                handle(matchType, header, expression)
            else:
                print '# header ', header, ' unhandled'
    print ') ' + action
    
print '''
else {
     keep;
}
'''
