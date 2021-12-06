-- https://futhark-lang.org/examples/histograms.html
let counter [n] (idxs: [n]i64): *[7]i64 =
  let counts = replicate 7 0
  in reduce_by_index counts (+) 0 idxs (replicate n 1)

-- Advance one step of the simulation.
-- Return any changes to "mutable" vars.
let step(counts: *[7]i64) (queue: *[2]i64) (time: i64): ([7]i64, [2]i64) =
  let spawn_t = time %% 7
  let qi = time %% 2
  let mature = queue[qi]
  let queue = queue with [qi] = counts[spawn_t]
  let counts = counts with [spawn_t] = counts[spawn_t] + mature
  in (counts, queue)

-- Run `times` steps of the simulation.
-- Return the total count of lanternfish.
let simulate(nums: []i64, times: i64) =
  let counts = counter nums
  let queue = [0, 0]
  let (counts, queue) = loop (counts, queue) for acc < times do
    step counts queue acc
  in (i64.sum counts) + (i64.sum queue)

entry part1(nums: []i64) = simulate(nums, 80)
entry part2(nums: []i64) = simulate(nums, 256)
