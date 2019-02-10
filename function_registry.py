from random import randint

class FunctionRegistry:
    registry = dict()
    
    @staticmethod
    def _get_new_name(f):
        while "name in registry":
            name = "{f_name}_{discrim}".format(
                f_name = f.__name__,
                discrim = randint(1000, 9999)
            )

            if not name in FunctionRegistry.registry:
                break

        return name
    
    @staticmethod
    def register(f):
        ident = FunctionRegistry._get_new_name(f)
        FunctionRegistry.registry[ident] = f
        return ident

    @staticmethod
    def get_ident(f):
        for k, v in FunctionRegistry.registry.items():
            if f == v:
                return k

        return None

    @staticmethod
    def invoke(ident, *args):
        f = FunctionRegistry.get(ident)
        return f(*args)

    @staticmethod
    def get(ident, default = None):
        return FunctionRegistry.registry.get(ident, default)

if __name__ == '__main__':
    def plus(x, y):
        return x + y

    def times(x, y):
        return x * y

    class Test:
        def __init__(self, s):
            self.str = s

        def register(self):
            ident = FunctionRegistry.register(self.hello)
            return ident

        def hello(self, test):
            return test

    ident_plus_1 = FunctionRegistry.register(plus)
    ident_plus_2 = FunctionRegistry.register(plus)
    ident_times = FunctionRegistry.register(times)

    inst = Test("whatever")
    ident_method = inst.register()

    x = 3
    y = 4
    
    assert FunctionRegistry.invoke(ident_plus_1, x, y) == plus(x, y)
    assert FunctionRegistry.invoke(ident_plus_2, x, y) == plus(x, y)
    assert FunctionRegistry.invoke(ident_times, x, y) == times(x, y)
    assert FunctionRegistry.get_ident(plus) in (ident_plus_1, ident_plus_2)
    assert FunctionRegistry.invoke(ident_method, "test_string") == "test_string"
    assert ident_plus_1 != ident_plus_2
    print("Tests OK")