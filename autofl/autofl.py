import json
import time
import argparse
import traceback
import hashlib
from copy import deepcopy
from lib.repo_interface import get_repo_interface

import sys
sys.path.insert(0, '..')
from utils import llm_utils

RESULT_DIR = './results/'

class AutoDebugger(llm_utils.OllamaEngine):
    def __init__(self, endpoint, bug_name, model_type, system_file, test_offset=None,
            max_num_tests=None, allow_multi_predictions=False,
            summarize_messages=False, debug=False, **ri_kwargs):
        super().__init__(endpoint, model_type)
        self._bug_name = bug_name
        self._dataset = self._get_dataset(self._bug_name)
        self._ri = get_repo_interface(bug_name, **ri_kwargs)
        self._test_offset = test_offset
        self._max_num_tests = max_num_tests
        self._allow_multi_predictions = allow_multi_predictions
        self._summarize_messages = summarize_messages
        self._system_file = system_file
        self._debug = debug

    def _get_dataset(self, bug_name):
        def _name_matches_proj_list(name, proj_list):
            return any(name.lower() == proj_name.lower()
                    for proj_name in proj_list)
        d4j_projects = [
            'Chart',
            'Cli',
            'Closure',
            'Codec',
            'Collections',
            'Compress',
            'Csv',
            'Gson',
            'JacksonCore',
            'JacksonDatabind',
            'JacksonXml',
            'Jsoup',
            'JxPath',
            'Lang',
            'Math',
            'Mockito',
            'Time',
        ]

        bip_projects = [
            'ansible',
            'cookiecutter',
            'pysnooper',
            'spacy',
            'sanic',
            'httpie',
            'keras',
            'matplotlib',
            'thefuck',
            'pandas',
            'black',
            'scrapy',
            'luigi',
            'fastapi',
            'tornado',
            'tqdm',
            'youtube-dl',
        ]

        pid, vid = bug_name.split('_')
        if _name_matches_proj_list(pid, d4j_projects):
            return "defects4j"
        elif _name_matches_proj_list(pid, bip_projects):
            return "bugsinpy"
        else:
            raise ValueError(f"Could not match the project for {bug_name}")

            

    def _replace_last_with_memo(self, memo):
        self.messages = self.messages[:-1] # replace recent two queries with memo
        self.messages.append({'role': 'assistant', 'content': 'Summary: ' + memo})

    def _append_to_messages(self, message):
        # to easily control debug behavior
        if self._debug:
            print(message)
        self.messages.append(message)

    @property
    def _system_message(self):
        with open(self._system_file) as f:
            system_message = f.read().strip()
        if self._allow_multi_predictions:
            system_message += "\n\nAfter providing this diagnosis, you will be prompted to suggest which methods would be the best locations to be fixed. The answers should be in the form of `ClassName.MethodName(ArgType1, ArgType2, ...)` without commentary (one per line), as your answer will be automatically processed before finally being presented to the user."
        else:
            system_message += "\n\nAfter providing this diagnosis, you will be prompted to suggest which method would be the best location to be fixed. You will provide a single answer, in the form of `ClassName.MethodName(ArgType1, ArgType2, ...)`, as your answer will be automatically processed before finally being presented to the user."
        return system_message

    def _init_interaction_records(self):
        self._mid_map = {} # md5_hash -> mid (message id)
        self._message_map = {} # mid -> message
        self._interaction_records = [] # list of dict

    def _append_to_interaction_records(self, prompt_messages, response_message):
        def _save_message_and_get_mid(message):
            s = json.dumps(message).encode('utf-8')
            md5_hash = hashlib.md5(s).digest()
            if md5_hash not in self._mid_map:
                self._mid_map[md5_hash] = f"m{len(self._mid_map) + 1}"
                self._message_map[self._mid_map[md5_hash]] = deepcopy(message)
            return self._mid_map[md5_hash]

        self._interaction_records.append({
            "prompt_messages": [_save_message_and_get_mid(m) for m in prompt_messages],
            "response_message": _save_message_and_get_mid(response_message)
        })

    def startup(self):
        self._init_interaction_records()
        self.messages = []

        self._append_to_messages({'role': 'system', 'content': self._system_message})

        fail_test_signatures = [
            signature for signature in self._ri.failing_test_signatures
            if self._ri.get_test_snippet(signature) is not None
        ]

        if self._test_offset is not None:
            # rotate list
            offset = self._test_offset % len(fail_test_signatures)
            fail_test_signatures = fail_test_signatures[offset:] + fail_test_signatures[:offset]

        if self._max_num_tests is not None:
            fail_test_signatures = fail_test_signatures[:self._max_num_tests]

        if not fail_test_signatures:
            raise ValueError(f'Could not find test snippet for bug {self._bug_name}')

        user_message = f"The test `{fail_test_signatures}` failed.\n"
        test_snippets = "\n\n".join(self._ri.get_test_snippet(signature).rstrip() for signature in fail_test_signatures)
        user_message += f"The test looks like:\n\n```{self._ri.language}\n{test_snippets}\n```\n\n"

        failing_traces = "\n\n".join(self._ri.get_fail_info(signature, minimize=True).rstrip() for signature in fail_test_signatures)
        user_message += f"It failed with the following error message and call stack:\n\n```\n{failing_traces}\n```\n\n"

        user_message += f'Start by calling the `{self._ri.initial_coverage_getter}` function.'

        self._append_to_messages({
            'role': 'user',
            'content': user_message,
        })
        
        # no-LLM call of first instruction (LLM always calls this anyway)
        self._append_to_messages({
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": self._ri.initial_coverage_getter,
                "arguments": "{}"
            }
        })
        self._append_to_messages({
            "role": "function",
            "name": self._ri.initial_coverage_getter,
            "content": json.dumps(self._ri.fname2func[self._ri.initial_coverage_getter]())
        })

    def call_function(self, response_message):
        function_name = response_message["function_call"]["name"]
        function_to_call = self._ri.fname2func[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        try:
            function_response = function_to_call(**function_args)
        except TypeError as e:
            return function_name, str(e) 
        return function_name, function_response

    def step(self, function_call_mode="auto"):
        if self._summarize_messages:
            prompt_messages = self.messages + [{'role': 'system', 'content': 'Summarize the important content of the immediate prior message. If you are unsure of the solution, call a function afterwards. Be concise, but fully qualify all names.'}]
        else:
            prompt_messages = self.messages

        if function_call_mode == "none":
            prompt_messages.append({
                'role': 'system',
                'content': 'NOTICE: You have reached the maximum budget for function calls. Do NOT generate any "Function call:". You must strictly provide the final diagnosis or explanation based on the information you have now.'
            })

        response = self.get_LLM_response(
            messages=prompt_messages,
            dataset = self._dataset
        )

        if self._summarize_messages:
            llm_summary = response['choices'][0]['message']['content']
            if llm_summary is not None:
                self._replace_last_with_memo(llm_summary)

        response_message = response["choices"][0]["message"]

        self._append_to_interaction_records(prompt_messages, response_message)

        # check if GPT wanted to call a function
        if response_message.get("function_call"):
            # call the function

            try: # Note: the JSON response may not always be valid; be sure to handle errors
                function_name, function_response = self.call_function(response_message)
            except Exception as e:
                if self._debug or isinstance(e, KeyboardInterrupt):
                    raise e
                else:
                    return False # drop erroneous response and retry if step budget left

            self._append_to_messages(response_message) # extend conversation with assistant's reply
            # send the info on the function call and function response to GPT
            function_message = {
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response),
            }
            self._append_to_messages(function_message)
            return False # not done
        else:
            self._append_to_messages(response_message)  # extend conversation with assistant's reply
            return True

    def finish(self):
        finishing_string = "Based on the available information, provide the signatures of the most likely culprit methods for the bug. Your answer will be processed automatically, so make sure to only answer with the accurate signatures of all likely culprits (in `ClassName.MethodName(ArgType1, ArgType2, ...)` format), without commentary (one per line). "
        if not self._allow_multi_predictions:
            finishing_string = finishing_string.replace('signatures', 'signature')
            finishing_string = finishing_string.replace('methods', 'method')
            finishing_string = finishing_string.replace(' (one per line)', '')
            finishing_string = finishing_string.replace('all likely culprits', 'the most likely culprit')

        querying_buggy_methods = {
            'role': 'user',
            'content': finishing_string
        }
        self._append_to_messages(querying_buggy_methods)
        response = self.get_LLM_response(
            messages=self.messages,
            dataset=self._dataset
        )
        response_message = response["choices"][0]["message"]
        self._append_to_messages(response_message)
        if 'content' not in response_message or response_message['content'] == None:
            return "Empty list genearted"
        return response_message['content'].strip()

    def grade(self, answer):
        if self._allow_multi_predictions:
            pred_exprs = answer.splitlines()
        else:
            pred_exprs = [answer]

        matching_method_signatures = {
            pred_expr: self._ri.get_matching_method_signatures(pred_expr)
            for pred_expr in pred_exprs
        }

        grade_result = {}
        for method in self._ri.buggy_method_signatures:
            pred_match = [
                pred_expr for pred_expr in pred_exprs
                if method in matching_method_signatures[pred_expr]
            ]
            grade_result[method] = {
                'is_found': len(pred_match) > 0,
                'matching_answer': pred_match
            }
        return grade_result

    def run(self, budget=10):
        self.startup()
        for i in range(budget):
            if i == budget - 1:
                function_call_mode = "none"
            else:
                function_call_mode = "auto"
            done = self.step(function_call_mode)
            time.sleep(0.1)
            if done:
                break
        final_response = self.finish()
        grade_result = self.grade(final_response)
        return grade_result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', default='llama3')
    parser.add_argument('-e', '--endpoint', default='http://localhost:11434/api/generate')
    parser.add_argument('-b', '--bug_name', default='Chart_1')
    parser.add_argument('-o', '--out', default='test.json')
    parser.add_argument('-p', '--prompt', default='prompts/system_msg_expbug_with_funcs.txt')
    parser.add_argument('-t', '--max_num_tests', default=None, type=int)
    parser.add_argument('--test_offset', default=0, type=int)
    parser.add_argument('--max_budget', default=10, type=int)
    parser.add_argument('--measure_power_consumption', action="store_true")
    parser.add_argument('--allow_multi_predictions', action="store_true")
    parser.add_argument('--summarize_messages', action="store_true")
    parser.add_argument('--show_line_number', action="store_true")
    parser.add_argument('--postprocess_test_snippet', action="store_true")
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()

    ad = AutoDebugger(args.endpoint, args.bug_name, args.model, args.prompt,
        test_offset=args.test_offset,
        max_num_tests=args.max_num_tests,
        allow_multi_predictions=args.allow_multi_predictions,
        summarize_messages=args.summarize_messages,
        show_line_number=args.show_line_number,
        postprocess_test_snippet=args.postprocess_test_snippet,
        debug=args.debug
    )

    start = time.time()
    if args.measure_power_consumption:
        from utils.energy import EnergyMeter 
        meter = EnergyMeter()
        meter.start_session()

    try:
        grade = ad.run(args.max_budget)
    except Exception as e:
        grade = traceback.format_exc()
        if args.debug:
            raise e
    finally:
        result = {
            'time_taken': time.time() - start,
            'messages': ad.messages,
            'interaction_records': {
                "step_histories": ad._interaction_records,
                "mid_to_message": ad._message_map
            },
            'buggy_methods': grade,
            'query_costs': ad.get_cost_history(),
        }

        if args.measure_power_consumption:
            total_energy, gpu_activity, power_draw = meter.finish_session()
            meter.stop()
            result['total_energy'] = total_energy.tolist()
            result['power_draw'] = power_draw
            result['gpu_activity'] = gpu_activity

    with open(args.out, "w") as f:
        json.dump(result, f, indent=4)
