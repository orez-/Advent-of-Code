int distance(n) { (n * (n + 1) / 2) as int }
int score(pivot, nums) {
    nums.stream().mapToInt({ distance((it - pivot).abs()) }).sum()
}

List<Integer> nums = System.in.newReader().readLine().split(",").collect { it as int }
answer = (nums.min()..nums.max()).stream().collect({ score(it, nums) }).min()
println answer
