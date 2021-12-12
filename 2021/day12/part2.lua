function readPaths()
    local paths = {}
    local line = io.read()
    while line do
        local a, b = string.match(line, "(%w+)-(%w+)")
        paths[a] = paths[a] or {}
        paths[a][#paths[a] + 1] = b
        paths[b] = paths[b] or {}
        paths[b][#paths[b] + 1] = a
        line = io.read()
    end
    return paths
end

function isSmallCave(name)
    return string.match(name, "%l")
end

function walk(paths, position, seen, doubled)
    local x2 = doubled
    if position == "end" then
        return 1
    end
    local seenAmt = seen[position] or 0
    if isSmallCave(position) and seenAmt > 0 then
        if x2 or position == "start" then
            return 0
        end
        x2 = true
    end
    seen[position] = seenAmt + 1
    local total = 0
    for i, next in ipairs(paths[position]) do
        total = total + walk(paths, next, seen, x2)
    end
    seen[position] = seenAmt
    return total
end

local paths = readPaths()
result = walk(paths, "start", {}, false)
print(result)
