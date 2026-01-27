LABEL_PREFIX=$1
if [ -z  "$1" ]; then
    echo "Please provide an experiment label."
    exit 0
fi

MODEL=$2
ENGINE=$3
BLOCK_REPETITIONS=$4

BLOCK_FLAG=""
if [ -n "$BLOCK_REPETITIONS" ]; then
    BLOCK_FLAG="--block_repetitions"
fi

DATASET="defects4j"
PROMPT_FILE="prompts/system_msg_expbug_with_funcs_d4j.txt"
DATA_DIR=./data/${DATASET}/
BUDGET="10"
NUM_TESTS="1"

trap 'echo interrupted; exit 1' INT

label="${LABEL_PREFIX}"
save_dir="results/constrained_autofl/${label}/${MODEL}"
mkdir -p "${save_dir}"
bug_list=$(ls -d ${DATA_DIR}/*/ | xargs -n1 basename)
for bugname in $bug_list; do
    save_file="${save_dir}/XFL-${bugname}.json"
    if [ -f ${save_file} ]; then
        echo "${save_file} exists"
        continue
    fi
    if [ -f "${DATA_DIR}/${bugname}/snippet.json" ]; then
        cmd="python autofl.py -m ${MODEL} --engine ${ENGINE} -b ${bugname} -p ${PROMPT_FILE} -o ${save_file} --max_budget ${BUDGET} --max_num_tests ${NUM_TESTS} --show_line_number --postprocess_test_snippet --allow_multi_predictions --test_offset 0 ${BLOCK_FLAG}" 
        # measure_power_consumption option only works when there are both pynvml module and GPU(s), disable otherwise
        echo ${cmd}
        timeout 3m ${cmd}
    fi
done
