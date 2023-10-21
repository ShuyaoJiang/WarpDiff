import os
import sys

COMPILE_OPTIMIZATION_LEVELS = ['O0', 'O1', 'O2', 'O3']

BENCHMARK_DIR = os.path.join('..', 'test-suite', 'SingleSource', 'Benchmarks')
TARGET_DIR = os.path.join('..', 'targets')

CLANG_PATH = '/usr/bin/clang'
CLANGPP_PATH = '/usr/bin/clang++'
EMCC_PATH = 'emcc'

COMPILE_TARGET_NATIVE = 'native'
COMPILE_TARGET_WASM = 'wasm'

ADOBECPP = 'Adobe-C++'
BENCHMARKGAME = 'BenchmarkGame'
COYOTEBENCH = 'CoyoteBench'
DHRYSTONE = 'Dhrystone'
LINPACK = 'Linpack'
MCGILL = 'McGill'
MISC = 'Misc'
MISCCPP = 'Misc-C++'
MISCCPPEH = 'Misc-C++-EH'
POLYBENCH = 'Polybench'
SHOOTOUT = 'Shootout'
SHOOTOUTCPP = 'Shootout-C++'
SMALLPT = 'SmallPT'
STANDFORD = 'Stanford'

BENCHMARKS = [
    ADOBECPP, BENCHMARKGAME, COYOTEBENCH, DHRYSTONE, LINPACK, MCGILL, MISC, 
    MISCCPP, MISCCPPEH, POLYBENCH, SHOOTOUT, SHOOTOUTCPP, SMALLPT, STANDFORD
    ]

ADOBECPP_SOURCES = [
    'functionobjects.cpp', 'loop_unroll.cpp', 'simple_types_constant_folding.cpp',
    'simple_types_loop_invariant.cpp', 'stepanov_abstraction.cpp', 'stepanov_vector.cpp'
    ]

BENCHMARKGAME_SOURCES = [
    'Large/fasta.c', 'fannkuch.c', 'n-body.c', 'nsieve-bits.c', 'partialsums.c',
    'puzzle.c', 'recursive.c', 'spectral-norm.c'
    ]

COYOTEBENCH_SOURCES = ['almabench.c', 'fftbench.cpp', 'huffbench.c', 'lpbench.c']

DHRYSTONE_SOURCES = ['dry.c', 'fldry.c']

LINPACK_SOURCES = ['linpack-pc.c']

MCGILL_SOURCES = ['chomp.c', 'exptree.c', 'misr.c', 'queens.c']

MISC_SOURCES = [
    'dt.c', 'evalloop.c', 'fbench.c', 'ffbench.c', 'flops-1.c', 'flops-2.c', 'flops-3.c', 
    'flops-4.c', 'flops-5.c', 'flops-6.c', 'flops-7.c', 'flops-8.c', 'flops.c', 'fp-convert.c',
    'himenobmtxpa.c' , 'lowercase.c', 'mandel-2.c', 'mandel.c', 'matmul_f64_4x4.c', 'oourafft.c',
    'perlin.c', 'pi.c', 'ReedSolomon.c', 'revertBits.c', 'richards_benchmark.c', 'salsa20.c',
    'whetstone.c'
    ]

MISCCPP_SOURCES = [
    'Large/ray.cpp', 'Large/sphereflake.cpp', 'bigfib.cpp', 'mandel-text.cpp',
    'oopack_v1p8.cpp', 'stepanov_container.cpp', 'stepanov_v1p2.cpp'
    ]

MISCCPPEH_SOURCES = ['spirit.cpp']

POLYBENCH_SOURCES = [
    'datamining/correlation/correlation.c', 'datamining/covariance/covariance.c',
    'linear-algebra/kernels/2mm/2mm.c', 'linear-algebra/kernels/3mm/3mm.c',
    'linear-algebra/kernels/atax/atax.c', 'linear-algebra/kernels/bicg/bicg.c',
    'linear-algebra/kernels/cholesky/cholesky.c', 'linear-algebra/kernels/doitgen/doitgen.c', 
    'linear-algebra/kernels/gemm/gemm.c', 'linear-algebra/kernels/gemver/gemver.c',
    'linear-algebra/kernels/gesummv/gesummv.c', 'linear-algebra/kernels/mvt/mvt.c', 
    'linear-algebra/kernels/symm/symm.c', 'linear-algebra/kernels/syr2k/syr2k.c',
    'linear-algebra/kernels/syrk/syrk.c', 'linear-algebra/kernels/trisolv/trisolv.c',
    'linear-algebra/kernels/trmm/trmm.c', 
    'linear-algebra/solvers/durbin/durbin.c', 'linear-algebra/solvers/dynprog/dynprog.c',
    'linear-algebra/solvers/gramschmidt/gramschmidt.c',
    'linear-algebra/solvers/lu/lu.c', 'linear-algebra/solvers/ludcmp/ludcmp.c',
    'medley/floyd-warshall/floyd-warshall.c', 'medley/reg_detect/reg_detect.c',
    'stencils/adi/adi.c', 'stencils/fdtd-2d/fdtd-2d.c', 'stencils/fdtd-apml/fdtd-apml.c', 
    'stencils/jacobi-1d-imper/jacobi-1d-imper.c', 'stencils/jacobi-2d-imper/jacobi-2d-imper.c',
    'stencils/seidel-2d/seidel-2d.c'
]

