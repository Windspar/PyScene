class ArrayProperty:
    def __init__(self, position):
        self.position = position

    def __get__(self, instance, owner):
        return instance[self.position]

    def __set__(self, instance, value):
        instance[self.position] = value

class ArrayDoubleProperty:
    def __init__(self, position1, position2, return_type=None):
        self.position1 = position1
        self.position2 = position2
        self.return_type = return_type

    def __get__(self, instance, owner):
        if self.return_type:
            return self.return_type(instance[self.position1], instance[self.position2])
        return instance[self.position1], instance[self.position2]

    def __set__(self, instance, value):
        instance[self.position1] = value[0]
        instance[self.position2] = value[1]

class ArrayCombineProperty:
    def __init__(self, position, combine):
        self.position = position
        self.combine = combine

    def __get__(self, instance, owner):
        return instance[self.position] + instance[self.combine]

    def __set__(self, instance, value):
        instance[self.position] = value - instance[self.combine]

class ArrayCombineCenterProperty:
    def __init__(self, position, combine):
        self.position = position
        self.combine = combine

    def __get__(self, instance, owner):
        return instance[self.position] + instance[self.combine] * 0.5

    def __set__(self, instance, value):
        instance[self.position] = value - instance[self.combine] * 0.5

class ArrayTypeDoubleProperty:
    def __init__(self, array1, array2, return_type=None):
        self.array1 = array1
        self.array2 = array2
        self.return_type = return_type

    def __get__(self, instance, owner):
        if self.return_type:
            return self.return_type(self.array1.__get__(instance, owner), self.array2.__get__(instance, owner))
        return self.array1.__get__(instance, owner), self.array2.__get__(instance, owner)

    def __set__(self, instance, value):
        self.array1.__set__(instance, value[0])
        self.array2.__set__(instance, value[1])
