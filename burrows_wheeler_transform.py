import suffix_array
import pprint

def make_everyting(text, suffix_array):
  bwt = [text[suffix_array[i] - 1] for i in range(len(text))]
  fc = [i for i in text]
  fc.sort()
  fo = {}
  last_symbol = None
  for i, symbol in enumerate(fc):
    if symbol != last_symbol:
      fo[symbol] = i
      last_symbol = symbol

  count = {key:[0] for key in fo.keys()}
  for i, symbol in enumerate(bwt):
     count[symbol].append(count[symbol][i]+1)
     for other in count.keys():
       if other != symbol:
         count[other].append(count[other][i])

  return (fo, bwt, count)

def better_bw_matching(fo, bwt, pattern, count):
  top = 0
  bottom = len(bwt) - 1
  while top <= bottom:
    if pattern:
      symbol = pattern[-1]
      pattern = pattern[:-1]
      top = fo[symbol] + count[symbol][top]
      bottom = fo[symbol] + count[symbol][bottom+1] -1
    else:
      return bottom - top + 1
  return 0

# def alignemnt_bw_matching(fo, bwt, pattern, count):

