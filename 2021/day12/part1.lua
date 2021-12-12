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

function walk(paths, position, seen)
    if position == "end" then
        return 1
    end
    if isSmallCave(position) and seen[position] then
        return 0
    end
    seen[position] = true
    local total = 0
    for i, next in ipairs(paths[position]) do
        total = total + walk(paths, next, seen)
    end
    seen[position] = nil
    return total
end

local paths = readPaths()
result = walk(paths, "start", {})
print(result)
