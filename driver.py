import sys
import random
import pprint
import burrows_wheeler_transform

import suffix_array
import burrows_wheeler_transform

if __name__ == "__main__":
  which = sys.argv[1]
  gen_len = int(sys.argv[2])
  x = int(sys.argv[3])
  y = int(sys.argv[4])

  genome = [random.choice("ACTG") for i in range(gen_len)]
  genome.append("$")
  reads = []
  for i in range(x):
    j = random.randint(0, len(genome)-y-1)
    reads.append((genome[j:j+y], y))

  sa = suffix_array.make_suffix_array(genome)

  if which == "sa":
    flo = []
    for i in range(x):
      flo.append(suffix_array.pattern_matching_with_suffix_array(genome, reads[i][0], sa))
    
    for i in range(x):
      in_original = False
      for j in range(flo[i][0],flo[i][1]+1):
        if j == reads[i][1]:
          in_original = True
        if reads[i][0] != genome[sa[j]:sa[j]+len(reads[i][0])]:
          raise ValueError("Expected read:[{}] did not appear in text at location:[{}]".format(read[i][0], j))
  

  elif which == "bwt":
    (fo, bwt, count) = burrows_wheeler_transform.make_everyting(genome, sa)
    for i in range(x):
      n_matches = burrows_wheeler_transform.better_bw_matching(fo, bwt, reads[i][0], count)
      if n_matches < 1:
        raise ValueErro("No matches found")

  else:
    raise ValueError("Yo, use 'sa' or 'bwt' to specify the tpye of pattern matching you want")