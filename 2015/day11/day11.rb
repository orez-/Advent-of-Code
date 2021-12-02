pw = "hepxxyzz"

while 1
    pw = pw.succ
    next unless pw.bytes.to_a.each_cons(3).any? {|a,b,c| a.ord + 1 == b.ord and b.ord + 1 == c.ord}
    next if /[iol]/ =~ pw
    next unless /(.)\1.*(.)\2/ =~ pw
    puts pw
    break
end
