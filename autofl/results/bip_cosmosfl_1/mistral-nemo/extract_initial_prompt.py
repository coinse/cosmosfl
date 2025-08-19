import json
import os

if __name__ == "__main__":
    prompt_dict = dict()
    for log_file in os.listdir('.'):
        bug_id = log_file[4:-5]
        if not log_file.endswith('.json'):
            continue
        with open(log_file) as f:
            messages = json.load(f)['messages']
        if len(messages) < 2:
            print(bug_id)
        else:
            initial_prompt = f"{messages[0]['content']}\n{messages[1]['content']}"
            prompt_dict[bug_id] = initial_prompt

    with open('prompts.json', 'w') as f:
        json.dump(dict(sorted(prompt_dict.items())), f, indent=4)
