import re
from difflib import *
from pprint import pprint

dividers = ['.', ':', '-', ';']
connectives = ['and']

divider_words = {
    'point': '.',
    'dot': '.'
}

multipliers = {
    'weeks': 26880,
    'days': 38400,
    'hours': 3600,
    'minutes': 60,
    'seconds': 1,
    'milliseconds': .01
}

abbreviations = {
    'ms': 'milliseconds',
    's': 'seconds',
    'sec': 'seconds',
    'm': 'minutes',
    'min': 'minutes',
    'h': 'hours',
    'hr': 'hours',
    'd': 'days',
    'w': 'weeks'
}

prefixes = {
    '.': 'milliseconds'
}

# Minimum time acceptable per 50m
min_time_50 = 20

# Maximum time acceptable per 50m
max_time_50 = 120


class EntryTime:

    def __init__(self):
        self.distance = 0
        self.time_text = ""
        self.tokenlist = []

    def set_distance(self, distance):
        self.distance = distance

    def set_time(self, time_text):
        self.time_text = time_text

    def parse(self):

        g = self.initial_tokenise()

        tokenlist = []
        idx = 0

        # Pass 1

        for t in g:

            # Identify numeric tokens
            if re.match(r'(\d)', t):

                numeral = t

                # Check for a decimal separator prefix
                decimal_prefix = '.'

                fraction = False
                if idx > 0:
                    if g[idx - 1] == decimal_prefix:
                        fraction = True

                if (len(g) - 1) >= (idx + 1):

                    if re.match(r'(\w+)', g[idx + 1]):
                        multiplier_options = self.multiplier_ident(g[idx + 1])
                    else:
                        multiplier_options = []
                else:
                    multiplier_options = []

                self.tokenlist.append({
                    'numeral': numeral,
                    'multiplier_options': multiplier_options,
                    'fractional': fraction
                })


    def initial_tokenise(self):

        # Tokenise the time and filter meaningless whitespace
        g = re.split(r'(\d+|\W+)', self.time_text)
        g = list(filter(None, g))
        g = [i for i in g if " " not in i]

        return g

    def multiplier_ident(self, target):

        candidates = []

        for key, value in abbreviations.items():

            s = SequenceMatcher(None, key, target)
            ratio = s.ratio()

            candidates.append({
                'multiplier_name': value,
                'ratio': ratio
            })

        for key, values in multipliers.items():

            s = SequenceMatcher(None, key, target)
            ratio = s.ratio()

            candidates.append({
                'multiplier_name': value,
                'ratio': ratio
            })

        candidates.sort(key=lambda x:x['ratio'], reverse=True)

        return candidates
