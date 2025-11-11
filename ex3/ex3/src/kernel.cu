/*************************************************************************************************
 *
 *        Computer Engineering Group, Heidelberg University - GPU Computing Exercise 03
 *
 *                           Group : gpu18
 *
 *                            File : main.cu
 *
 *                         Purpose : Memory Operations Benchmark
 *
 *************************************************************************************************/

//
// Kernels
//

__global__ void
globalMemCoalescedKernel(const int* src, int* dst, size_t n)
{
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
      dst[i] = src[i];
    }
}

void
globalMemCoalescedKernel_Wrapper(dim3 gridDim, dim3 blockDim, const int* src, int* dst, size_t n) {
	globalMemCoalescedKernel<<< gridDim, blockDim, 0 /*Shared Memory Size*/ >>>(src, dst, n);
}

__global__ void
globalMemStrideKernel(const int* src, int* dst, size_t n, size_t stride)
{
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        dst[i] = src[i * stride];
    }
}

void
globalMemStrideKernel_Wrapper(dim3 gridDim, dim3 blockDim, const int* src, int* dst, size_t n, size_t stride) {
	globalMemStrideKernel<<< gridDim, blockDim, 0 /*Shared Memory Size*/ >>>(src, dst, n, stride);
}

__global__ void
globalMemOffsetKernel(const int* src, int* dst, size_t n, size_t offset)
{
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        dst[i] = src[i + offset];
    }
}

void
globalMemOffsetKernel_Wrapper(dim3 gridDim, dim3 blockDim, const int* src, int* dst, size_t n, size_t offset) {
	globalMemOffsetKernel<<< gridDim, blockDim, 0 /*Shared Memory Size*/ >>>(src, dst, n, offset);
}

