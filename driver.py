import sys
import random
import pprint
import time
import gc
from guppy import hpy


import suffix_array
import burrows_wheeler_transform
import resource

if __name__ == "__main__":
  which = sys.argv[1]
  gen_len = int(sys.argv[2])
  x = int(sys.argv[3])
  y = int(sys.argv[4])
  check = bool(sys.argv[5]=="True")

  h = hpy()

  setup_start = 0
  setup_end = 0
  match_start = 0
  match_end = 0
  base_memory = 0
  total_memory = 0

  genome = [random.choice("ACTG") for i in range(gen_len)]
  genome.append("$")
  reads = []
  for i in range(x):
    j = random.randint(0, len(genome)-y-1)
    reads.append((genome[j:j+y], y))

  base_memory = h.heap().size
  
  setup_start = time.perf_counter()
  sa = suffix_array.make_suffix_array(genome)

  if which == "sa":
    flo = []
    setup_end = time.perf_counter()
    gc.collect()
    match_start = time.perf_counter()
    for i in range(x):
      flo.append(suffix_array.pattern_matching_with_suffix_array(genome, reads[i][0], sa))
    match_end = time.perf_counter()
    total_memory = h.heap().size
    
    if check:
      for i in range(x):
        in_original = False
        for j in range(flo[i][0],flo[i][1]+1):
          if j == reads[i][1]:
            in_original = True
          if reads[i][0] != genome[sa[j]:sa[j]+len(reads[i][0])]:
            raise ValueError("Expected read:[{}] did not appear in text at location:[{}]".format(read[i][0], j))
  
  elif which == "bwt":
    n_matches = []
    (fo, bwt, count) = burrows_wheeler_transform.make_everything(genome, sa)
    setup_end = time.perf_counter()
    del genome
    del sa
    gc.collect()
    match_start = time.perf_counter()
    for i in range(x):
      n_matches.append(burrows_wheeler_transform.better_bw_matching(fo, bwt, reads[i][0], count))
    
    match_end = time.perf_counter()
    total_memory = h.heap().size
    
    if check:
      for i in range(x):
        if n_matches[i] < 1:
          raise ValueErro("No matches found")
  
  else:
    raise ValueError("Yo, use 'sa' or 'bwt' to specify the tpye of pattern matching you want")
  
  setup_time = setup_end - setup_start
  match_time = match_end - match_start
  print(which, gen_len, x, y, setup_time, match_time, base_memory, total_memory, sep=", ")

  