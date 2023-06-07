from typing import Callable


def repeat_decorator(repetition: int, compare_func: Callable, compare: str, strint: str) -> Callable:
    '''

    :param strint:
    :param compare_func:
    :param repetition: number of repetition
    :param compare: repite until func compare
    :return:
    '''

    def inner(func):
        def wrapper(*args, **kwargs):
            result = False
            for _ in range(repetition):
                result = compare_func(compare, func(*args, **kwargs), strint)
                if result: break
            return result

        return wrapper

    return inner


def check_is_equil_and_correct(purpose, result, strint='POSSS') -> bool:
    split=purpose.split(strint)
    print('==============================================')
    if len(split) == 2:
        length = tuple(map(len, split))
        if result[:length[0]] == split[0] and result[-length[1]:] == split[1]:
            try:
                int(result[length[0]:-length[1]])

            except ValueError:
                return False
    else:
        return purpose == result


if __name__ == '__main__':
    def func(a='asdasdasd'):
        print(a)
        return a


    # print(repeat_decorator(12,'Geek')(func)('Geeks'))
    check_is_equil_and_correct("#0185POSSS32460.43\n", "#018512532460.43\n", strint='POSSS')
    check_is_equil_and_correct("#0185POSSS32460.43\n", "#018512t532460.43\n", strint='POSSS')
    check_is_equil_and_correct("#0185POSSS32460.43\n", "#018532460.43\n", strint='POSSS')
    check_is_equil_and_correct("#0185POSSS\n", "#018532460.43\n", strint='POSSS')

    check_is_equil_and_correct("#018532460.43\n", "#018532460.43\n", strint='POSSS')
    check_is_equil_and_correct("#018532460.43\n", "#01853260.43\n", strint='POSSS')

    # check_is_equil_and_correct(purpose, result, strint='POS')
