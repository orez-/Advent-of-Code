nums = System.in.newReader().readLine().split(",").collect { it as int }
nums.sort()
total = nums.size()
answer = (0..total / 2).stream()
    .mapToInt({ nums[total - 1 - it] - nums[it] })
println answer.sum()
