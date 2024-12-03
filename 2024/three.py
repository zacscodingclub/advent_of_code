from pprint import pprint
import re


class Multiply:
    def __init__(self, data):
        p = r"\d{1,3}"
        result = re.findall(p, data)
        self.x = int(result[0])
        self.y = int(result[1])

    def result(self):
        return self.x * self.y


def main():
    count = 0
    do_operation = True

    with open('three.input', 'r') as file:
        for i, line in enumerate(file):
            p = r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))"
            result = re.findall(p, line)       
            for r in result:
                if r == "don't()":
                    do_operation = False
                if r == "do()":
                    do_operation = True
                if do_operation and r.startswith("mul"):
                    mul = Multiply(r)
                    count += mul.result()

    print(count)


test = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    
main()