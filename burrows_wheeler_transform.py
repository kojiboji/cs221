import pprint
import random

import suffix_array

def make_everything(text, suffix_array):
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

def make_everything_efficient(text, suffix_array, k, c):
  (fo, bwt, count) = make_everything(text, suffix_array)
  checkpoint = {symbol: arr[0::c] for symbol,arr in count.items()}
  partial_sa = {i:suffix for i,suffix in enumerate(suffix_array) if suffix % k ==0}
  return (fo,bwt,partial_sa, checkpoint)

def better_bw_matching(fo, bwt, clone, count):
  pattern = [i for i in clone]
  top = 0
  bottom = len(bwt) - 1
  while top <= bottom:
    if pattern:
      symbol = pattern[-1]
      pattern.pop()
      top = fo[symbol] + count[symbol][top]
      bottom = fo[symbol] + count[symbol][bottom+1] - 1
    else:
      return bottom - top + 1
  return 0

def efficient_bw_matching(fo, bwt, clone, partial_sa, k, checkpoint, c):
  pattern = [i for i in clone]
  top = 0
  bottom = len(bwt) - 1
  while top <= bottom:
    if pattern:
      symbol = pattern[-1]
      pattern.pop()
      top = fo[symbol] + getCount(symbol, top, checkpoint, c, bwt)
      bottom = fo[symbol] + getCount(symbol, bottom+1, checkpoint, c, bwt) - 1
    else:
      positions = []
      for i in range(top,bottom+1):
        offset = 0
        while(True):
          if i in partial_sa.keys():
            positions.append(partial_sa[i] + offset)
            break
          else:
            symbol = bwt[i] 
            offset += 1
            occurence = getCount(symbol, i+1,checkpoint, c, bwt)
            i = fo[symbol] + occurence - 1
      
      return positions
  return None

def getCount(symbol, place, checkpoint, c, bwt):
  last_checkpoint = int(place/c)
  count = checkpoint[symbol][last_checkpoint]

  for i in range(last_checkpoint*c, place):
    if bwt[i] == symbol:
      count += 1
  return count

# def alignemnt_bw_matching(fo, bwt, pattern, count):

if __name__ ==  "__main__":
  genome = [random.choice("ACTG") for i in range(10)]
  genome.append("$")
  sa = suffix_array.make_suffix_array(genome)
  (fo,bwt,partial_sa, checkpoint) = make_everything_efficient(genome, sa, 2, 2)
  pprint.pprint(genome)
  pprint.pprint(fo)
  pprint.pprint(bwt)
  pprint.pprint(sa)
  pprint.pprint(partial_sa)
  pprint.pprint(checkpoint)
