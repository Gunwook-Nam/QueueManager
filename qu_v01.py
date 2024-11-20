import os
from datetime import datetime


red    = "\033[31m"
green  = "\033[32m"
yellow = "\033[33m"
grey   = "\033[90m"
reset  = "\033[0m"

def get_nodetype(node_num):
    if 1 <= node_num <= 10:
        return "old"
    elif 11 <= node_num <= 13:
        return "new"
    elif 14 <= node_num <= 29:
        return "skl"
    else:
        return "unk"

def set_len(qu):
    l_id   = max([len(str(job['jobid'])) for job in qu]) + 1
    l_sess = max([len(str(job['sessionid'])) for job in qu] + [6]) + 1
    l_name = max([len(str(job['jobname'])) for job in qu]) + 1
    l_queu = max([len(str(job['queue'])) for job in qu]) + 1
    l_node = max([len(str(job['node'])) for job in qu]) + 1
    l_stat = 9
    l_t0   = 12
    l_dt   = 12
    return l_id, l_sess, l_name, l_queu, l_node, l_stat, l_t0, l_dt

def print_now():
    print()
    print(f' * Now  : {datetime.now().strftime("%m/%d %H:%M:%S")}')
    print(f' * User : {user}\n')

def print_boarder(qu):
    max_width = sum(set_len(qu)) + len(set_len(qu)) + 1
    print("+" + "="*max_width + "+")

def print_header():
    l_id, l_sess, l_name, l_queu, l_node, \
    l_stat, l_t0, l_dt = set_len(qu)
        
    header = "| " + f"{'JobID':<{l_id}} " \
                  + f"{'Session':<{l_sess}} "\
                  + f"{'JobName':<{l_name}} " \
                  + f"{'Queue':<{l_queu}} " \
                  + f"{'Node':<{l_node}} "\
                  + f"{'State':<{l_stat}} "\
                  + f"{'Start':<{l_t0}} " \
                  + f"{'Elapsed':<{l_dt}}" + " |"
                #   + f"{'Node':<{l_node}} "\

    line = "| " + "-"*l_id   + " " \
                + "-"*l_sess + " " \
                + "-"*l_name + " " \
                + "-"*l_queu + " " \
                + "-"*l_node + " " \
                + "-"*l_stat + " " \
                + "-"*l_t0 + " " \
                + "-"*l_dt + " |"
                # + "-"*l_node + " " \

    print(header)
    print(line)

def print_job(job):
    l_id, l_sess, l_name, l_queu, l_node, \
    l_stat, l_t0, l_dt = set_len(qu)

    if job['queue'] == 'small':
        queue_color = yellow
    elif job['queue'] == 'normal':
        queue_color = red
    else:
        queue_color = reset

    if job['jobstate'] == 'R':
        state_color = green
        state = 'Running'
    elif job['jobstate'] == 'Q':
        state_color = grey
        state = 'Queue'
    elif job['jobstate'] == 'C':
        state_color = reset
        state = 'Complete'
    elif job['jobstate'] == 'E':
        state_color = reset
        state = 'Exit'
    else:
        state_color = reset
        state = job['jobstate']
    

    print("|", end=" ")
    print(f"{job['jobid']:<{l_id}}", end=" ")
    print(f"{job['sessionid']:<{l_sess}}", end=" ")
    print(f"{job['jobname']:<{l_name}}", end=" ")
    print(f"{queue_color}{job['queue']:<{l_queu}}{reset}", end=" ")
    print(f"{job['node']:<{l_node}}", end=" ")
    print(f"{state_color}{state:<{l_stat}}{reset}", end=" ")
    print(f"{job['start_time']:<{l_t0}}", end=" ")
    print(f"{job['elapsed_time']:<{l_dt}}", end=" ")
    print("|")


qf     = os.popen('qstat -f').read().split('\n\n')[:-1]
user   = os.popen('whoami').read().strip()
server = os.popen('hostname').read().strip()

qu = []

for jobinfos in qf:
    job_owner = jobinfos.split('Job_Owner = ')[-1].split('@')[0]
    if job_owner != user:
         continue
    else:
        jobid        = "--"
        sessionid    = "--"
        jobname      = "--"
        queue        = "--"
        nodeinfo     = "--"
        jobstate     = "--"
        start_time   = "--"
        elapsed_time = "--"
        
        for info in jobinfos.split("\n"):

            if 'Job Id' in info:
                jobid = info.split(": ")[-1].split('.')[0]

            if 'session_id' in info:
                sessionid = info.split(" = ")[-1]

            if 'Job_Name' in info:
                jobname = info.split(" = ")[-1]

            if 'queue = ' in info:
                queue = info.split(" = ")[-1]

            if 'job_state' in info:
                jobstate = info.split(" = ")[-1]

            if 'start_time' in info:
                start_time = info.split(" = ")[-1]
                start_time = datetime.strptime(start_time, "%a %b %d %H:%M:%S %Y")
                
                elapsed_time = datetime.now() - start_time
                elap_d = elapsed_time.days
                elap_h, elap_m = divmod(elapsed_time.seconds, 3600)
                elap_m, elap_s = divmod(elap_m, 60)
                elapsed_time = f"{elap_d:01d}d,{elap_h:02d}:{elap_m:02d}:{elap_s:02d}"
                
                start_time = start_time.strftime("%m/%d %H:%M")

            if 'exec_host' in info:
                host = info.split(" = ")[-1]
                host = [h.split("/")[0].split(server)[-1] for h in host.split("+")]
                hostinfo = "+".join(host)
                hosttype = get_nodetype(int(host[0]))
                nodeinfo = f"{hostinfo}({hosttype})"

    qu.append({
        'jobid': jobid,
        'sessionid': sessionid,
        'jobname': jobname,
        'queue': queue,
        'jobstate': jobstate,
        'start_time': start_time,
        'elapsed_time': elapsed_time,
        'node' : nodeinfo
    })


if len(qu) == 0:
    print(f"{grey}  No job is running now.  {reset}")
    exit()

else:
    print_now()
    print_boarder(qu)
    print_header()

    for job in qu:
        print_job(job)

    print_boarder(qu)

import json

queue_path = os.popen('echo $QueueManagers')
queue_path = queue_path.read().strip()
log_path = queue_path + '/qu_log/'
for job in qu:
    id = job['jobid']
    with open(log_path + f'{id}.json', 'w') as f:
        json.dump(job, f, indent=4)

for log in os.listdir(log_path):
    log_name = log.split('.json')[0]
    if log_name not in [job['jobid'] for job in qu] and 'exit' not in log_name:
        done_job = json.load(open(log_path + f'{log}'))
        job_name = done_job['jobname']
        os.rename(log_path + f'{log}', log_path + f'{log_name}_exit.json')
        print(f" * Check : {job_name} (JobID {log_name})")
        