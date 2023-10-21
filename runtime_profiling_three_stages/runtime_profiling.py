import os
import sys
from time import perf_counter, sleep
import func_timeout
from func_timeout import func_set_timeout
from numpy import mean
import csv
import traceback
import subprocess
from datetime import datetime
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
WASMEDGE_AOT = 'wasmedgec'
WAMR = 'iwasm'
WAMR_AOT = 'wamrc'
WAMR_AOT_RT = "wamr-aot-rt"
WAMR_JIT = 'iwasm-jit'
WAVM = 'wavm'
RUNTIMES = [WASMER, WASMTIME, WASM3, WASMEDGE_AOT, WASMEDGE, WAMR_AOT, WAMR, WAMR_JIT]

TARGET_DIR = os.path.join('..', 'targets')
PROFILIGDATA_DIR = os.path.join('..', 'profiling_data')
PERF_LOG_DIR = os.path.join('..', 'perf_log')

EXECUTE_COMMAND_TEMPLATE = {
    NATIVE: './%s',
    WASMER: '/home/ringzzz/wasm_runtime/wasmer/target/release/wasmer %s',
    WASMTIME: 'wasmtime %s',
    WASM3: 'wasm3 %s',
    WASMEDGE: 'wasmedge %s',
    WASMEDGE_AOT: 'wasmedge %s',
    # WASMEDGE_AOT: 'wasmedgec %s %s && wasmedge %s',
    WAMR: 'iwasm %s',
    # WAVM: 'wavm run %s'
}

TIME_UNIT = 1000000
PROBE_NUM = 5

RUNTIMES_PROBES = {
    WASMER: ["sched:sched_process_exec", "probe_wasmer:abs_591f00", "probe_wasmer:abs_8d5ee0", "sched:sched_process_exit"],
    WASMTIME: ["sched:sched_process_exec", "probe_wasmtime:abs_2e73c0", "probe_wasmtime:abs_398ce0", "sched:sched_process_exit"],
    WASM3: ["sched:sched_process_exec", "probe_wasm3:main", "probe_wasm3:repl_call", "sched:sched_process_exit"],
    WASMEDGE: ["sched:sched_process_exec", "probe_libwasmedge:abs_59710", "probe_libwasmedge:abs_d4de0", "sched:sched_process_exit"],
    WASMEDGE_AOT: ["probe_libwasmedge:abs_15eda0", "probe_libwasmedge:abs_167e90"],
    WAMR: ["sched:sched_process_exec", "probe_iwasm:abs_8850", "probe_iwasm:abs_e2d0", "sched:sched_process_exit"],
    WAMR_AOT: ["probe_wamrc:abs_3b4bc0", "probe_wamrc:abs_3b9af0"],
    WAMR_AOT_RT: ["sched:sched_process_exec", "probe_iwasm:abs_8850", "probe_iwasm:abs_170f0", "sched:sched_process_exit"],
    WAMR_JIT: ["sched:sched_process_exec", "probe_iwasm:abs_1c0c00", "probe_iwasm:abs_23e350", "sched:sched_process_exit"]
}

RUNTIME_PATH = {
    WASMER: '/home/ringzzz/wasm_runtime/wasmer/target/release/wasmer',
    WASMTIME: '/home/ringzzz/wasm_runtime/wasmtime/target/release/wasmtime',
    WASM3: '/home/ringzzz/wasm_runtime/wasm3/build/wasm3',
    WASMEDGE: '/home/ringzzz/wasm_runtime/WasmEdge/build/tools/wasmedge/wasmedge',
    WASMEDGE_AOT: '/home/ringzzz/wasm_runtime/WasmEdge/build/tools/wasmedge/wasmedgec',
    WAMR: '/home/ringzzz/wasm_runtime/wasm-micro-runtime/product-mini/platforms/linux/build-fast-interp/iwasm',
    WAMR_AOT: '/home/ringzzz/wasm_runtime/wasm-micro-runtime/wamr-compiler/build/wamrc',
    WAMR_JIT: '/home/ringzzz/wasm_runtime/wasm-micro-runtime/product-mini/platforms/linux/build/iwasm'
}

