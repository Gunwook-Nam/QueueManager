import os
from collections import defaultdict
from datetime import datetime


bold      = "\033[1m"
underline = '\033[4m'
red       = '\033[31m'
green     = '\033[32m'
yellow    = '\033[33m'
blue      = '\033[34m'
grey      = '\033[90m'
reset     = '\033[0m'

def coloring(text, node_type):
    if node_type == 'old':
        return f'{yellow}{text}{reset}'
    elif node_type == 'new':
        return f'{blue}{text}{reset}'
    elif node_type == 'skl':
        return f'{red}{text}{reset}'

me     = os.popen('whoami').read().strip()
qf     = os.popen('qstat -f').read().split('\n\n')[:-1]
server = os.popen('hostname').read().strip()

mu_nodes = {
    f'mu{i:02d}': '' for i in range(1, 30)
}

assigned_node = defaultdict(int)
free_node = {'old' : 10, 'new' : 3, 'skl' : 16}


def get_nodetype(node_num):
    if 1 <= node_num <= 10:
        return 'old'
    elif 11 <= node_num <= 13:
        return 'new'
    elif 14 <= node_num <= 29:
        return 'skl'
    else:
        return 'unk'

    
def print_nodes(node_jobs, node_type):
    job_list = list(node_jobs.items())

    for i, (node, owner) in enumerate(job_list):
        if i == 0:
            print(' '*2, end='')

        node_num = node[-2:]
        node_num = coloring(f'[{node_num}]', node_type)
        print(f'{node_num} {owner.ljust(19)}', end='')

        if (i+1) % 4 == 0 and (i+1) != len(job_list):
            print()
            print(' '*7, end='')

        elif (i+1) == len(job_list):
            print()


for jobinfos in qf:
    owner   = jobinfos.split('Job_Owner = ')[-1].split('@')[0]
    for info in jobinfos.split('\n'):
        if 'start_time = ' in info:
            start_time = info.split(" = ")[-1]
            start_time = datetime.strptime(start_time, "%a %b %d %H:%M:%S %Y")
                
            elapsed = datetime.now() - start_time
            elapsed_hour = elapsed.days * 24 + elapsed.seconds // 3600
            break

    for info in jobinfos.replace('\n\t','').split('\n'):
        if 'exec_host' in info:
            nodes = info.split(" = ")[-1].split("+")
            nodes = set(node.split("/")[0] for node in nodes)
            for node in nodes:
                if node in mu_nodes.keys():
                    num_dots = 17 - len(owner) - len(f'{elapsed_hour}h')
                    mu_nodes[node] = f'{owner}{"."*num_dots}{elapsed_hour}h'
                    # mu_nodes[node] = f'{owner} ({elapsed_hour}h)'
                    assigned_node[owner] += 1
                    free_node[get_nodetype(int(node[-2:]))] -= 1

assigned_node = sorted(assigned_node.items(), key=lambda item: item[1], reverse=True)

down_node_status = os.popen('pbsnodes -l').read().strip().split('\n')

for node_down in down_node_status:
    if node_down:
        node, down = node_down.split()
        if node in mu_nodes.keys():
            down_text = 'down'.ljust(19)
            mu_nodes[node] = f'{grey}{down_text}{reset}'
            free_node[get_nodetype(int(node[-2:]))] -= 1

olds = {k: v for k, v in mu_nodes.items() if 1 <= int(k[-2:]) <= 10}
news = {k: v for k, v in mu_nodes.items() if 11 <= int(k[-2:]) <= 13}
skls = {k: v for k, v in mu_nodes.items() if 14 <= int(k[-2:]) <= 29}
all_nodes = [('old', olds), ('new', news), ('skl', skls)]

print('-'*101)
for node_type, node_jobs in all_nodes:
    print(coloring('* ' + node_type, node_type), end='')
    print_nodes(node_jobs, node_type)
    print('-'*101)

print()
print(f'* Free nodes' + ' '*19 + '* Assigned nodes')
print(f'  {yellow}{"old".center(4)}{reset}', end='')
print(f' {blue}{f"new".center(4)}{reset}', end='')
print(f' {red}{f"skl".center(4)}{reset}', end='')
print(f' {"Total".center(4)}', end='')

print(f' '*11, end='')
job_num_and_len = []
for owner, num in assigned_node:
    print(f'{underline}{owner}{reset}', end='')
    job_num_and_len.append((num, len(owner)))
    print(' '*2, end='')
print()

print(f'  {yellow}{str(free_node["old"]).center(4)}{reset}', end='')
print(f' {blue}{str(free_node["new"]).center(4)}{reset}', end='')
print(f' {red}{str(free_node["skl"]).center(4)}{reset}', end='')
print(f' {str(sum(free_node.values())).center(5)}', end='')
print(f' '*11, end='')
for num, len_owner in job_num_and_len:
    print(f'{str(num).center(len_owner)}', end='')
    print(' '*2, end='')
print()