#!/bin/bash

trap 'echo interrupted; exit 1' INT

## Llama3.X
## Qwen2.5-Coder

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Meta-Llama-3-8B-Instruct guidance True
sh constrained_runner.sh constraints meta-llama/Meta-Llama-3-8B-Instruct guidance
sh constrained_runner.sh without_constraints meta-llama/Meta-Llama-3-8B-Instruct hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-7B-Instruct guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-7B-Instruct guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-7B-Instruct hf

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-3B-Instruct guidance True
sh constrained_runner.sh constraints meta-llama/Llama-3.2-3B-Instruct guidance
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-3B-Instruct hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-3B-Instruct guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-3B-Instruct guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-3B-Instruct hf

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-1B-Instruct guidance True
sh constrained_runner.sh constraints meta-llama/Llama-3.2-1B-Instruct guidance
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-1B-Instruct hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-1.5B-Instruct guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-1.5B-Instruct guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-1.5B-Instruct hf
