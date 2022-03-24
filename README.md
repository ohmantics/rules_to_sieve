# rules_to_sieve

A quick script I whipped up some time ago to help convert Apple's Mail.app built-in rules system over to [sieve](https://en.wikipedia.org/wiki/Sieve_\(mail_filtering_language\)) rules.

In recent versions of macOS, you'll need to finagle your way into the ~/Library/Mail folder to run this script since it needs to look at SyncedRules.plist and RulesActiveState.plist from there.
