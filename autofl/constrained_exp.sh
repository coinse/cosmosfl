#!/bin/bash

trap 'echo interrupted; exit 1' INT

## Llama3.X
## Qwen2.5-Coder

### defects4j

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance True
sh constrained_runner.sh constraints meta-llama/Meta-Llama-3-8B-Instruct defects4j guidance
sh constrained_runner.sh without_constraints meta-llama/Meta-Llama-3-8B-Instruct defects4j hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-7B-Instruct defects4j guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-7B-Instruct defects4j hf

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-3B-Instruct defects4j guidance True
sh constrained_runner.sh constraints meta-llama/Llama-3.2-3B-Instruct defects4j guidance
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-3B-Instruct defects4j hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-3B-Instruct defects4j guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-3B-Instruct defects4j guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-3B-Instruct defects4j hf

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-1B-Instruct defects4j guidance True
sh constrained_runner.sh constraints meta-llama/Llama-3.2-1B-Instruct defects4j guidance
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-1B-Instruct defects4j hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-1.5B-Instruct defects4j hf

### bugsinpy

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Meta-Llama-3-8B-Instruct bugsinpy guidance True
sh constrained_runner.sh constraints meta-llama/Meta-Llama-3-8B-Instruct bugsinpy guidance
sh constrained_runner.sh without_constraints meta-llama/Meta-Llama-3-8B-Instruct bugsinpy hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-7B-Instruct bugsinpy guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-7B-Instruct bugsinpy guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-7B-Instruct bugsinpy hf

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-3B-Instruct bugsinpy guidance True
sh constrained_runner.sh constraints meta-llama/Llama-3.2-3B-Instruct bugsinpy guidance
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-3B-Instruct bugsinpy hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-3B-Instruct bugsinpy guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-3B-Instruct bugsinpy guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-3B-Instruct bugsinpy hf

sh constrained_runner.sh constraints_with_no_repetitions meta-llama/Llama-3.2-1B-Instruct bugsinpy guidance True
sh constrained_runner.sh constraints meta-llama/Llama-3.2-1B-Instruct bugsinpy guidance
sh constrained_runner.sh without_constraints meta-llama/Llama-3.2-1B-Instruct bugsinpy hf

sh constrained_runner.sh constraints_with_no_repetitions Qwen/Qwen2.5-Coder-1.5B-Instruct bugsinpy guidance True
sh constrained_runner.sh constraints Qwen/Qwen2.5-Coder-1.5B-Instruct bugsinpy guidance
sh constrained_runner.sh without_constraints Qwen/Qwen2.5-Coder-1.5B-Instruct bugsinpy hf