import pygraphviz as pgv
import json

def render_state(state_name, state_data, graph):
    if state_data['Type'] == 'Parallel':
        graph.add_node(state_name, label=state_name, shape='box', style='filled', fillcolor='lightblue')

        # Render parallel branches
        for branch in state_data['Branches']:
            branch_start = branch['StartAt']
            branch_states = branch['States']
            render_state(branch_start, branch_states[branch_start], graph)
            graph.add_edge(state_name, branch_start)
    elif state_data['Type'] == 'Fail':
        graph.add_node(state_name, label=state_name, shape='box', style='filled', fillcolor='red')
    elif state_data['Type'] == 'Choice':
        graph.add_node(state_name, label=state_name, shape='diamond')

        # Render choice conditions and their next states
        for choice in state_data['Choices']:
            choice_condition = choice['Condition']
            choice_next_state = choice['Next']
            graph.add_node(choice_condition, shape='box')
            graph.add_edge(state_name, choice_condition)
            graph.add_edge(choice_condition, choice_next_state)
        
        # Render default state if provided
        if 'Default' in state_data:
            default_next_state = state_data['Default']
            graph.add_edge(state_name, default_next_state)
    else:
        graph.add_node(state_name, label=state_name, shape='box')

        # Handle Catch states
        if 'Catch' in state_data:
            for catch_block in state_data['Catch']:
                error = catch_block['Error']
                next_state = catch_block['Next']
                graph.add_node(error, shape='box')
                graph.add_edge(state_name, error)
                graph.add_edge(error, next_state)

        if 'Next' in state_data:
            next_state = state_data['Next']
            graph.add_edge(state_name, next_state)


def render_step_function_json(json_path, output_path):
    # Load JSON file
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    # Create directed graph
    graph = pgv.AGraph(directed=True)

    # Add states and transitions to the graph
    for state_name, state_data in json_data['States'].items():
        render_state(state_name, state_data, graph)

    # Render graph to PNG
    graph.draw(output_path, prog='dot', format='png')

    print(f"Step Function JSON rendered as PNG: {output_path}")


# Usage example
json_path = 'path/to/your/step_function.json'
output_path = 'path/to/save/output.png'

render_step_function_json(json_path, output_path)
