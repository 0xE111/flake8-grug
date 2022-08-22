def early_quit(x: int) -> int:
    print('ok')
    if x == 1:
        print('ok')
    # elif x == 2:
    #     print('ok')
    else:
        print('oops')
        raise ValueError()
