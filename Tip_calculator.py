
try:
    def tip_calculator(total,tip,split):
        assert type(total) == float
        assert type(split) == int
        assert type(tip) == float

        updated_total = total / split

        tipped_total = updated_total * (tip /100)

        updated_total = updated_total + tipped_total
        return f"{split} have to pay {float(updated_total)} each and tip has to be {float(tipped_total)}"
except AssertionError:
    print("assertion failed")

t = float(input("Enter total amount to pay: "))
tp = float(input("Enter percentage of tip to pay: "))
s = int(input("Enter number of people to split the bill with: "))

print(tip_calculator(t,tp,s))