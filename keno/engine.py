import random

payouts = {
       1 : {
           1 : 2
        },
       2 : {
           2 : 9,
           1 : 1
        },
       3 : {
           3 : 47,
           2 : 2
        },
       4 : {
           4 : 91,
           3 : 5,
           2 : 1
        },
       5 : {
           5 : 820,
           4 : 12,
           3 : 3
        },
       6 : {
           6 : 1600,
           5 : 70,
           4 : 4,
           3 : 3
        },
       7 : {
           7 : 7000,
           6 : 400,
           5 : 21,
           4 : 2,
           3 : 1
        },
       8 : {
           8 : 10000,
           7 : 1650,
           6 : 100,
           5 : 12,
           4 : 2
        },
       9 : {
           9 : 10000,
           8 : 4700,
           7 : 335,
           6 : 44,
           5 : 6,
           4 : 1
        },
       10 : {
           10 : 10000,
           9 : 4500,
           8 : 1000,
           7 : 142,
           6 : 24,
           5 : 5,
           0 : 3
        }
    }

def get_random_list(size, numbers=(1,80)):
    '''
    Returns a list of unique random numbers between range in numbers

    :param size: int size of list you want
    :param_range: tuple of the range the numbers should be picked from.
    :return: list
    '''

    # Not the most efficient way to do this, but I feel like this best simulates a lotto drawing
    pool = list(range(numbers[0], numbers[1] + 1))
    results = []
    for _ in range(size):
        ball = pool.pop(random.randint(0,len(pool)-1))
        results.append(ball)
    return results

def get_payout(num_selections, num_matches, bet=1):
    '''
    Gives you the amount of money payed out based on number of selections and number of matches
    Will also multiply by an optional bet amount

    :param num_selections: int number of selections made
    :param num_matches: int number of matches
    :param bet: int amount bet
    :return: int payout based on json file
    '''

    try:
        payout = payouts[num_selections][num_matches]
    except KeyError:
        payout = 0
    return payout * bet

def get_payout_list(num_selections):
    '''
    Get full payout list for a certain number of selections

    :param num_selections: int Number of selections
    :return: dict
    '''

    if num_selections == 0:
        return {}
    retval = payouts[num_selections]
    return retval

def get_hits(selections, picks):
    '''
    basically just returns the items in both lists

    :param selections: list of int values indicating the user selection
    :param picks: list of int values indicating that was picked
    :return:
    '''
    return [pick for pick in picks if pick in selections]