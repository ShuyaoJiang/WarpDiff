# WarpDiff: Differential Testing of Wasm Runtime Performance Issues

## Step 0: Environment and Data Preparation
* **Runtime Installation:** Install Wasm runtimes on your local environment for testing, including Wasmer, Wasmtime, Wasm3, WasmEdge, and WAMR.
* **Compiler Installation:** Install Emscripten via https://emscripten.org.
* **Dataset:** Download `llvm-test-suite` via https://github.com/llvm/llvm-test-suite.
* **Programming Language:** Python 3.9.


## Step 1: Test Case Compilation
* `$ python3 compile_to_target.py O2`
  

## Step 2: Runtime Performance Profiling
* To obtain the total running time: `$ python3 runtime_profiling_total.py O2`
* To obtain the running time for three stages: 
  * `$ cd runtime_profiling_three_stages`
  * `$ python3 runtime_profiling.py O2`


## Step 3: Differential Testing on Runtime Performance Data
* `$ python3 analyze_performance.py`