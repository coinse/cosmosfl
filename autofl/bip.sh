sh runner.sh bip_cosmosfl_ 10 bugsinpy mistral-nemo prompts/system_msg_expbug_with_funcs_bip.txt
sh runner.sh bip_cosmosfl_ 10 bugsinpy qwen2.5-coder prompts/system_msg_expbug_with_funcs_bip.txt
sh runner.sh bip_cosmosfl_ 10 bugsinpy llama3 prompts/system_msg_expbug_with_funcs_bip.txt
sh runner.sh bip_cosmosfl_ 10 bugsinpy llama3.1 prompts/system_msg_expbug_with_funcs_bip.txt

python compute_score.py results/bip_cosmosfl_*/llama3 -l python -a -v -o bip_llama3_results_R10.json
python compute_score.py results/bip_cosmosfl_*/llama3.1 -l python -a -v -o bip_llama3.1_results_R10.json
python compute_score.py results/bip_cosmosfl_*/mistral-nemo -l python -a -v -o bip_mistral-nemo_results_R10.json
python compute_score.py results/bip_cosmosfl_*/qwen2.5-coder -l python -a -v -o bip_qwen2.5-coder_results_R10.json
