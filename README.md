# Queue Manager

**Author:** Gunwook Nam  
**Version:** 0.1  
**Last Updated:** 2024-11-20  

## Overview
Queue Manager is a collection of scripts designed to simplify job monitoring on the MICC `mu` server.
These tools provide enhanced visualization and filtering of job information for improved usability.

## Features

### `qu01`
- Displays the current time and username.
- Provides concise and structured job information, optimized for narrow displays.

### `qq01`
- Organizes job information into partitions: old, new, and `skl`.
- Displays the number of free nodes and assigned nodes.

### `qf01`
- Filters and displays only the user's jobs.
- Highlights the job submission path in grey for better readability.

### `qqt01`
- Extends `qq01` by including elapsed time for each job.
- Useful for estimating the termination time of others' jobs.

## Installation
To install Queue Manager v0.1, execute the installation `tcsh` script:

```tcsh
./QueueManager_v01_install.sh
```