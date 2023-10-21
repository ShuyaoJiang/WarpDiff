# WarpDiff: Differential Testing of Wasm Runtime Performance

## Usage

### Step 0: Environment and Data Preparation
* **Runtime Installation:** Install Wasm runtimes on your local environment for testing, including [Wasmer](https://github.com/wasmerio/wasmer), [Wasmtime](https://github.com/bytecodealliance/wasmtime), [Wasm3](https://github.com/wasm3/wasm3), [WasmEdge](https://github.com/WasmEdge/WasmEdge), and [WAMR](https://github.com/bytecodealliance/wasm-micro-runtime).
* **Compiler Installation:** Install [Emscripten](https://emscripten.org).
* **Dataset:** Download [llvm-test-suite](https://github.com/llvm/llvm-test-suite).
* **Programming Language:** Python 3.9.


### Step 1: Test Case Compilation
```
python3 compile_to_target.py O2
```  

### Step 2: Runtime Performance Profiling
To obtain the total running time: 
```
python3 runtime_profiling_total.py O2
```

To obtain the running time for three stages: 
```
cd runtime_profiling_three_stages
python3 runtime_profiling.py O2
```


### Step 3: Differential Testing on Runtime Performance Data
```
python3 analyze_performance.py
```


## Publication
[Revealing Performance Issues in Server-side WebAssembly Runtimes via Differential Testing](https://arxiv.org/abs/2309.12167).  
Shuyao Jiang, Ruiying Zeng, Zihao Rao, Jiazhen Gu, Yangfan Zhou, and Michael R. Lyu.  
In *Proceedings of the 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)*, September, 2023. 