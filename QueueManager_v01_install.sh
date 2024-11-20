#!/bin/tcsh
set me = `whoami`

set qu = '/mifs/gunwook2/scripts/QueueManagers/v01/qu_v01.py'
set qq = '/mifs/gunwook2/scripts/QueueManagers/v01/qq_v01.py'
set qf = '/mifs/gunwook2/scripts/QueueManagers/v01/qf_v01.py'

echo "***************************************"
echo "*   Queue Manager v0.1 Installation   *"
echo "***************************************"
echo ""
echo "    Enter the path to install:"
echo "    (default: /mifs/$me/scripts/QueueManager_v01/)"
echo -n "    > "
echo ""

if ($< == "") then
    set destpath = "/mifs/$me/scripts/QueueManager_v01"
else
    set destpath = $<
endif

# Check if the destination directory exists
if (! -d $destpath) then
    echo "[info] $destpath does not exist. Creating directory..."
    mkdir -p $destpath    
endif

# Copy the file to the destination directory
echo "[info] Copying the files to $destpath..."
cp $qu $destpath
cp $qq $destpath
cp $qf $destpath
mkdir -p $destpath/qu_log

echo "[info] Setting up the aliases..."
set qu_alias  = "alias qu01 'python $destpath/qu_v01.py'"
set qq_alias  = "alias qq01 'python $destpath/qq_v01.py'"
set qf_alias  = "alias qf01 'python $destpath/qf_v01.py'"
set qqt_alias = "alias qqt01 'python $destpath/qq_time_v01.py'"

echo '## QueueManager v0.1' >> /mifs/$me/tcshrc/tcshrc.alias
echo setenv QueueManagers $destpath >> /mifs/$me/tcshrc/tcshrc.alias
echo $qu_alias >> /mifs/$me/tcshrc/tcshrc.alias
echo $qq_alias >> /mifs/$me/tcshrc/tcshrc.alias
echo $qf_alias >> /mifs/$me/tcshrc/tcshrc.alias
echo $qqt_alias >> /mifs/$me/tcshrc/tcshrc.alias
echo ""

echo "***********************************"
echo "*  Queue Manager v0.1 Installed!  *"
echo "***********************************"

echo ""
echo "  * Installed directory : $destpath."
echo ""
echo "  * The aliases are as follows:"
echo "        qu01: 'python $destpath/qu_v01.py'"
echo "        qq01: 'python $destpath/qq_v01.py'"
echo "        qf01: 'python $destpath/qf_v01.py'"
echo "        qqt01: 'python $destpath/qq_time_v01.py' (for printing epalsed time)"
echo "    You can change your alias in /mifs/$me/tcshrc/tcshrc.alias."
echo ""
echo "  * For more detail, please refer to the /mifs/$me/tcshrc/tcshrc.alias and $destpath/README.md."
echo ""
echo "  Enjoy your Queue Manager v0.1! I will reexecute the tcsh."
echo ""

exec /bin/tcsh