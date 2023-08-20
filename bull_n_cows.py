# First steps:
# Implementation of the game itself - guess the number, make a guess, check the rules, end game.

import numpy as np
import pickle
import random
import time
import tqdm
import yaml

from typing import List, Dict

def load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

def load_digits(config):
    with open(config["digits_filepath"], "rb")as f:
        digits = pickle.load(f)
        digits = [list(it) for it in digits]
    return digits

def generate_magic_number(config) -> List[int]:
    """
    Basic rules are applied:
     - all digits are different
     - digit '0' can be on any place

     :return: magic number
    """

    magic_number = np.random.choice(range(10), size=config["num_of_digits"], replace=False)

    return magic_number

def make_guess_naive(digits: List[List[int]], guess: List[int], answer: Dict[int, int], config):
    """
    Naive strategy - random guess

    :param digits: set of numbers to search magic_number
    :param guess: guessed number
    :param answer: answer for the guessed number
    :param config: config file

    :return: new set of possible numbers, new guess
    """
    
    digits.remove(guess)

    possible_numbers = [number for number in digits if compare_numbers(guess, number, config) == answer]
    random_guess = random.choice(possible_numbers)

    return possible_numbers, random_guess

def compare_numbers(magic_number: List[int], guess_number: List[int], config) -> Dict[int, int]:
    """
    Count the number of Bulls and Cows.
    Cows are accociated with 0's, Bulls with 1's.
    """
    num_of_bulls = 0
    num_of_cows = 0

    for idx in range(config["num_of_digits"]):
        if guess_number[idx] == magic_number[idx]:
            num_of_bulls += 1
        elif guess_number[idx] in magic_number:
            num_of_cows += 1
    
    answer = {
        0: num_of_cows,
        1: num_of_bulls
    }

    return answer

config = load_config()
digits = load_digits(config)
logger = {
    "average_time": 0,
    "time": 0,
    "average_num_of_guesses": 0,
}

for _ in tqdm.tqdm(range(config["num_of_trials"])):
    start_time = time.time()

    mn = generate_magic_number(config)
    guess = random.choice(digits)
    ans = compare_numbers(mn, guess, config)

    num_of_guesses = 1
    digits_copy = digits[:]

    while(ans[1] != 4):
        digits_copy, guess = make_guess_naive(digits_copy, guess, ans, config)
        ans = compare_numbers(mn, guess, config)
        num_of_guesses +=1

    end_time = time.time()
    logger["average_num_of_guesses"] += num_of_guesses
    logger["time"] += end_time - start_time

logger["average_num_of_guesses"] = logger["average_num_of_guesses"] / config["num_of_trials"]
logger["average_time"] = logger["time"] / config["num_of_trials"]

print(f"num = {round(logger['average_num_of_guesses'], 4)}, "
      f"time per round = {round(logger['average_time'], 4)}, "
      f"total time = {round(logger['time'], 4)}")
