import json
import os

if __name__ == "__main__":
    model = 'qwen2.5-coder' 
    benchmark_prefix = 'bip_cosmosfl'  # 'd4j_autofl_eol' 

    prompt_dict = dict()
    for i in range(1, 11):
        log_dir = f'results/{benchmark_prefix}_{i}/{model}'
        for log_file in os.listdir(log_dir):
            bug_id = log_file[4:-5]
            if not log_file.endswith('.json') or not log_file.startswith('XFL'):
                continue
            with open(f'{log_dir}/{log_file}') as f:
                data = json.load(f)
                messages = data['messages']
            if len(messages) < 2:
                continue
            if bug_id not in prompt_dict:
                prompt_dict[bug_id] = dict()
            buggy_methods = data['buggy_methods']
            is_correct = type(buggy_methods) == dict and buggy_methods and any([item['is_found'] for item in buggy_methods.values()])
            trajectory = '\n'.join([f'{msg["role"]}: {msg["content"]}' for msg in messages])
            if is_correct:
                prompt_dict[bug_id]['found'] = trajectory
            else:
                prompt_dict[bug_id]['failed'] = trajectory

    filtered_items = list()
    for bug_id, trajectories in prompt_dict.items():
        if len(trajectories) == 2:
            filtered_items.append((bug_id, trajectories))

    with open(f'trajectories/{benchmark_prefix.split("_")[0]}/{model}_trajectories.json', 'w') as f:
        json.dump(dict(sorted(filtered_items)), f, indent=4)
