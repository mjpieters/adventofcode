from collections import namedtuple
from functools import reduce
from itertools import product
from operator import mul


Ingredient = namedtuple(
    'Ingredient', 'capacity durability flavor texture calories')


def read_ingredients(fileobj):
    results = {}
    for line in fileobj:
        name, __, properties = line.strip().partition(': ')
        properties = {name: int(val)
                      for prop in properties.split(',')
                      for name, val in (prop.split(),)}
        results[name] = Ingredient(**properties)
    return results


def optimise_for_score(ingredients, target_calories=None):
    max_score = 0
    for combo in product(range(100), repeat=len(ingredients) - 1):
        if sum(combo) > 100:
            continue
        combo += ((100 - sum(combo)),)
        if target_calories is not None:
            calories = sum(ingr.calories * factor
                           for factor, ingr in zip(
                               combo, ingredients.values()))
            if calories != target_calories:
                continue
        scores = [sum(ingr[p] * factor
                      for factor, ingr in zip(combo, ingredients.values()))
                  for p in range(4)]
        if any(s <= 0 for s in scores):
            continue
        score = reduce(mul, scores)
        if score > max_score:
            max_score = score
    return max_score


if __name__ == '__main__':
    import sys

    filename = sys.argv[-1]
    with open(filename) as ingrf:
        ingr = read_ingredients(ingrf)
    score = optimise_for_score(ingr)
    print('Part 1:', score)
    score = optimise_for_score(ingr, 500)
    print('Part 2:', score)
