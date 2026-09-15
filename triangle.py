import math
def classify_triangle(a,b,c):
    if a + b <= c or a + c <= b or b + c <= a:
     return "not triangle"
    if a == b == c:
        return "равнобедренный"
