import os
import yaml

from dotenv import load_dotenv
load_dotenv() 

def load_agents_config():
    config_path = os.path.join(os.path.dirname(__file__), 'agents_config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def build_task_prompt(agent_config, common_config):
    schema = common_config['response_structure']['schema'].strip()
    examples = agent_config.get('example_vulnerabilities', '').strip()

    task_prompt = (
        f"Task: {agent_config['task_description']}\n"
        f"Important: {common_config['output_format_instruction']}\n"
        f"Required output structure:\n{schema}.\n"
        f"Few Examples:\n{examples}.\n"
        f"In case no vulnerability found return {common_config['response_structure']['no_findings_response']} "
    )
    
    return task_prompt

config = load_agents_config()
common_config = config['common']

MODELS = []

agent_names = ['xml_api_agent', 'access_control_agent', 'file_access_agent', 'client_side_agent', 'input_validation_agent']

for agent_name in agent_names:
    agent_config = config['agents'][agent_name]
    api_key = os.getenv(agent_config['api_key_env'])
    task_prompt = build_task_prompt(agent_config, common_config)
    
    model = {
        "name": common_config['model_name'],
        "api_key": api_key,
        "task": task_prompt
    }
    
    MODELS.append(model)