RUNTIME_CMDS = {
    WASMER: [
        ["{runtime} {wasm}", f"make {WASMER}-perf-record", RUNTIMES_PROBES[WASMER], WASMER, WASMER],
    ],
    WASMTIME: [
        ["{runtime} {wasm} --disable-cache", f"make {WASMTIME}-perf-record", RUNTIMES_PROBES[WASMTIME], WASMTIME, WASMTIME],
    ],
    WASM3: [
        ["{runtime} {wasm}", f"make {WASM3}-perf-record", RUNTIMES_PROBES[WASM3], WASM3, WASM3],
        ["{runtime} --compile {wasm}", f"make {WASM3}-perf-record", RUNTIMES_PROBES[WASM3], WASM3, f"{WASM3}--compile"],
    ],
    WASMEDGE_AOT: [
        ["{runtime} {wasm} {wasm_aot}", f"make {WASMEDGE_AOT}-perf-record", RUNTIMES_PROBES[WASMEDGE_AOT], WASMEDGE_AOT, WASMEDGE_AOT],
    ],
    WASMEDGE: [
        ["{runtime} {wasm_aot}", f"make {WASMEDGE}-perf-record", RUNTIMES_PROBES[WASMEDGE], WASMEDGE, f"{WASMEDGE}_aot"],
    ],
    WAMR_AOT: [
        ["{runtime} -o {wasm_aot} {wasm}", f"make {WAMR_AOT}-perf-record", RUNTIMES_PROBES[WAMR_AOT], WAMR_AOT, WAMR_AOT],
    ],
    WAMR: [
        ["{runtime} {wasm}", f"make {WAMR}-perf-record", RUNTIMES_PROBES[WAMR], WAMR, WAMR],
        ["{runtime} {wasm_aot}", f"make {WAMR}-perf-record", RUNTIMES_PROBES[WAMR_AOT_RT], WAMR, f"{WAMR}_aot"],
    ],
    WAMR_JIT: [  
        ["{runtime} --fast-jit {wasm}", f"make {WAMR_JIT}-perf-record", RUNTIMES_PROBES[WAMR_JIT], WAMR, f"{WAMR}--fast-jit"],
        ["{runtime} --llvm-jit {wasm}", f"make {WAMR_JIT}-perf-record", RUNTIMES_PROBES[WAMR_JIT], WAMR, f"{WAMR}--llvm-jit"],
        ["{runtime} --multi-tier-jit {wasm}", f"make {WAMR_JIT}-perf-record",RUNTIMES_PROBES[WAMR_JIT], WAMR, f"{WAMR}--multi-tier-jit"],
    ],
}

PERF_LOG_PROC_NAME_IDX = 0
PERF_LOG_TIMESTAMP_IDX = 3
PERF_LOG_PROBE_IDX = 4


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
    # subprocess.run(command.split())


def profile_time_in_one_case(runtime, execution_cmd, perf_record_cmd, probes, perf_log_path):
    probes_num = len(probes)
    # start perf record cmd, different runtimes have different probe
    perf_record = subprocess.Popen(perf_record_cmd.split())
    sleep(2)

    def kill_perf():
        f = os.popen("ps aux | grep 'perf record' | awk '{print $2}'")
        res = f.read().split('\n')
        os.popen(f"sudo kill {' '.join(res)}")

    try:
        run(execution_cmd)
    except Exception as e:
        # stop perf record cmd
        kill_perf()
        print("error occur!", e)
        return

    # stop perf record cmd
    sleep(1)
    kill_perf()
    sleep(1)
    
    # run perf script to get the perf log, and save in perf_log_path
    subprocess.run(f"sudo perf script --ns -f".split(), stdout=open(perf_log_path,'w'))
    sleep(1)

    # extract 5 timestamp from perf log, compute the above time range
    timestamps = []
    with open(perf_log_path, 'r') as f:
        i = 0
        line = f.readline()
        exit_time = None
        while line is not None and line != '':
            line = line.strip()
            items = line.split()

            if items[PERF_LOG_PROC_NAME_IDX] != runtime or items[PERF_LOG_PROBE_IDX][:-1] != probes[i]:
                line = f.readline()
                continue
            
            if i == probes_num - 1:
                exit_time = float(items[PERF_LOG_TIMESTAMP_IDX][:-1])
            else:
                timestamps.append(float(items[PERF_LOG_TIMESTAMP_IDX][:-1]))
                i += 1
            line = f.readline()
            
    if i < probes_num - 1 or exit_time is None:
        print("Something wrong....\n", i, " != ", probes_num)
        return
    
    timestamps.append(exit_time)
    print(timestamps)

    range_compute = lambda x, y: (x * TIME_UNIT - y * TIME_UNIT)
    time_range = [range_compute(timestamps[probes_num - 1], timestamps[0])]
    i = 0
    if probes_num > 2:
        while i < probes_num - 1:
            time_range.append(range_compute(timestamps[i+1], timestamps[i]))
            i += 1
    print(time_range, "\n\n")
    return time_range


