from typing import Callable


def repeat_decorator(repetition: int, compare: str) -> Callable:
    '''

    :param repetition: number of repetition
    :param compare: repite until func result!=compare
    :return:
    '''
    def Inner(func):
        def wrapper(*args, **kwargs):
            result = False
            for _ in range(repetition):
                result = (compare == func(*args, **kwargs))
                if result: break
            return result
        return wrapper

    return Inner



if __name__ == '__main__':
    def func(a='asdasdasd'):
        print(a)
        return a


    print(repeat_decorator(12,'Geek')(func)('Geeks'))
