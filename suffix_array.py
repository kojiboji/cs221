import random
import string

def suffix_array(text):
  arr = [ord(i) for i in text]
  return recursive_suffix_array(arr)

def recursive_suffix_array(arr):
  if(len(arr) == 1):
    return [0]
  elif(len(arr) == 2):
    if arr[0] < arr[1]:
      return [0, 1]
    else:
      return [1,0]
  arr = arr + [0]

  #find triplets for mod23
  triplets_pos = [(arr[i:i+3], i) for i in range(len(arr)) if i % 3 != 0]

  #sort the triplets
  triplets_pos.sort()

  #and figure out their ranks
  pos_to_rank = {}
  rank = 0
  prev_value = -1
  for i in range(len(triplets_pos)):
    if triplets_pos[i][0] != prev_value:
      rank += 1
    prev_value = triplets_pos[i][0]
    pos_to_rank[triplets_pos[i][1]] = rank
  
  #produce the new sa12prime string made up of ranks
  fuck = [arr[i] for i in range(len(arr)) if i % 3 == 1] + [arr[i] for i in range(len(arr)) if i % 3 == 2]
  s12prime = [pos_to_rank[i] for i in range(len(arr)) if i % 3 == 1] + [pos_to_rank[i] for i in range(len(arr)) if i % 3 == 2]
  #TODO:change this to recursion
  #sort it
  sa12prime = recursive_suffix_array(s12prime)
  # sa12prime = cheater_suffix_array(s12prime)
  #convert sa12prime to sa12
  halfway = int((len(sa12prime)+1)/2)
  sa12 = [i*3 + 1 if (i < halfway)
   else (i-halfway)*3 + 2 for i in sa12prime]

  #update pos to rank with unambigious ranks
  pos_to_rank = {}
  for i,val in enumerate(sa12):
    pos_to_rank[val] = i
  
  #make s0prime which is first letter of mod0 concatenaed with rank of mod1
  sa0 = [(arr[i], pos_to_rank.get(i+1) or 0, i) for i in range(len(arr)) if i % 3 == 0]
  sa0.sort()

  #now merge them
  i = 0
  j = 0
  sa = []
  while i < len(sa12) and j < len(sa0):
    if arr[sa12[i]] < arr[sa0[j][2]]:
      sa.append(sa12[i])
      i += 1
    elif arr[sa0[j][2]] < arr[sa12[i]]:
      sa.append(sa0[j][2])
      j += 1
    else:
      if (sa12[i] + 1) % 3 != 0:
        if pos_to_rank[sa12[i]+1] < pos_to_rank[sa0[j][2]+1]:
          sa.append(sa12[i])
          i += 1
        else:
          sa.append(sa0[j][2])
          j += 1
      else:
        if arr[sa12[i]+1] < arr[sa0[j][2]+1]:
          sa.append(sa12[i])
          i += 1
        elif arr[sa0[j][2]+1] < arr[sa12[i]+1]:
          sa.append(sa0[j][2])
          j += 1
        else:
          if pos_to_rank[sa12[i]+2] < pos_to_rank[sa0[j][2]+2]:
            sa.append(sa12[i])
            i += 1
          else:
            sa.append(sa0[j][2])
            j += 1

  while i < len(sa12):
    sa.append(sa12[i])
    i  += 1

  while j < len(sa0):
    sa.append(sa0[j][2])
    j += 1

  return sa[1:]


def cheater_suffix_array(arr):
  return [t[1] for t in sorted((arr[i:], i) for i in range(len(arr)))]
  
if __name__ == "__main__":
  for i in range(100):
    test = [random.choice(string.ascii_letters) for i in range(1000)]
    if cheater_suffix_array(test) != suffix_array(test):
      raise ValueError
