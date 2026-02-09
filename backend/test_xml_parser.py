"""
Test XML parser
"""
import re
import json
from typing import List, Dict, Any


def parse_xml_tool_calls(content: str) -> List[Dict[str, Any]]:
    """
    Parse XML-style tool calls from model response.
    """
    tool_calls = []
    
    # Pattern to extract tool_call blocks
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_call_matches = re.findall(tool_call_pattern, content, re.DOTALL)
    
    for tool_call_content in tool_call_matches:
        # Extract function name
        function_match = re.search(r'<function=([^>]+)>', tool_call_content)
        if not function_match:
            continue
        
        function_name = function_match.group(1).strip()
        
        # Extract all parameters
        param_pattern = r'<parameter=([^>]+)>\s*(.*?)\s*</parameter>'
        param_matches = re.findall(param_pattern, tool_call_content, re.DOTALL)
        
        arguments = {}
        for param_name, param_value in param_matches:
            param_name = param_name.strip()
            param_value = param_value.strip()
            
            # Try to parse as JSON if it looks like JSON
            if param_value.startswith('{') or param_value.startswith('['):
                try:
                    arguments[param_name] = json.loads(param_value)
                except json.JSONDecodeError:
                    arguments[param_name] = param_value
            else:
                arguments[param_name] = param_value
        
        tool_calls.append({
            "name": function_name,
            "arguments": arguments
        })
    
    return tool_calls


# Test cases
test1 = "<tool_call> <function=list_tasks> </function> </tool_call>"
test2 = "<tool_call> <function=add_task> <parameter=title> sleep </parameter> <parameter=description> Need to schedule sleep </parameter> </function> </tool_call>"
test3 = "<tool_call> <function=delete_task> <parameter=task_id> 18102103-b363-43ac-b3de-1a69da619fea </parameter> </function> </tool_call>"

print("Test 1 (list_tasks):")
result1 = parse_xml_tool_calls(test1)
print(f"  Result: {result1}")
print()

print("Test 2 (add_task):")
result2 = parse_xml_tool_calls(test2)
print(f"  Result: {result2}")
print()

print("Test 3 (delete_task):")
result3 = parse_xml_tool_calls(test3)
print(f"  Result: {result3}")
