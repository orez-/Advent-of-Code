#!/usr/bin/awk -f
{ nr[NR] = $0 }
nr[NR - 3] < $0 { total = total + 1 }
END { print total - 3 }
