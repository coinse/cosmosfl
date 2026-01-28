import json
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

# for defects4j
FUNCTION_INDICES = {'get_failing_tests_covered_classes': 0, 'get_failing_tests_covered_methods_for_class': 1,
        'get_code_snippet': 2, 'get_comments': 3}
FUNCTION_COLORS = ['039dff', 'ABDEFF', 'd62728', 'EB9394', '000000']
FUNCTION_LABELS = ['class_cov', 'method_cov', 'snippet', 'comments', 'undefined']
MAX_STEPS=11

def file2bug(json_file):
    if not json_file.endswith(".json"):
        return None
    try:
        return os.path.basename(json_file).removeprefix('XFL-').removesuffix('.json')
    except:
        return None

def count_function_calls_by_step(calls_by_step, messages):
    index = 0
    for m in messages:
        if m['role'] == 'assistant' and 'function_call' in m and index < MAX_STEPS:
            if not m['function_call']['name'] in calls_by_step:
                calls_by_step[m['function_call']['name']] = [0] * MAX_STEPS
            calls_by_step[m['function_call']['name']][index] += 1
            index += 1 

def count_failing_and_total_calls(failing_calls, total_calls, messages):
    total = 0
    fail = 0
    for i in range(len(messages) - 1):
        m = messages[i]
        next_m = messages[i + 1]
        if m['role'] == 'assistant' and 'function_call' in m:
            if next_m['role'] != 'function':
                continue 
            if not m['function_call']['name'] in total_calls:
                total_calls[m['function_call']['name']] = 0
                failing_calls[m['function_call']['name']] = 0
            if 'error_message' in next_m['content']:
                failing_calls[m['function_call']['name']] += 1
                fail += 1
            total_calls[m['function_call']['name']] += 1
            total += 1
    return total, fail 

def function_call_to_str(function_call):
    return function_call['name'] + function_call['arguments']

def is_found(log):
    return isinstance(log['buggy_methods'], dict) and any([method['is_found'] for method in log['buggy_methods'].values()])

def count_repeated_calls(repeated_calls, messages, is_found):
    previous_calls = {}
    for m in messages:
        if m['role'] == 'assistant' and 'function_call' in m:
            if not function_call_to_str(m['function_call']) in previous_calls:
                previous_calls[function_call_to_str(m['function_call'])] = 0
            previous_calls[function_call_to_str(m['function_call'])] += 1
    repeated_calls[is_found].append(sum([count - 1 for count in previous_calls.values()]) / sum(previous_calls.values()))
    return sum([count - 1 for count in previous_calls.values()])

def analyze_patterns(result_dirs, project=None):
    execution_time = []
    num_steps = []
    num_suspicious_methods = []
    num_total = []
    num_fail = []
    num_repeat = []

    calls_by_step = {}
    total_calls = {}
    failing_calls = {}
    repeated_calls = {True: [], False: []}

    for result_dir in result_dirs:
        file_iterator = sorted([f for f in os.listdir(result_dir) if f.endswith('.json')], key=lambda fname: int(fname.split('_')[1].split('.')[0]))
        print(f"Processing {result_dir}...")
        for fname in file_iterator:
            bug_name = file2bug(fname)
            if bug_name is None:
                continue            
            if project and not bug_name.startswith(project):
                continue

            fpath = os.path.join(result_dir, fname)
            with open(fpath, 'r') as f:
                autofl_data = json.load(f)
            
            valid_messages = autofl_data["messages"]
            if isinstance(autofl_data['buggy_methods'], dict): # filter out invalid runs
                execution_time.append(autofl_data['time_taken'])
                num_steps.append(sum([1 for m in valid_messages if m['role'] == 'assistant']) - 1) # Exclude step 0 function call
                final_message = valid_messages[-1]['content']
                num_suspicious_methods.append(len(final_message.splitlines()) if final_message else 0)

            count_function_calls_by_step(calls_by_step, valid_messages)
            total, fail = count_failing_and_total_calls(failing_calls, total_calls, valid_messages)
            repeat = count_repeated_calls(repeated_calls, valid_messages, is_found(autofl_data))

            num_total.append(total)
            num_fail.append(fail)
            num_repeat.append(repeat)

    repeated_calls['num_found'] = len(repeated_calls[True])
    repeated_calls['mean_of_found'] = sum(repeated_calls[True]) / len(repeated_calls[True]) if len(repeated_calls[True]) else 0.0
    repeated_calls['num_unfound'] = len(repeated_calls[False])
    repeated_calls['mean_of_unfound'] = sum(repeated_calls[False]) / len(repeated_calls[False]) if len(repeated_calls[False]) else 0.0


    print(f"Valid Runs: {len(execution_time)}")
    print(f"Suspicious methods count statistics: {np.mean(num_suspicious_methods):.2f} ({np.std(num_suspicious_methods):.2f})")
    print(f"Execution time statistics: {np.mean(execution_time):.2f} ({np.std(execution_time):.2f})")
    print(f"Total call statistics: {np.mean(num_total):.2f} ({np.std(num_total):.2f})")
    print(f"Failed call statistics: {np.mean(num_fail):.2f} ({np.std(num_fail):.2f})")
    print(f"Repeated call statistics: {np.mean(num_repeat):.2f} ({np.std(num_repeat):.2f})")
    print(f"Step count statistics: {np.mean(num_steps):.2f} ({np.std(num_steps):.2f})")

    return calls_by_step, total_calls, failing_calls, repeated_calls

