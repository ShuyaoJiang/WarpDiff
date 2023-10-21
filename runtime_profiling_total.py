import os
import sys
from time import perf_counter
import func_timeout
from func_timeout import func_set_timeout
from numpy import mean
import csv
import traceback
from compile_to_target import COMPILE_OPTIMIZATION_LEVELS, COMPILE_TARGET_NATIVE, \
    COMPILE_TARGET_WASM, BENCHMARKS, ADOBECPP, BENCHMARKGAME, COYOTEBENCH, DHRYSTONE, \
    LINPACK, MCGILL, MISC, MISCCPP, MISCCPPEH, POLYBENCH, SHOOTOUT, SHOOTOUTCPP, SMALLPT, STANDFORD, \
    TARGET_SUFFIX

TEST_TIMES = 10

NATIVE = 'x86native'
WASMER = 'wasmer'
WASMTIME = 'wasmtime'
WASM3 = 'wasm3'
WASMEDGE = 'wasmedge'
WASMEDGE_AOT = 'wasmedge_aot'
WAMR = 'wamr'
WAVM = 'wavm'
RUNTIMES = [NATIVE, WASMER, WASMTIME, WASM3, WAMR, WAVM]

TARGET_DIR = os.path.join('..', 'targets')
PROFILINGDATA_DIR = os.path.join('..', 'profiling_data')

EXECUTE_COMMAND_TEMPLATE = {
    NATIVE: './%s',
    WASMER: 'wasmer %s',
    WASMTIME: 'wasmtime %s',
    WASM3: 'wasm3 %s',
    WASMEDGE: 'wasmedge %s',
    WASMEDGE_AOT: 'wasmedge %s',
    # WASMEDGE_AOT: 'wasmedgec %s %s && wasmedge %s',
    WAMR: 'iwasm %s',
    WAVM: 'wavm run %s'
}


def write_csv(data, file):
    print('Write to ' + file)
    if not os.path.exists(file):
        with open(file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
    else:
        with open(file, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)  
    

def profile_bin_size_by_target(target, out_dir):
    target_name = os.path.basename(target)
    target_size = os.path.getsize(target)
    data = ['bin_size', target_name, target_size]
    if target.endswith(TARGET_SUFFIX[COMPILE_TARGET_WASM]):
        out_file = os.path.join(out_dir, 'wasm_bin_size.csv')
    else:
        out_file = os.path.join(out_dir, 'native_bin_size.csv')
    write_csv(data, out_file)


def profile_bin_size(native_target, wasm_target, out_dir):
    target_size_out_dir = os.path.join(out_dir, 'bin_size')
    os.makedirs(target_size_out_dir, exist_ok=True)
    profile_bin_size_by_target(native_target, target_size_out_dir)
    profile_bin_size_by_target(wasm_target, target_size_out_dir)
    

def profile_execution_time(native_target, wasm_target, out_dir):
    for runtime in RUNTIMES:
        if runtime == NATIVE:
            target = native_target
        elif runtime == WASMEDGE_AOT:
            # a.wasm -> a_aot.wasm
            wasm_aot_target = os.path.join(os.path.dirname(wasm_target), 
                os.path.splitext(os.path.basename(wasm_target))[0] + '_wasmedge_aot.wasm')
            aot_compile_command = 'wasmedgec %s %s' % (wasm_target, wasm_aot_target)
            print(aot_compile_command)
            os.system(aot_compile_command)
            target = wasm_aot_target
        else: 
            target = wasm_target
        execute_command = EXECUTE_COMMAND_TEMPLATE[runtime] % target
        print(execute_command)

        times = []
        for i in range(TEST_TIMES):
            try:            
                start = perf_counter()
                run(execute_command)
                end = perf_counter()
                execution_time = end - start
                times.append(execution_time)
            except func_timeout.exceptions.FunctionTimedOut as e:
                print(e)
                break
        avg_time = mean(times)
        print('Average time:', avg_time)

        target_name = os.path.basename(target)
        data = ['execution_time', runtime, target_name, avg_time]
        execution_time_out_dir = os.path.join(out_dir, 'execution_time')
        os.makedirs(execution_time_out_dir, exist_ok=True)
        out_file = os.path.join(execution_time_out_dir, 'execution_time_' + runtime + '.csv')
        write_csv(data, out_file)


@func_set_timeout(600)
def run(command):
    os.system(command)


def profile_by_source(native_target, wasm_target, out_dir):
    # profile_bin_size(native_target, wasm_target, out_dir)
    profile_execution_time(native_target, wasm_target, out_dir)


def profile_by_benchmark(benchmark):
    print('Profile ' + benchmark + ':')
    benchmark_dir = os.path.join(TARGET_DIR, op_level, benchmark)
    native_dir = os.path.join(benchmark_dir, COMPILE_TARGET_NATIVE)
    wasm_dir = os.path.join(benchmark_dir, COMPILE_TARGET_WASM)
    benchmark_out_dir = os.path.join(PROFILINGDATA_DIR, op_level, benchmark)
    os.makedirs(benchmark_out_dir, exist_ok=True)

    native_targets = os.listdir(native_dir)
    wasm_targets = os.listdir(wasm_dir)
    for native_target_name in native_targets:
        wasm_target_name = native_target_name + TARGET_SUFFIX[COMPILE_TARGET_WASM]
        if wasm_target_name in wasm_targets:
            native_target_path = os.path.join(native_dir, native_target_name)
            wasm_target_path = os.path.join(wasm_dir, wasm_target_name)
            profile_by_source(native_target_path, wasm_target_path, benchmark_out_dir)


def profile_all():
    for benchmark in BENCHMARKS:
        profile_by_benchmark(benchmark)


def main():
    if len(sys.argv) != 2:
        print('Wrong number of parameters')
    elif not sys.argv[1] in COMPILE_OPTIMIZATION_LEVELS:
        print('Wrong optimizaion level')
    else:
        global op_level
        op_level = sys.argv[1]
        # profile_all()
        profile_by_benchmark(BENCHMARKGAME)


if __name__=="__main__":
    main()
