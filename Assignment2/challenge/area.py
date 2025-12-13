import math_utils

l = float(input("Enter length of rectangle: "))
b = float(input("Enter breadth of rectangle: "))
print("Rectangle area:", math_utils.rect_area(l, b))

s = float(input("Enter side of square: "))
print("Square area:", math_utils.sqr_area(s))

r = float(input("Enter radius of circle: "))
print("Circle area:", math_utils.circ_area(r))