def plot_call_distribution(data, total_runs, path):
    plt.style.use('../style/style-formal.mplstyle')

    labels = list(data.keys())
   
    undefined_functions = [l for l in labels if l not in FUNCTION_INDICES]
    labels = sorted([l for l in labels if l in FUNCTION_INDICES], key=lambda label: FUNCTION_INDICES[label])
    values = [data[label] for label in labels]

    if undefined_functions:
        undefined_calls = [0] * MAX_STEPS
        for func in undefined_functions:
            to_add = data[func]
            undefined_calls = [undefined_calls[i] + to_add[i] for i in range(MAX_STEPS)]
        values.append(undefined_calls)
        labels.append('undefined_functions')

    values = np.array(values) / total_runs
    cumulative_values = np.cumsum(values, axis=0)
    y = np.arange(len(data[labels[0]]))
    
    _, ax = plt.subplots(figsize=(5, 2))
    
    for i in range(len(labels)):
        try:
            label_index = FUNCTION_INDICES[labels[i]]
        except:
            label_index = 4
        if i == 0:
            ax.barh(y, values[i], label=FUNCTION_LABELS[label_index], color=f'#{FUNCTION_COLORS[label_index]}', tick_label=[f'Step {i}' for i in range(MAX_STEPS)])
        else:
            ax.barh(y, values[i], left=cumulative_values[i-1], label=FUNCTION_LABELS[label_index], color=f'#{FUNCTION_COLORS[label_index]}', tick_label=[f'Step {i}' for i in range(MAX_STEPS)])
    
    ax.set_xlabel('Proportion of Runs')
    ax.set_title('Function Call Distribution at Each Step')
    ax.legend()
    
    ax.set_ylim(len(data[labels[0]]) - 0.5, -0.5)
    plt.savefig(path, bbox_inches='tight')

def plot_failing_calls(total_calls, failing_calls, total_runs, path):
    functions = sorted([f for f in list(total_calls.keys()) if f in FUNCTION_INDICES], key=lambda func: FUNCTION_INDICES[func])
    total_values = [total_calls[func] / total_runs for func in functions]
    failing_values = [failing_calls[func] / total_runs for func in functions]

    translated_labels = [FUNCTION_LABELS[FUNCTION_INDICES[f]] for f in functions]

    x = np.arange(len(functions))

    plt.figure(figsize=(6, 8))
    plt.bar(x, total_values, width=0.8, label='Valid Calls', color='limegreen', alpha=1.0)
    plt.bar(x, failing_values, width=0.8, label='Invalid Calls', color='salmon', alpha=1.0)

    plt.ylabel('Number of Calls', fontsize=14)
    # plt.title('Total Calls vs Invalid Calls per Function', fontsize=16)
    plt.xticks(x, translated_labels)
    # plt.legend(prop={'size': 16})

    plt.savefig(path, bbox_inches='tight')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('result_dirs', nargs="+", type=str)
    parser.add_argument('--output', '-o', type=str, default="scores.json")
    parser.add_argument('--project', '-p', type=str, default=None)
    args = parser.parse_args()

    calls_by_step, total, failing, repeated = analyze_patterns(args.result_dirs, args.project)

    total_runs = calls_by_step[list(calls_by_step.keys())[0]][0]
    # plot_call_distribution(calls_by_step, total_runs, f'{args.output}_distribution.png')
    # plot_failing_calls(total, failing, total_runs, f'{args.output}_failing_rate.png')

    # with open(f'{args.output}.json', "w") as f:
    #     json.dump({'total': total, 'failing': failing, 'steps': calls_by_step, 'repetition': repeated}, f, indent=4)
