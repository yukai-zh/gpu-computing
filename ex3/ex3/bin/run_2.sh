#!/bin/bash

# Benchmark script for CUDA memory access patterns
# This script runs systematic experiments to measure memory bandwidth

OUTPUT_DIR="results"
mkdir -p $OUTPUT_DIR

ITERATIONS=1000

echo "=========================================="
echo "CUDA Memory Benchmark Suite"
echo "=========================================="
echo ""

# Experiment 1: Vary threads per block (1 block)
echo "Experiment 1: Varying threads per block (1 to 1024, 1 block)"
echo "=============================================================="
OUTPUT_FILE="$OUTPUT_DIR/exp1_threads_per_block.csv"
echo "threads_per_block,bandwidth_gbps" > $OUTPUT_FILE

for threads in 1 2 4 8 16 32 64 128 256 512 1024; do
    echo "Testing with $threads threads per block..."
    result=$(./memCpy --global-coalesced -t $threads -g 1 -i $ITERATIONS | grep "Coalesced" | awk '{print $NF}' | sed 's/GB\/s//')
    echo "$threads,$result" >> $OUTPUT_FILE
    echo "  Bandwidth: $result GB/s"
done
echo ""

# Experiment 2: Vary number of blocks (with optimal thread count from Exp 1)
# You should replace 256 with the optimal value found in Experiment 1
OPTIMAL_THREADS=256

echo "Experiment 2: Varying number of blocks (1 to 32, $OPTIMAL_THREADS threads/block)"
echo "================================================================================"
OUTPUT_FILE="$OUTPUT_DIR/exp2_blocks_per_grid.csv"
echo "blocks_per_grid,bandwidth_gbps" > $OUTPUT_FILE

for blocks in 1 2 4 8 16 32; do
    echo "Testing with $blocks blocks..."
    result=$(./memCpy --global-coalesced -t $OPTIMAL_THREADS -g $blocks -i $ITERATIONS | grep "Coalesced" | awk '{print $NF}' | sed 's/GB\/s//')
    echo "$blocks,$result" >> $OUTPUT_FILE
    echo "  Bandwidth: $result GB/s"
done
echo ""

# Experiment 3: 2D optimization - vary both threads and blocks
echo "Experiment 3: 2D Optimization (threads × blocks)"
echo "================================================="
OUTPUT_FILE="$OUTPUT_DIR/exp3_2d_optimization.csv"
echo "threads_per_block,blocks_per_grid,bandwidth_gbps" > $OUTPUT_FILE

for threads in 32 64 128 256 512; do
    for blocks in 1 2 4 8 16 32; do
        echo "Testing with $threads threads/block, $blocks blocks..."
        result=$(./memCpy --global-coalesced -t $threads -g $blocks -i $ITERATIONS | grep "Coalesced" | awk '{print $NF}' | sed 's/GB\/s//')
        echo "$threads,$blocks,$result" >> $OUTPUT_FILE
        echo "  Bandwidth: $result GB/s"
    done
done
echo ""

# Experiment 4: Compare coalesced vs strided access
echo "Experiment 4: Coalesced vs Strided Access Patterns"
echo "===================================================="
OUTPUT_FILE="$OUTPUT_DIR/exp4_stride_comparison.csv"
echo "stride,bandwidth_gbps" > $OUTPUT_FILE

# Coalesced (stride=1)
echo "Testing coalesced access (stride=1)..."
result=$(./memCpy --global-coalesced -t 256 -g 16 -i $ITERATIONS | grep "Coalesced" | awk '{print $NF}' | sed 's/GB\/s//')
echo "1,$result" >> $OUTPUT_FILE
echo "  Bandwidth: $result GB/s"

# Various strides
for stride in 2 4 8 16 32; do
    echo "Testing strided access (stride=$stride)..."
    result=$(./memCpy --global-stride --stride $stride -t 256 -g 16 -i $ITERATIONS | grep "Strided" | awk '{print $NF}' | sed 's/GB\/s//')
    echo "$stride,$result" >> $OUTPUT_FILE
    echo "  Bandwidth: $result GB/s"
done
echo ""

# Experiment 5: Effect of memory offset
echo "Experiment 5: Effect of Memory Offset"
echo "======================================"
OUTPUT_FILE="$OUTPUT_DIR/exp5_offset_comparison.csv"
echo "offset,bandwidth_gbps" > $OUTPUT_FILE

for offset in 0 1 2 4 8 16 32; do
    echo "Testing with offset=$offset..."
    result=$(./memCpy --global-offset --offset $offset -t 256 -g 16 -i $ITERATIONS | grep "Offset" | awk '{print $NF}' | sed 's/GB\/s//')
    echo "$offset,$result" >> $OUTPUT_FILE
    echo "  Bandwidth: $result GB/s"
done
echo ""

# Experiment 6: Varying memory sizes
echo "Experiment 6: Effect of Memory Size"
echo "====================================="
OUTPUT_FILE="$OUTPUT_DIR/exp6_memory_size.csv"
echo "memory_size_mb,bandwidth_gbps" > $OUTPUT_FILE

for size_mb in 1 2 4 8 16 32 64 128; do
    size_bytes=$((size_mb * 1024 * 1024))
    echo "Testing with memory size=${size_mb}MB..."
    result=$(./memCpy --global-coalesced -s $size_bytes -t 256 -g 16 -i $ITERATIONS | grep "Coalesced" | awk '{print $NF}' | sed 's/GB\/s//')
    echo "$size_mb,$result" >> $OUTPUT_FILE
    echo "  Bandwidth: $result GB/s"
done
echo ""

echo "=========================================="
echo "All benchmarks completed!"
echo "Results saved in $OUTPUT_DIR/"
echo "=========================================="
