#!/bin/bash

trap 'echo interrupted; exit 1' INT

# last three flags stand for {block_repetitions} / {force_selection} / {force_tool_calls}

### defects4j

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance true false false
sh constrained_runner.sh no_repeat_force_select meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance true true false
sh constrained_runner.sh constraints meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance false false false
sh constrained_runner.sh force_select meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance false true false
sh constrained_runner.sh force_tool_call meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance false false true 
sh constrained_runner.sh force_both meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance false true true 
sh constrained_runner.sh no_repeat_force_both meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance true true true 
sh constrained_runner.sh without_constraints meta-llama/Meta-Llama-3-8B-Instruct defects4j hf false false false

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance true false false
sh constrained_runner.sh no_repeat_force_select Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance true true false
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance false false false
sh constrained_runner.sh force_select Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance false true false
sh constrained_runner.sh force_tool_call Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance false false true
sh constrained_runner.sh force_both Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance false true true
sh constrained_runner.sh no_repeat_force_both Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance true true true
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-7B-Instruct defects4j hf false false false

sh constrained_runner.sh constraints_with_no_repetitions google/gemma-2-9b-it defects4j guidance true false false
sh constrained_runner.sh no_repeat_force_select google/gemma-2-9b-it defects4j guidance true true false
sh constrained_runner.sh constraints google/gemma-2-9b-it defects4j guidance false false false
sh constrained_runner.sh force_select google/gemma-2-9b-it defects4j guidance false true false
sh constrained_runner.sh force_tool_call google/gemma-2-9b-it defects4j guidance false false true
sh constrained_runner.sh force_both google/gemma-2-9b-it defects4j guidance false true true
sh constrained_runner.sh no_repeat_force_both google/gemma-2-9b-it defects4j guidance true true true
sh constrained_runner.sh without_constraints google/gemma-2-9b-it defects4j hf false false false

sh constrained_runner.sh constraints_with_no_repetitions microsoft/Phi-3-mini-4k-instruct defects4j guidance true false false
sh constrained_runner.sh no_repeat_force_select microsoft/Phi-3-mini-4k-instruct defects4j guidance true true false
sh constrained_runner.sh constraints microsoft/Phi-3-mini-4k-instruct defects4j guidance false false false
sh constrained_runner.sh force_select microsoft/Phi-3-mini-4k-instruct defects4j guidance false true false
sh constrained_runner.sh force_tool_call microsoft/Phi-3-mini-4k-instruct defects4j guidance false false true
sh constrained_runner.sh force_both microsoft/Phi-3-mini-4k-instruct defects4j guidance false true true
sh constrained_runner.sh no_repeat_force_both microsoft/Phi-3-mini-4k-instruct defects4j guidance true true true
sh constrained_runner.sh without_constraints microsoft/Phi-3-mini-4k-instruct defects4j hf false false false

