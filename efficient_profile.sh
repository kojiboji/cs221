echo 'type, gen_len, x(num_reads, y(read_length), setup_time, match_time, base_memory, setup_memory' > ebwt.csv
python3 driver.py ebwt 1000000 10000 100 False >> ebwt.csv

for (( k=1; k<=2**7; k*=2))
do
  for (( c=1; c<=2**7; c*=2))
  do
    python3 driver.py ebwt 1000000 10000 100 False $k $c >> ebwt.csv
  done
done

