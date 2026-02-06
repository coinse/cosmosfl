#!/bin/bash

trap 'echo interrupted; exit 1' INT

## Llama3.X
## Qwen2.5-Coder

### defects4j

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance true true
sh constrained_runner.sh constraints meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance false false
sh constrained_runner.sh force_select meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance false true 
sh constrained_runner.sh without_constraints meta-llama/Meta-Llama-3-8B-Instruct defects4j hf false false

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance true true
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance false false
sh constrained_runner.sh force_select Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance false true 
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-7B-Instruct defects4j hf false false

sh constrained_runner.sh constraints_with_no_repetitions google/gemma-2-9b-it defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select google/gemma-2-9b-it defects4j guidance true true
sh constrained_runner.sh constraints google/gemma-2-9b-it defects4j guidance false false
sh constrained_runner.sh force_select google/gemma-2-9b-it defects4j guidance false true 
sh constrained_runner.sh without_constraints google/gemma-2-9b-it defects4j hf false false

sh constrained_runner.sh constraints_with_no_repetitions microsoft/Phi-3-mini-4k-instruct defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select microsoft/Phi-3-mini-4k-instruct defects4j guidance true true
sh constrained_runner.sh constraints microsoft/Phi-3-mini-4k-instruct defects4j guidance false false
sh constrained_runner.sh force_select microsoft/Phi-3-mini-4k-instruct defects4j guidance false true 
sh constrained_runner.sh without_constraints microsoft/Phi-3-mini-4k-instruct defects4j hf false false

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-3B-Instruct defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select meta-llama/Llama-3.2-3B-Instruct defects4j guidance true true
sh constrained_runner.sh constraints meta-llama/Llama-3.2-3B-Instruct defects4j guidance false false
sh constrained_runner.sh force_select meta-llama/Llama-3.2-3B-Instruct defects4j guidance false true 
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-3B-Instruct defects4j hf false false

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-3B-Instruct defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select Qwen/Qwen2.5-Coder-3B-Instruct defects4j guidance true true
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-3B-Instruct defects4j guidance false false
sh constrained_runner.sh force_select Qwen/Qwen2.5-Coder-3B-Instruct defects4j guidance false true
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-3B-Instruct defects4j hf false false

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-1B-Instruct defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select meta-llama/Llama-3.2-1B-Instruct defects4j guidance true true
sh constrained_runner.sh constraints meta-llama/Llama-3.2-1B-Instruct defects4j guidance false false
sh constrained_runner.sh force_select meta-llama/Llama-3.2-1B-Instruct defects4j guidance false true 
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-1B-Instruct defects4j hf false false

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j guidance true false
sh constrained_runner.sh no_repeat_force_select Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j guidance true true
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j guidance false false
sh constrained_runner.sh force_select Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j guidance false true
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j hf false false
