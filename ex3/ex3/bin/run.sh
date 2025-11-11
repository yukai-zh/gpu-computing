#!/bin/bash

################################################################################
# Ultra Simple Benchmark - Just run and show output
# Exercise 3.1: cudaMemcpy bandwidth testing
################################################################################

echo "========================================"
echo "CUDA Memory Benchmark - Exercise 3.1"
echo "cudaMemcpy Performance Testing"
echo "========================================"
echo ""

# Memory sizes from 1KB to 1GB
SIZES=(
    1024          # 1KB
    2048          # 2KB
    4096          # 4KB
    8192          # 8KB
    16384         # 16KB
    32768         # 32KB
    65536         # 64KB
    131072        # 128KB
    262144        # 256KB
    524288        # 512KB
    1048576       # 1MB
    4194304       # 4MB
    16777216      # 16MB
    67108864      # 64MB
    268435456     # 256MB
    1073741824    # 1GB
)

format_size() {
    local bytes=$1
    if [ $bytes -lt 1048576 ]; then
        printf "%6dKB" $((bytes/1024))
    elif [ $bytes -lt 1073741824 ]; then
        printf "%6dMB" $((bytes/1048576))
    else
        printf "%6dGB" $((bytes/1073741824))
    fi
}

################################################################################
# PAGEABLE MEMORY
################################################################################
echo "========================================="
echo "TEST 1: PAGEABLE MEMORY"
echo "========================================="
echo ""
printf "%-10s %15s %15s %15s\n" "Size" "H2D (GB/s)" "D2H (GB/s)" "D2D (GB/s)"
printf "%-10s %15s %15s %15s\n" "----------" "---------------" "---------------" "---------------"

for size in "${SIZES[@]}"; do
    size_str=$(format_size $size)
    printf "%-10s " "$size_str"
    
    # Run benchmark
    ./memCpy --global-coalesced -s $size -t 256 -g 16 -i 1 --im 10 2>&1 | \
        grep "H2D:" | \
        awk '{
            for(i=1;i<=NF;i++) {
                if($i=="H2D:") h2d=$(i+1);
                if($i=="D2H:") d2h=$(i+1);
                if($i=="D2D:") d2d=$(i+1);
            }
            printf "%15.2f %15.2f %15.2f\n", h2d, d2h, d2d
        }'
done

echo ""
echo ""

################################################################################
# PINNED MEMORY
################################################################################
echo "========================================="
echo "TEST 2: PINNED MEMORY"
echo "========================================="
echo ""
printf "%-10s %15s %15s %15s\n" "Size" "H2D (GB/s)" "D2H (GB/s)" "D2D (GB/s)"
printf "%-10s %15s %15s %15s\n" "----------" "---------------" "---------------" "---------------"

for size in "${SIZES[@]}"; do
    size_str=$(format_size $size)
    printf "%-10s " "$size_str"
    
    # Run benchmark with pinned memory
    ./memCpy --global-coalesced -s $size -t 256 -g 16 -i 1 --im 10 -p 2>&1 | \
        grep "H2D:" | \
        awk '{
            for(i=1;i<=NF;i++) {
                if($i=="H2D:") h2d=$(i+1);
                if($i=="D2H:") d2h=$(i+1);
                if($i=="D2D:") d2d=$(i+1);
            }
            printf "%15.2f %15.2f %15.2f\n", h2d, d2h, d2d
        }'
done

echo ""
echo "========================================"
echo "Done!"
echo "========================================"
