import cachetools

# 创建一个 LRU 缓存
cache = None


def init(maxsize=50):
    global cache
    if cache is None:
        cache = cachetools.LRUCache(maxsize=maxsize)


if __name__ == '__main__':
    if cache is None:
        cache = cachetools.LRUCache(maxsize=10)
    cache['key1'] = 99
    cache['key2'] = True
    print('key3' in cache)
    print('key2' in cache)
    # print(cache['key3'])
    print(cache['key2'] == True)
