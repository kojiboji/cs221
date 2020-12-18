echo 'type, gen_len, x, y, setup_time, match_time, setup_memory, total_memory, k, c' > ebwt.csv

for (( k=1; k<=2**7; k*=2))
do
  for (( c=1; c<=2**7; c*=2))
  do
    python3 driver.py ebwt 1000000 10000 100 False $k $c >> ebwt.csv
  done
done

