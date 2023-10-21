wasmer-perf-record:
	sudo perf record -e probe_wasmer:abs_591f00 -e probe_wasmer:abs_8d5ee0 -e probe_wasmer:abs_6d5cb0 -e sched:sched_process_exec -e sched:sched_process_exit -a -T

wasmtime-perf-record:
	sudo perf record -e probe_wasmtime:abs_2e73c0 -e probe_wasmtime:abs_398ce0 -e sched:sched_process_exec -e sched:sched_process_exit -a -T

wasm3-perf-record:
	sudo perf record -e probe_wasm3:main -e probe_wasm3:repl_call -e sched:sched_process_exec -e sched:sched_process_exit -a -T

wasmedgec-perf-record:
	sudo perf record -e probe_libwasmedge:abs_15eda0 -e probe_libwasmedge:abs_167e90 -a -T

wasmedge-perf-record:
	sudo perf record -e probe_libwasmedge:abs_59710 -e probe_libwasmedge:abs_d4de0 -e sched:sched_process_exec -e sched:sched_process_exit -a -T

wamrc-perf-record:
	sudo perf record -e probe_wamrc:abs_3b4bc0 -e probe_wamrc:abs_3b9af0

iwasm-perf-record:
	sudo perf record -e sched:sched_process_exec -e probe_iwasm:abs_8850 -e probe_iwasm:abs_e2d0 -e probe_iwasm:abs_170f0 -e sched:sched_process_exit -a -T

iwasm-jit-perf-record:
	sudo perf record -e sched:sched_process_exec -e probe_iwasm:abs_1c0c00 -e probe_iwasm:abs_23e350 -e sched:sched_process_exit -a -T