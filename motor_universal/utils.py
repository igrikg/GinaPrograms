from typing import Callable


def repeat_decorator(repetition: int) -> Callable:
    def Inner(func):
        def wrapper(*args, **kwargs):
            result = False
            for _ in range(repetition):
                result = func(*args, **kwargs)
                if result: break
            return result

        return wrapper

    return Inner


if __name__ == '__main__':
    def func(a='asdasdasd'):
        print(a)
        return True


    print(repeat_decorator(12)(func)('Geeks'))
