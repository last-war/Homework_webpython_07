import argparse

"""
py main.py --action -a CRUD-action
py main.py --model -m use table 
py main.py --data -d data with _ as separete
"""

parser = argparse.ArgumentParser(description='CRUD create read update delete')

parser.add_argument('-a', '--action', required=True)
parser.add_argument('-m', '--model', required=True)
parser.add_argument('-d', '--data', required=True)



def do_action(arg):
    action = arg.get('action')
    base_name = arg.get('model')

    match action:
        case 'create':
            pass
        case 'read':
            pass
        case 'update':
            pass
        case 'delete':
            pass



if __name__ == "__main__":
    params = vars(parser.parse_args())
    do_action(params)

