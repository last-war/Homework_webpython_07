import argparse

from seed import fill_db

"""
py main.py --action -a CRUD-action or fake
py main.py --model -m use table or fake
py main.py --data -d data with _ as separete
"""

parser = argparse.ArgumentParser(description='CRUD create read update delete')

parser.add_argument('-a', '--action', required=True)
parser.add_argument('-m', '--model', required=True)
parser.add_argument('-d', '--data', required=True)


def do_action(arg):
    action = arg.get('action')
    tabl_name = arg.get('model')
    raw_data = arg.get('data')

    match action:
        case 'fake':
            fill_db()
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

