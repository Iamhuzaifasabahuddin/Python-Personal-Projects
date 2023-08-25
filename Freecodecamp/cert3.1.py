class Category:
    def __init__(self, category):
        self.category = category
        self.balance = 0
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.category}")
            category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.balance

    def __str__(self):
        category_title = f"{self.category:*^30}\n"
        items = ""
        for item in self.ledger:
            description = item["description"][:23]
            amount = format(item["amount"], ".2f")
            items += f"{description:<23}{amount:>7}\n"
        total = format(self.balance, ".2f")
        return category_title + items + f"Total: {total}"


def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    spendings = []
    total_spent = 0

    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spendings.append(spent)
        total_spent += spent

    percentages = [(spending / total_spent) * 100 for spending in spendings]

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for percent in percentages:
            if percent >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    -" + "---" * len(categories) + "\n"

    max_len = max(len(category.category) for category in categories)
    for i in range(max_len):
        chart += "     "
        for category in categories:
            if i < len(category.category):
                chart += category.category[i] + "  "
            else:
                chart += "   "
        if i < max_len - 1:
            chart += "\n"

    return chart


food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")

food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
print(food)
entertainment.deposit(1000, "initial deposit")
entertainment.withdraw(15, "cinema")
entertainment.withdraw(50, "concert")
print(entertainment.get_balance())
print(entertainment)

business.deposit(1000, "initial deposit")
business.withdraw(50, "bought office supplies")
business.withdraw(100, "office rent")
business.deposit(500, "client payment")
print(business.get_balance())
print(business)

print(create_spend_chart([business, food, entertainment]))
