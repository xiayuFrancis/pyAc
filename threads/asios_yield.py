def jumping_range(N):
    index = 0
    while index < N:
        jump = yield index
        if jump is None:
            jump = 1
        index += jump


if __name__ == "__main__":
    itr = jumping_range(5)
    print(next(itr))
    print(itr.send(2))
    print(next(itr))
    print(itr.send(-1))
