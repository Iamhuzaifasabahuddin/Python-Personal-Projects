import random
import copy


class Hat:
    def __init__(self, **balls):
        self.contents = []
        for color, count in balls.items():
            self.contents.extend([color] * count)

    def draw(self, num_balls):
        if num_balls >= len(self.contents):
            return self.contents
        drawn_balls = random.sample(self.contents, num_balls)
        for ball in drawn_balls:
            self.contents.remove(ball)
        return drawn_balls


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    num_success = 0

    for _ in range(num_experiments):
        hat_copy = copy.deepcopy(hat)
        drawn_balls = hat_copy.draw(num_balls_drawn)
        print(drawn_balls)

        success = True
        for color, count in expected_balls.items():
            if drawn_balls.count(color) < count:
                success = False
                break
        if success:
            num_success += 1

    probability = num_success / num_experiments
    return probability


hat = Hat(blue=5, red=4, green=2)
expected_balls = {"red": 1, "green": 2}
num_balls_drawn = 4
num_experiments = 2
probability = experiment(hat, expected_balls, num_balls_drawn, num_experiments)
print(f"Probability: {probability:.4f}")
