"""
Small script to parse an XML file and print the contents, focusing on type.
"""
import xmltodict


def traverse(current: object, depth: int = 2, current_depth: int = -1, key: str = ''):
    """
    Given a structured list/tree representing an XML file, iterates through to print it
    to a specified depth. Importantly, shows the datatypes.

    :param current: The current tree entry- may be an endpoint, or something that branches further.
    :param depth: The maximum number of dictionaries or lists to delve into.
    :param current_depth: The depth of the current iteration.
    :param key: If this object was an entry in a dictionary, what was its key?
    :return: None
    """
    current_depth += 1

    if isinstance(current, list):
        print('  ' * current_depth + key + str(type(current)) + ': [')

        if current_depth < depth:
            for item in current:
                traverse(item, depth, current_depth)
        else:
            print('  ' * current_depth + "  <MAX DEPTH REACHED>")

        print('  ' * current_depth + ']')

    elif isinstance(current, dict):
        print('  ' * current_depth + key + str(type(current)) + ': {')  # Not using f-strings as they hate loose {

        if current_depth < depth:
            for key, value in current.items():
                traverse(value, depth, current_depth, key)
        else:
            print('  ' * current_depth + "  <MAX DEPTH REACHED>")

        print('  ' * current_depth + '}')

    else:
        print('  '*current_depth + key + str(type(current)) + ': ' + str(current))


with open('helentest.xml') as input_file:
    print(f"### {input_file.name} ###")
    tree = xmltodict.parse(input_file.read())
    traverse(tree, depth=5)

with open('pta_combined_test.xml') as input_file:
    print(f"### {input_file.name} ###")
    tree = xmltodict.parse(input_file.read())
    traverse(tree, depth=6)
