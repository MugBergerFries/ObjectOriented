class Shape:  # Top class, represents all shapes
    type = 'undefined'

    def __init__(self, order):  # Order represents the order in which the object should be 'displayed' (1 is first, etc)
        self.order = order

    def identify(self):
        return "I am a {} in position {}".format(self.type, self.order)


class Triangle(Shape):  # (Shape) means it inherits from Shape
    type = 'triangle'
    pass


class Circle(Shape):
    type = 'circle'
    pass


class Square(Shape):
    type = 'square'
    pass


def order(data):  # Orders the database by 'order'
    data.sort(key=lambda x: x.order)
    pass


database = [Triangle(2), Square(1), Circle(3), Square(4)]
order(database)
for shape in database:
    print(shape.identify())
