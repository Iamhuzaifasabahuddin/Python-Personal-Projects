class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height

    def get_area(self):
        area = self.height * self.width
        return area

    def get_perimeter(self):
        perimeter = (2 * self.width) + (2 * self.height)
        return perimeter

    def get_diagonal(self):
        diagonal = (self.width ** 2 + self.height ** 2) ** 0.5
        return diagonal

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture."

        picture = '*' * self.width + '\n'
        picture *= self.height
        return picture

    def get_amount_inside(self, shape):
        width_fit = self.width // shape.width
        height_fit = self.height // shape.height
        return width_fit * height_fit

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


class Square(Rectangle):
    def __init__(self, side):
        Rectangle.__init__(self, side, side)
        self.side = side

    def set_side(self, new_side):
        self.side = new_side
        self.width = new_side
        self.height = new_side

    def set_width(self, new_side):
        self.set_side(new_side)

    def set_height(self, new_side):
        self.set_side(new_side)

    def get_picture(self):
        if self.side > 50:
            return "Too big for picture."

        picture = '*' * self.side + '\n'
        picture *= self.side
        return picture

    def __str__(self):
        return f"Square(side={self.side})"


if __name__ == '__main__':
    rect = Rectangle(10, 5)
    print(rect.get_picture())

    sq = Square(4)
    print(sq.get_area())
