#!/usr/bin/awk -f
BEGIN { lastLine = 9999 }
$0 > lastLine { total = total + 1 }
{ lastLine = $0 }
END { print total }
