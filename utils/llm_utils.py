import time
import requests
import json
import torch

from abc import ABC
from guidance import models, gen

class TextGenerationEngine(ABC):
    def __init__(self):
        self._query_costs = list()

    def _funcCall2str(self, function_call):
        return function_call['name']+'('+', '.join(f'{k}={v}' for k, v in json.loads(function_call['arguments']).items())+')'

    def _messages2prompt(self, messages):
        full_str = ''
        for m in messages:
            role_str = m['role'].title()
            content_str = m['content'] if m['content'] is not None else ''
            func_call_str = f'Function call: {self._funcCall2str(m["function_call"])}' if 'function_call' in m else ''
            full_str += f'[{role_str}] {content_str}{func_call_str}\n'
        full_str += '[Assistant] '
        return full_str

    def parse_response(self, response, dataset):
        if 'Function call:' in response:
            response = [line for line in response.splitlines() if 'Function call:' in line][0]
            true_response = response.split('Function call:')[1].strip()
            func_name = true_response.split('(')[0]
                
            arg_value = true_response.split('(')[1].removesuffix(')') if '(' in true_response else ''
            if '=' in arg_value:
                arg_value = arg_value.split('=')[-1]
            arg_value = arg_value.strip('"').strip("'")
            if dataset == 'defects4j':
                if func_name == 'get_failing_tests_covered_methods_for_class':
                    args_dict = {'class_name': arg_value}
                elif func_name == 'get_failing_tests_covered_classes': 
                    args_dict = {}
                else:
                    args_dict = {'signature': arg_value}
            else: # bugsinpy
                if func_name == 'get_covered_packages':
                    args_dict = {}
                elif func_name == 'get_failing_tests_covered_classes':
                    args_dict = {'package_name': arg_value}
                elif func_name == 'get_failing_tests_covered_methods_for_class':
                    args_dict = {'class_name': arg_value}
                else:
                    args_dict = {'signature': arg_value}
            
            response_obj = {'choices': [{"message": {
                'role': "assistant",
                "content": None,
                "function_call": {
                    "name": func_name,
                    "arguments": json.dumps(args_dict),
                }
            }}]}

            return response_obj
        else:
            response_obj = {'choices': [{"message": {
                'role': "assistant",
                "content": response,
            }}]}
            return response_obj

    def _query_model(self, payload):
        pass
    
    def get_LLM_response(self, messages, dataset):
        pass
        
    def clear_cost_history(self):
        self._query_costs.clear()

    def get_cost_history(self):
        return self._query_costs

class OllamaEngine(TextGenerationEngine):
    def __init__(self, endpoint, model):
        super().__init__()
        self._base_url = endpoint
        self._model = model

    def _extract_costs(self, response):
        self._query_costs.append({
            key: response[key]
            for key in ['total_duration', 'load_duration', 'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration']
            if key in response
        })

    def _query_model(self, payload):
        for _ in range(5):
            try:
                json_payload = json.dumps(payload)
                headers = {'Content-Type': 'application/json'}
                response = json.loads(requests.post(self._base_url, data=json_payload, headers=headers).text)
                self._extract_costs(response)
                return response['response']
            except Exception as e:
                save_err = e
                if "The server had an error processing your request." in str(e):
                    time.sleep(1)
                else:
                    break
        raise save_err

    def get_LLM_response(self, messages, dataset):
        payload = {
            'model': self._model,
            'prompt': self._messages2prompt(messages),
            'stream': False
        }
        return self.parse_response(self._query_model(payload), dataset) 
        
class HFEngine(TextGenerationEngine):
    def __init__(self, model):
        super().__init__()
        self._model = models.Transformers(model, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map='auto')

    def _query_model(self, payload):
        for _ in range(5):
            try:
                prompt = payload['prompt']
                
                lm = self._model + prompt
                start_time = time.time()
                lm += gen(name='response', temperature=1e-5)
                gen_time = time.time() - start_time
                generated_text = lm['response']
                
                self._query_costs.append({
                    'generation_time': gen_time,
                    'prompt_words': len(prompt.split()),
                    'completion_words': len(generated_text.split())
                })
                
                return generated_text
            except Exception as e:
                save_err = e
                if "The server had an error processing your request." in str(e):
                    time.sleep(1)
                else:
                    break
        raise save_err
        
    def get_LLM_response(self, messages, dataset):
        payload = {
            'prompt': self._messages2prompt(messages),
            'stream': False,
        }
        return self.parse_response(self._query_model(payload), dataset)