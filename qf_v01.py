import os

red    = "\033[31m"
green  = "\033[32m"
yellow = "\033[33m"
grey   = "\033[90m"
reset  = "\033[0m"

yellow_bg = "\033[43m"
black_txt = "\033[30m"


user = os.popen('whoami').read().strip()
print(f"{yellow} {user}'s job {reset}")

qf_string = os.popen('/mifs/gunwook2/scripts/QueueManagers/asset/qstat_detail')
qf_new = []
for qf_info in qf_string:
    if user in qf_info:
        job_info = {
            'id' : '',       'owner' : '',       'jobname' : '',
            'nodes' : '',    'walltime' : '',    'status' : '',
            'path' : '',
                }
        qf_info = qf_info.split()
        # running job
        if len(qf_info) == 7:
            id, owner, jobname, nodes, walltime, status, path = qf_info
        
        # queued job
        elif len(qf_info) == 5:
            id, owner, jobname, status, path = qf_info
            nodes = '--'
            walltime = '--:--:--'

        job_info['id'] = id
        job_info['owner'] = owner
        job_info['jobname'] = jobname
        job_info['nodes'] = nodes
        job_info['walltime'] = walltime
        job_info['status'] = status
        job_info['path'] = path
        qf_new.append(job_info)

print('num  id       jobname                 nodes    walltime    status')
print('='*80)
for i, job in enumerate(qf_new):
    if job['status'] == 'R':
        print(f"[{i}]  {job['id']}    {job['jobname']:<20}    {job['nodes']:<5}    {job['walltime']}    {green}{job['status']}{reset}")
    else:
        print(f"[{i}]  {job['id']}    {job['jobname']:<20}    {job['nodes']:<5}    {job['walltime']}    {job['status']}")
    print(f"{grey}     {job['path']}{reset}")
        