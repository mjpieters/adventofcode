from itertools import accumulate


def calc_moves(l):
    """
    To move x items up one floor takes 2 * (x - 1) - 1 moves.

    So all we have to do is move those items up one floor, then calculate
    the number of moves needed to move those up together with what is already
    on that floor, etc.

    Input is a list of item counts per floor

    """
    return sum(2 * (c - 1) - 1 for c in accumulate(l))


if __name__ == '__main__':
    # only the item count per floor matters. We don't care what's up on the top
    # floor either, that's already on the top floor.
    star1_input = [4, 2, 4]
    print('Star 1:', calc_moves(star1_input))
    star2_input = [8, 2, 4]
    print('Star 2:', calc_moves(star2_input))