SHOOTOUT_SOURCES = [
    'ackermann.c', 'ary3.c', 'fib2.c', 'hash.c', 'heapsort.c', 'hello.c', 'lists.c',
    'matrix.c', 'methcall.c', 'nestedloop.c', 'objinst.c', 'random.c', 'sieve.c', 'strcat.c'
    ]

SHOOTOUTCPP_SOURCES = [   
    'EH/except.cpp', 'ackermann.cpp', 'ary.cpp', 'ary2.cpp', 'ary3.cpp', 'fibo.cpp',
    'hash.cpp', 'hash2.cpp', 'heapsort.cpp', 'hello.cpp', 'lists.cpp', 'lists1.cpp',
    'matrix.cpp', 'methcall.cpp', 'moments.cpp', 'nestedloop.cpp', 'objinst.cpp', 
    'random.cpp', 'reversefile.cpp', 'sieve.cpp', 'spellcheck.cpp', 'strcat.cpp',
    'sumcol.cpp', 'wc.cpp', 'wordfreq.cpp'
]

SMALLPT_SOURCES = ['smallpt.cpp']

STANDFORD_SOURCES = [
    'Bubblesort.c', 'FloatMM.c', 'IntMM.c', 'Oscar.c', 'Perm.c', 'Puzzle.c', 'Queens.c',
    'Quicksort.c', 'RealMM.c', 'Towers.c', 'Treesort.c'
]

SOURCE_MAP = {
    ADOBECPP: ADOBECPP_SOURCES,
    BENCHMARKGAME: BENCHMARKGAME_SOURCES,
    COYOTEBENCH: COYOTEBENCH_SOURCES, 
    DHRYSTONE: DHRYSTONE_SOURCES, 
    LINPACK: LINPACK_SOURCES, 
    MCGILL: MCGILL_SOURCES, 
    MISC: MISC_SOURCES, 
    MISCCPP: MISCCPP_SOURCES, 
    MISCCPPEH: MISCCPPEH_SOURCES, 
    POLYBENCH: POLYBENCH_SOURCES, 
    SHOOTOUT: SHOOTOUT_SOURCES, 
    SHOOTOUTCPP: SHOOTOUTCPP_SOURCES, 
    SMALLPT: SMALLPT_SOURCES, 
    STANDFORD: STANDFORD_SOURCES
}

TARGET_SUFFIX = {
    COMPILE_TARGET_NATIVE: '',
    COMPILE_TARGET_WASM: '.wasm'
}


def get_compile_command(benchmark, source, target_type, out_dir):
    benchmark_path = os.path.join(BENCHMARK_DIR, benchmark)
    source_path = os.path.join(benchmark_path, source)
    source_type = os.path.splitext(os.path.basename(source_path))[1]
    target_name = os.path.splitext(os.path.basename(source_path))[0] + TARGET_SUFFIX[target_type]

    if target_type == COMPILE_TARGET_NATIVE and source_type == '.c':
        command_template = '%s -%s -lm %%s' % (CLANG_PATH, op_level)
    elif target_type == COMPILE_TARGET_NATIVE and source_type == '.cpp':
        command_template = '%s -%s -lm %%s' % (CLANGPP_PATH, op_level)
    elif target_type == COMPILE_TARGET_WASM:
        command_template = '%s -%s -s WASM=1 -s TOTAL_MEMORY=512MB %%s' % (EMCC_PATH, op_level)

    if benchmark == POLYBENCH:
        source_part = '-I %s -I %s %s -DFP_ABSTOLERANCE=1e-5 -DPOLYBENCH_TIME -o %s' % (
            os.path.join(benchmark_path, 'utilities'),
            os.path.dirname(source_path),
            source_path,
            os.path.join(out_dir, target_name)
        )
    else:
        source_part = '%s -o %s' % (
            source_path,
            os.path.join(out_dir, target_name)
        )

    command = command_template % source_part
    return command


def compile_by_target(benchmark, target_type):
    print('Compile '+ benchmark + ' to '+ target_type + ':')
    out_dir = os.path.join(TARGET_DIR, op_level, benchmark, target_type)
    os.makedirs(out_dir, exist_ok=True)
    benchmark_sources = SOURCE_MAP[benchmark]
    for source in benchmark_sources:
        command = get_compile_command(benchmark, source, target_type, out_dir)
        print(command)
        os.system(command)
    print()


def compile_all():
    for benchmark in BENCHMARKS:
        compile_by_target(benchmark, COMPILE_TARGET_NATIVE)
        compile_by_target(benchmark, COMPILE_TARGET_WASM)
   

def main():
    if len(sys.argv) != 2:
        print('Wrong number of parameters')
    elif not sys.argv[1] in COMPILE_OPTIMIZATION_LEVELS:
        print('Wrong optimizaion level')
    else:
        global op_level
        op_level = sys.argv[1]
        compile_all()


if __name__=="__main__":
    main()
