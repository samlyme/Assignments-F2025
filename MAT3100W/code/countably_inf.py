from typing import Callable, Iterator, TypeVar
from itertools import islice, tee

def N() -> Iterator[int]:
    i = 0 
    while True:
        yield i
        i += 1

def Z() -> Iterator[int]:
    n = N()
    yield next(n)
    for i in n:
        yield i
        yield -i

R = TypeVar("R")
S = TypeVar("S")
type Tree[T] = T | tuple[Tree[T], Tree[T]]
def forward_replay(g: Iterator[R]) -> Iterator[R]:
    seen = []
    for elem in g:
        seen.append(elem)
        yield from seen

def reverse_replay(g: Iterator[R]) -> Iterator[R]:
    seen = []
    for elem in g:
        seen.append(elem)
        yield from reversed(seen)
    
def compose(a: Iterator[R], b: Iterator[S]) -> Iterator[tuple[R, S]]:
    f = forward_replay(a)
    r = reverse_replay(b)
    yield from zip(f, r)

def set_pow(it: Callable[[], Iterator[R]], pow: int) -> Iterator[Tree[R]]:
    if pow < 1:
        raise Exception("Pow must be >=1")
    
    if pow == 1:
        return it()

    if pow % 2 == 0:
        
        return compose(*tee(set_pow(it, pow//2), 2))

    return compose(it(), set_pow(it, pow-1))

def NxN() -> Iterator:
    yield from set_pow(N, 2)

def ZxZ() -> Iterator:
    yield from set_pow(Z, 2)

def index(it: Iterator, index: int):
    return next(islice(it, index, None))

def flatten_tree(t: Tree[R]) -> R | tuple[R, ...]:
    if not isinstance(t, tuple):
        return t

    def leaves(node: Tree[R]) -> Iterator[R]:
        if isinstance(node, tuple):
            # node is a pair of subtrees
            left, right = node
            yield from leaves(left)
            yield from leaves(right)
        else:
            # node is a leaf
            yield node

    return tuple(leaves(t))


# for i, x in enumerate(set_pow(N, 3)):
#     print(i, flatten_tree(x))

p = 5
it = set_pow(N, p)
m = 100
for i in range(m+1):
    x = next(it)
    print(x, flatten_tree(x))