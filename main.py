import arithmetic
import geometry as geo

print("Hello world")

a = int(input("Enter a:"))
b = int(input("Enter b:"))

arithmetic.add(a,b)
arithmetic.substract(a,b)

len = int(input("Enter length:"))
br = int(input("Enter breadth:"))

geo.calc_rect_area(len,br)
geo.calc_rect_peri(len,br)