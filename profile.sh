echo 'type, gen_len, x(num_reads, y(read_length), setup_time, match_time, base_memory, setup_memory' > $1.csv
python3 driver.py $1 1000000 10000 100 False >> $1.csv

for (( y=1; y<=2**10; y*=2))
do
  python3 driver.py $1 1000000 10000 $y False >> $1.csv
done

for (( x=1; x<=2**20; x*=2))
do
  python3 driver.py $1 1000000 $x 100 False >> $1.csv
done

