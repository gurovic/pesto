# shard_by is a list of (key function, pretty key, comparable key)

def shard(data, shard_by, indent=0, key=str):
    result = {}
    key_func, pretty_func, comparable, *nop = shard_by[0] + (int,)
    shard_by = shard_by[1:]
    sep = '\n' + '\t' * indent
    for i in data:
        key = key_func(i)
        result[key] = result.get(key, {})
        result[key][i] = data[i]
    if shard_by:
        for i in result:
            result[i] = shard(result[i], shard_by, indent+1, key)
    else:
        for i in result:
            try:
                sorted_data=sorted(result[i].values(), key=lambda x:key(x[0]))
            except Exception:
                sorted_data = sorted(result[i].values())
            result[i] = '\n' + '\n'.join(sorted_data)
            result[i] = result[i].replace('\n', (sep + '\t'))
    try:
        keys = sorted(result, key=comparable)
    except Exception:
        keys = sorted(result)
    ret = []
    for i in keys:
        ret.append(sep + pretty_func(i) + ':')
        ret.append(result[i])
    return (''.join(ret) if indent else ''.join(ret).lstrip())
