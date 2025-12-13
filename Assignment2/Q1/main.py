from math_utils import rect_area, sqr_area, circ_area

len = float(input("Enter length:"))
br = float(input("Enter breadth:"))
a1 = rect_area(len,br)
print("rectangle area : ",a1)

s = float(input("Enter side:"))
a2 = sqr_area(s)
print("square area : ",a2)

r = float(input("Enter radius:"))
a3 = circ_area(r)
print("circle area : ",a3)
