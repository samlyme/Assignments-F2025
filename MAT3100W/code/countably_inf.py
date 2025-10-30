from typing import Callable, Iterator, TypeVar
from itertools import islice

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

def NxN() -> Iterator:
    yield from compose(N(), N())

def ZxZ() -> Iterator:
    yield from compose(Z(), Z())

def N_pow(pow: int) -> Iterator:
    if pow < 1:
        raise Exception("Pow must be >=1")
    
    if pow == 1:
        return N()

    if pow % 2 == 0:
        return compose(N_pow(pow//2), N_pow(pow//2))

    return compose(N(), N_pow(pow-1))

type Tree[T] = T | tuple[Tree[T], Tree[T]]
def set_pow(it: Callable[[], Iterator[R]], pow: int) -> Iterator[Tree[R]]:
    if pow < 1:
        raise Exception("Pow must be >=1")
    
    if pow == 1:
        return it()

    if pow % 2 == 0:
        return compose(set_pow(it, pow//2), set_pow(it, pow//2))

    return compose(it(), set_pow(it, pow-1))
    

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



p = 5
it = set_pow(N, p)
m = 100
for i in range(m+1):
    x = next(it)
    print(x, flatten_tree(x))