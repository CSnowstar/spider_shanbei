

flat = lambda ls: sum(
        map(
            flat, ls
        ),
        []
    ) if isinstance(ls, list) else [ls]


flat2 = lambda ls: sum(
        map(
            flat, ls
        ),
        []
    ) if isinstance(ls, list) else [ls]


def flat3(node):
    return sum(map(flat3, node), []) if isinstance(node, list) else [node]

def flat4(node):
    if isinstance(node, list):
        lsSubNode = map(flat3, node)
        res = []
        for x in lsSubNode:
            res += x
        return res
    else:
        return [node]


def start():
    x = [2, 22]
    y = [1, 56, 4, x]
    z = [3, x, y]
    print z
    print flat(z)
    print flat2(z)
    print flat3(z)
    print flat4(z)


if __name__ == "__main__":
    start()
