#!/bin/bash

sizes=(1024 4096 16384 65536 262144 1048576 4194304 16777216 67108864 268435456 1073741824)

echo "size [B],H2D [GB/s],D2H [GB/s],D2D [GB/s],pinned_flag" > results.csv

for size in "${sizes[@]}"; do
    echo "==== Measuring Pageable Memory: $size B ===="
    ./bin/memCpy -s $size -im 100 | awk '/Results for cudaMemcpy:/ {print $0}' >> results.csv

    echo "==== Measuring Pinned Memory: $size B ===="
    ./bin/memCpy -p -s $size -im 100 | awk '/Results for cudaMemcpy:/ {print $0}' >> results.csv
done

echo "All measurements done! Results saved in results.csv"
