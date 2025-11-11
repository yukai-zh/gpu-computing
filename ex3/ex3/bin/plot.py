#!/usr/bin/env python3
"""
Visualization script for CUDA memory benchmark results
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

RESULTS_DIR = "results"
OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_experiment1():
    """Plot: Threads per Block vs Bandwidth"""
    print("Plotting Experiment 1: Threads per Block...")
    df = pd.read_csv(f"{RESULTS_DIR}/exp1_threads_per_block.csv")
    
    fig, ax = plt.subplots()
    ax.plot(df['threads_per_block'], df['bandwidth_gbps'], 
            marker='o', linewidth=2, markersize=8, color='#2E86AB')
    ax.set_xlabel('Threads per Block', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bandwidth (GB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Bandwidth vs Threads per Block\n(Single Block)', 
                 fontsize=14, fontweight='bold')
    ax.set_xscale('log', base=2)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(df['threads_per_block'])
    ax.set_xticklabels(df['threads_per_block'])
    
    # Add optimal point marker
    max_idx = df['bandwidth_gbps'].idxmax()
    optimal_threads = df.loc[max_idx, 'threads_per_block']
    optimal_bw = df.loc[max_idx, 'bandwidth_gbps']
    ax.plot(optimal_threads, optimal_bw, 'r*', markersize=20, 
            label=f'Optimal: {optimal_threads} threads')
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/exp1_threads_per_block.png", dpi=300)
    print(f"  Optimal configuration: {optimal_threads} threads/block, {optimal_bw:.2f} GB/s")
    plt.close()

def plot_experiment2():
    """Plot: Blocks per Grid vs Bandwidth"""
    print("Plotting Experiment 2: Blocks per Grid...")
    df = pd.read_csv(f"{RESULTS_DIR}/exp2_blocks_per_grid.csv")
    
    fig, ax = plt.subplots()
    ax.plot(df['blocks_per_grid'], df['bandwidth_gbps'], 
            marker='s', linewidth=2, markersize=8, color='#A23B72')
    ax.set_xlabel('Blocks per Grid', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bandwidth (GB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Bandwidth vs Number of Blocks\n(Fixed Threads per Block)', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add optimal point marker
    max_idx = df['bandwidth_gbps'].idxmax()
    optimal_blocks = df.loc[max_idx, 'blocks_per_grid']
    optimal_bw = df.loc[max_idx, 'bandwidth_gbps']
    ax.plot(optimal_blocks, optimal_bw, 'r*', markersize=20, 
            label=f'Optimal: {optimal_blocks} blocks')
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/exp2_blocks_per_grid.png", dpi=300)
    print(f"  Optimal configuration: {optimal_blocks} blocks, {optimal_bw:.2f} GB/s")
    plt.close()

def plot_experiment3():
    """Plot: 2D Optimization Heatmap"""
    print("Plotting Experiment 3: 2D Optimization...")
    df = pd.read_csv(f"{RESULTS_DIR}/exp3_2d_optimization.csv")
    
    # Pivot for heatmap
    pivot_table = df.pivot(index='threads_per_block', 
                           columns='blocks_per_grid', 
                           values='bandwidth_gbps')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(pivot_table.values, cmap='YlOrRd', aspect='auto')
    
    # Set ticks
    ax.set_xticks(np.arange(len(pivot_table.columns)))
    ax.set_yticks(np.arange(len(pivot_table.index)))
    ax.set_xticklabels(pivot_table.columns)
    ax.set_yticklabels(pivot_table.index)
    
    # Labels
    ax.set_xlabel('Blocks per Grid', fontsize=12, fontweight='bold')
    ax.set_ylabel('Threads per Block', fontsize=12, fontweight='bold')
    ax.set_title('Memory Bandwidth Heatmap\n(Threads per Block × Blocks per Grid)', 
                 fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Bandwidth (GB/s)', rotation=270, labelpad=20, fontsize=11)
    
    # Add text annotations
    for i in range(len(pivot_table.index)):
        for j in range(len(pivot_table.columns)):
            text = ax.text(j, i, f'{pivot_table.values[i, j]:.1f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    # Mark optimal configuration
    max_bw = df['bandwidth_gbps'].max()
    optimal_config = df[df['bandwidth_gbps'] == max_bw].iloc[0]
    opt_threads_idx = list(pivot_table.index).index(optimal_config['threads_per_block'])
    opt_blocks_idx = list(pivot_table.columns).index(optimal_config['blocks_per_grid'])
    ax.add_patch(plt.Rectangle((opt_blocks_idx-0.5, opt_threads_idx-0.5), 1, 1, 
                               fill=False, edgecolor='blue', linewidth=3))
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/exp3_2d_optimization.png", dpi=300)
    print(f"  Optimal: {optimal_config['threads_per_block']} threads/block, "
          f"{optimal_config['blocks_per_grid']} blocks, {max_bw:.2f} GB/s")
    plt.close()
    
    # Additional 3D surface plot
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    X, Y = np.meshgrid(pivot_table.columns, pivot_table.index)
    ax.plot_surface(X, Y, pivot_table.values, cmap='viridis', alpha=0.8)
    
    ax.set_xlabel('Blocks per Grid', fontsize=11, fontweight='bold')
    ax.set_ylabel('Threads per Block', fontsize=11, fontweight='bold')
    ax.set_zlabel('Bandwidth (GB/s)', fontsize=11, fontweight='bold')
    ax.set_title('3D View: Memory Bandwidth Optimization', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/exp3_2d_optimization_3d.png", dpi=300)
    plt.close()

def plot_experiment4():
    """Plot: Stride Comparison"""
    print("Plotting Experiment 4: Stride Comparison...")
    df = pd.read_csv(f"{RESULTS_DIR}/exp4_stride_comparison.csv")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Linear scale
    ax1.plot(df['stride'], df['bandwidth_gbps'], 
             marker='o', linewidth=2, markersize=8, color='#F18F01')
    ax1.set_xlabel('Stride', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Bandwidth (GB/s)', fontsize=12, fontweight='bold')
    ax1.set_title('Memory Bandwidth vs Stride (Linear Scale)', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Log scale
    ax2.plot(df['stride'], df['bandwidth_gbps'], 
             marker='o', linewidth=2, markersize=8, color='#C73E1D')
    ax2.set_xlabel('Stride', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Bandwidth (GB/s)', fontsize=12, fontweight='bold')
    ax2.set_title('Memory Bandwidth vs Stride (Log Scale)', fontsize=13, fontweight='bold')
    ax2.set_xscale('log', base=2)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/exp4_stride_comparison.png", dpi=300)
    
    # Calculate bandwidth degradation
    coalesced_bw = df[df['stride'] == 1]['bandwidth_gbps'].values[0]
    print(f"  Coalesced bandwidth: {coalesced_bw:.2f} GB/s")
    for _, row in df.iterrows():
        if row['stride'] > 1:
            degradation = (1 - row['bandwidth_gbps']/coalesced_bw) * 100
            print(f"  Stride {int(row['stride'])}: {row['bandwidth_gbps']:.2f} GB/s "
                  f"({degradation:.1f}% degradation)")
    plt.close()

def plot_experiment5():
    """Plot: Offset Effect"""
    print("Plotting Experiment 5: Offset Effect...")
    df = pd.read_csv(f"{RESULTS_DIR}/exp5_offset_comparison.csv")
    
    fig, ax = plt.subplots()
    ax.plot(df['offset'], df['bandwidth_gbps'], 
            marker='D', linewidth=2, markersize=8, color='#6A4C93')
    ax.set_xlabel('Offset (elements)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bandwidth (GB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Bandwidth vs Access Offset', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Highlight misaligned offsets
    aligned_bw = df[df['offset'] == 0]['bandwidth_gbps'].values[0]
    for _, row in df.iterrows():
        if row['offset'] % 32 != 0 and row['offset'] != 0:
            ax.axvline(x=row['offset'], color='red', alpha=0.2, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/exp5_offset_comparison.png", dpi=300)
    print(f"  Aligned (offset=0): {aligned_bw:.2f} GB/s")
    plt.close()

def plot_experiment6():
    """Plot: Memory Size Effect"""
    print("Plotting Experiment 6: Memory Size Effect...")
    df = pd.read_csv(f"{RESULTS_DIR}/exp6_memory_size.csv")
    
    fig, ax = plt.subplots()
    ax.plot(df['memory_size_mb'], df['bandwidth_gbps'], 
            marker='o', linewidth=2, markersize=8, color='#1E847F')
    ax.set_xlabel('Memory Size (MB)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bandwidth (GB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Bandwidth vs Transfer Size', fontsize=14, fontweight='bold')
    ax.set_xscale('log', base=2)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(df['memory_size_mb'])
    ax.set_xticklabels(df['memory_size_mb'])
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/exp6_memory_size.png", dpi=300)
    plt.close()

def generate_summary_report():
    """Generate a text summary of all experiments"""
    print("\nGenerating summary report...")
    
    with open(f"{OUTPUT_DIR}/summary_report.txt", 'w') as f:
        f.write("="*70 + "\n")
        f.write("CUDA MEMORY BENCHMARK SUMMARY REPORT\n")
        f.write("="*70 + "\n\n")
        
        # Exp 1
        df1 = pd.read_csv(f"{RESULTS_DIR}/exp1_threads_per_block.csv")
        max_idx = df1['bandwidth_gbps'].idxmax()
        f.write("Experiment 1: Threads per Block Optimization\n")
        f.write("-" * 70 + "\n")
        f.write(f"Optimal: {df1.loc[max_idx, 'threads_per_block']} threads/block\n")
        f.write(f"Bandwidth: {df1.loc[max_idx, 'bandwidth_gbps']:.2f} GB/s\n")
        f.write(f"Range: {df1['bandwidth_gbps'].min():.2f} - {df1['bandwidth_gbps'].max():.2f} GB/s\n\n")
        
        # Exp 2
        df2 = pd.read_csv(f"{RESULTS_DIR}/exp2_blocks_per_grid.csv")
        max_idx = df2['bandwidth_gbps'].idxmax()
        f.write("Experiment 2: Blocks per Grid Optimization\n")
        f.write("-" * 70 + "\n")
        f.write(f"Optimal: {df2.loc[max_idx, 'blocks_per_grid']} blocks\n")
        f.write(f"Bandwidth: {df2.loc[max_idx, 'bandwidth_gbps']:.2f} GB/s\n")
        f.write(f"Range: {df2['bandwidth_gbps'].min():.2f} - {df2['bandwidth_gbps'].max():.2f} GB/s\n\n")
        
        # Exp 3
        df3 = pd.read_csv(f"{RESULTS_DIR}/exp3_2d_optimization.csv")
        max_bw = df3['bandwidth_gbps'].max()
        optimal_config = df3[df3['bandwidth_gbps'] == max_bw].iloc[0]
        f.write("Experiment 3: 2D Optimization\n")
        f.write("-" * 70 + "\n")
        f.write(f"Optimal: {optimal_config['threads_per_block']} threads/block, "
                f"{optimal_config['blocks_per_grid']} blocks\n")
        f.write(f"Bandwidth: {max_bw:.2f} GB/s\n\n")
        
        # Exp 4
        df4 = pd.read_csv(f"{RESULTS_DIR}/exp4_stride_comparison.csv")
        coalesced_bw = df4[df4['stride'] == 1]['bandwidth_gbps'].values[0]
        f.write("Experiment 4: Stride Impact\n")
        f.write("-" * 70 + "\n")
        f.write(f"Coalesced (stride=1): {coalesced_bw:.2f} GB/s\n")
        for _, row in df4.iterrows():
            if row['stride'] > 1:
                degradation = (1 - row['bandwidth_gbps']/coalesced_bw) * 100
                f.write(f"Stride {int(row['stride'])}: {row['bandwidth_gbps']:.2f} GB/s "
                       f"({degradation:.1f}% degradation)\n")
        f.write("\n")
        
        f.write("="*70 + "\n")
        f.write("KEY FINDINGS:\n")
        f.write("="*70 + "\n")
        f.write("1. Memory coalescing is critical for optimal bandwidth\n")
        f.write("2. Thread block size affects occupancy and performance\n")
        f.write("3. Sufficient parallelism (blocks) needed to saturate memory\n")
        f.write("4. Strided access causes significant performance degradation\n")
        f.write("5. Memory alignment affects coalescing efficiency\n")
    
    print("  Summary report saved to plots/summary_report.txt")

def main():
    """Main plotting function"""
    print("\n" + "="*70)
    print("CUDA Memory Benchmark Visualization")
    print("="*70 + "\n")
    
    try:
        plot_experiment1()
        plot_experiment2()
        plot_experiment3()
        plot_experiment4()
        plot_experiment5()
        plot_experiment6()
        generate_summary_report()
        
        print("\n" + "="*70)
        print(f"All plots saved to '{OUTPUT_DIR}/' directory")
        print("="*70 + "\n")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find results file: {e}")
        print("Please run the benchmark script first: ./run_benchmarks.sh")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