def profile_time_during_execution(wasm_target, out_dir, source_perf_log_dir):
    for runtime in RUNTIMES:
        if runtime not in RUNTIME_CMDS:
            continue
        wasm_aot_target = os.path.join(os.path.dirname(wasm_target), 
            os.path.splitext(os.path.basename(wasm_target))[0] + '_wasmedge_aot.wasm')
        for runtime_cmd in RUNTIME_CMDS[runtime]:
            execute_command = runtime_cmd[0].format(runtime=RUNTIME_PATH[runtime], wasm=wasm_target, wasm_aot=wasm_aot_target)
            print(execute_command, runtime_cmd)
            
            source_runtime_perf_log_dir = os.path.join(source_perf_log_dir, runtime_cmd[4])
            os.makedirs(source_runtime_perf_log_dir, exist_ok=True)
            start_time = []
            code_loaded_time = []
            code_execution_time = []
            aot_compilation_time = []
            total_time = []
            for i in range(TEST_TIMES):
                if runtime == WASMER:
                    run(f"{RUNTIME_PATH[runtime]} cache clean")
                try:            
                    tmp = profile_time_in_one_case(runtime_cmd[3], execute_command, runtime_cmd[1], runtime_cmd[2], os.path.join(source_runtime_perf_log_dir, f"log_{i}.txt"))
                    if len(tmp) == 4:
                        total_time.append(tmp[0])
                        start_time.append(tmp[1])
                        code_loaded_time.append(tmp[2])
                        code_execution_time.append(tmp[3])
                    elif len(tmp) == 1:
                        aot_compilation_time.append(tmp[0])
                    else:
                        raise Exception("The length of the perf result is wrong")
                except func_timeout.exceptions.FunctionTimedOut as e:
                    print(e)
                    break
                sleep(2)
            
            target_name = os.path.basename(wasm_target)
            def write_res_to_csv(time_tag, arr):
                if len(arr) == 0:
                    return
                avg_time = mean(arr)
                data = [time_tag, runtime_cmd[4], target_name, avg_time]
                execution_time_out_dir = os.path.join(out_dir, time_tag)
                os.makedirs(execution_time_out_dir, exist_ok=True)
                out_file = os.path.join(execution_time_out_dir, f'{time_tag}_' + runtime_cmd[4] + '.csv')
                write_csv(data, out_file)
            
            write_res_to_csv("start_time", start_time)
            write_res_to_csv("code_loaded_time", code_loaded_time)
            write_res_to_csv("code_execution_time", code_execution_time)
            write_res_to_csv("aot_compilation_time", aot_compilation_time)
            write_res_to_csv("total_time", total_time)
            print("================\n\n")



def profile_by_source(native_target, wasm_target, out_dir, source_perf_log_dir):
    # profile_bin_size(native_target, wasm_target, out_dir)
    profile_time_during_execution(wasm_target, out_dir, source_perf_log_dir)


def profile_by_benchmark(benchmark):
    print('Profile ' + benchmark + ':')
    benchmark_dir = os.path.join(TARGET_DIR, op_level, benchmark)
    native_dir = os.path.join(benchmark_dir, COMPILE_TARGET_NATIVE)
    wasm_dir = os.path.join(benchmark_dir, COMPILE_TARGET_WASM)
    benchmark_out_dir = os.path.join(PROFILIGDATA_DIR, op_level, benchmark)
    os.makedirs(benchmark_out_dir, exist_ok=True)

    now_perf_log_dir = os.path.join(PERF_LOG_DIR, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), op_level, benchmark)
    os.makedirs(now_perf_log_dir, exist_ok=True)

    native_targets = os.listdir(native_dir)
    wasm_targets = os.listdir(wasm_dir)
    for native_target_name in native_targets:
        wasm_target_name = native_target_name + TARGET_SUFFIX[COMPILE_TARGET_WASM]
        if wasm_target_name in wasm_targets:
            native_target_path = os.path.join(native_dir, native_target_name)
            wasm_target_path = os.path.join(wasm_dir, wasm_target_name)
            now_perf_log_for_target_dir = os.path.join(now_perf_log_dir, native_target_name)
            os.makedirs(now_perf_log_for_target_dir, exist_ok=True)
            profile_by_source(native_target_path, wasm_target_path, benchmark_out_dir, now_perf_log_for_target_dir)


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
        # profile_by_benchmark(ADOBECPP)
        # profile_by_benchmark(BENCHMARKGAME)

        # 3.29 test
        # profile_by_benchmark(COYOTEBENCH)
        # profile_by_benchmark(DHRYSTONE) # empty
        # profile_by_benchmark(LINPACK)
        # profile_by_benchmark(MCGILL)
        
        # 3.30 test
        # profile_by_benchmark(MISC)
        # profile_by_benchmark(MISCCPP)

        # 3.31 test
        # profile_by_benchmark(MISCCPPEH) # empty
        profile_by_benchmark(POLYBENCH)
        profile_by_benchmark(SHOOTOUT)
        profile_by_benchmark(SHOOTOUTCPP)
        # profile_by_benchmark(SMALLPT) # empty
        profile_by_benchmark(STANDFORD)


if __name__=="__main__":
    main()
