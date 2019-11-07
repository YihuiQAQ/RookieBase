"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime impoiimstsrt

"Utility functions for file and string manipulation"

import string


def lines_from_file(path):
    """Return a list of strings, one for each line in a file."""
    with open(path, 'r') as f:
        return [line.strip() for line in f.readlines()]


punctuation_remover = str.maketrans('', '', string.punctuation)


def remove_punctuation(s):
    """Return a string with the same contents as s, but with punctuation removed.

    >>> remove_punctuation("It's a lovely day, don't you think?")
    'Its a lovely day dont you think'
    """
    return s.strip().translate(punctuation_remover)


def lower(s):
    """Return a lowercased version of s."""
    return s.lower()


def split(s):
    """Return a list of words contained in s, which are sequences of characters
    separated by whitespace (spaces, tabs, etc.).

    >>> split("It's a lovely day, don't you think?")
    ["It's", 'a', 'lovely', 'day,', "don't", 'you', 'think?']
    """
    return s.split()


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    if k < 0:
        return ''
    else:
        b = 0
        c = []
        for i in paragraphs:
            if select(i):
                b = b + 1
                c.append(i)
        if b > k:
            return c[k]
        else:
            return ''
    # END PROBLEM 1

print(['Cute Dog!', 'That is a cat.', 'Nice pup!'], select, 2)

def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    topic = [x.lower() for x in topic]

    def select(i):
        i = split(remove_punctuation(lower(i)))
        for s in i:
            for c in topic:
                if c == s:
                    return True
        return False

    return select

    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    index = 0
    input_length = len(typed_words)
    if len(typed_words) > len(reference_words):
        for i in range(len(reference_words)):
            if typed_words[i] == reference_words[i]:
                index = index + 1
            else:
                index = index
    elif not typed_words:
        index = 0
        input_length = 1
    else:
        for i in range(len(typed_words)):
            if typed_words[i] == reference_words[i]:
                index = index + 1
            else:
                index = index
    return (index / input_length) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(typed) / 5) // (elapsed / 60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    ans = []
    for word in valid_words:
        diff = diff_function(user_word, word, limit)
        ans.append(diff)
    placeOften = ans.index(min(ans))
    Selected_Word = valid_words[placeOften]
    difference = diff_function(user_word, Selected_Word, limit)
    if user_word in valid_words:
        return user_word
    elif difference > limit:
        return user_word
    else:
        return Selected_Word
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def support(start, goal):
        if len(start) == 0:
            return len(goal)
        elif len(goal) == 0:
            return len(start)
        elif start[0] == goal[0]:
            return support(start[1:], goal[1:])
        else:
            return support(start[1:], goal[1:]) + 1
    if support(start, goal) <= limit:
        return support(start, goal)
    else:
        return limit + 1
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    # BEGIN PROBLEM 7
    """A diff function that computes the edit distance from START to GOAL."""
    if len(start) == 0 or len(goal) == 0:
        return max(len(start), len(goal))

    dp = [[0]*(len(goal) + 1) for _ in range(len(start) + 1)]
    dp[0][0] = 0

    for i in range(0, len(start) + 1):
        for j in range(0, len(goal) + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            else:
                cond1 = dp[i][j - 1] + 1
                cond2 = dp[i - 1][j] + 1
                cond3 = 0
                if start[i - 1] == goal[j - 1]:
                    cond3 = dp[i - 1][j - 1]
                else:
                    cond3 = dp[i - 1][j - 1] + 1
                dp[i][j] = min(cond1, cond2, cond3)
    if dp[-1][-1] > limit:
        return limit + 1
    else:
        return dp[-1][-1]


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    def check(typed, prompt):
        if len(typed) == 0:
            return 0
        elif len(prompt) == 0:
            return 0
        elif typed[0] == prompt[0]:
            return check(typed[1:], prompt[1:]) + 1
        else:
            return 0
    progress = check(typed, prompt)/len(prompt)

    dic = {id: progress}
    send(dic)

    return progress
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    totalWordlist = []
    for i in range(1, len(word_times[0])): #找到全部单词表
        ww = word(word_times[0][i])
        totalWordlist.append(ww)
    totalDeltatime = [] #totalDeltatime是输入单词的列表
    for i in range(len(word_times[0]) - 1):
        ttime = []
        for gamer in word_times:
            deltaT = elapsed_time(gamer[i+1]) - elapsed_time(gamer[i])
            ttime.append(deltaT) #算出时间差做一个列表
        totalDeltatime.append(ttime) #总时间差，totalDeltatime是时间差列表
    for i in word_times:
        i.clear()
    for i in range(len(totalDeltatime)):
        a = 0
        for tt in totalDeltatime[i]:
            if tt - min(totalDeltatime[i]) <= margin:
                word_times[a].append(totalWordlist[i])
            a = a + 1
    return word_times
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)