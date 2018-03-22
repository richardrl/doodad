import os

import doodad as dd
import doodad.ec2 as ec2
import doodad.ssh as ssh
import doodad.mount as mount
from doodad.utils import EXAMPLES_DIR, REPO_DIR


# Local docker
mode_docker = dd.mode.LocalDocker(
    image='richardrl/nrl:latest',
)

# or this! Run experiment via docker on another machine through SSH
mode_ssh = dd.mode.SSHDocker(
    image='python:3.5',
    credentials=ssh.SSHCredentials(hostname='my.machine.name', username='my_username', identity_file='~/.ssh/id_rsa'),
)

# or use this!
# mode_ec2=None
mode_ec2 = dd.mode.EC2AutoconfigDocker(
   image='richardrl/nrl:latest',
   region='us-east-2',
   instance_type='c4.4xlarge',
    # instance_type='m3.medium',
   spot_price=0.3,
    terminate=False,
    s3_log_prefix="nconvs6-200g-experiment"
)

MY_RUN_MODE = mode_ec2  # CHANGE THIS

# Set up code and output directories
OUTPUT_DIR = '/home/richard/newnrl/noreward-rl-private/src/tmp/'  # this is the directory visible to the target
REPO_DIR = '/home/richard/newnrl/'
mounts = [
    mount.MountLocal(local_dir=REPO_DIR, pythonpath=True, filter_dir=['tmp/', 'mapgen2_take2/', 'testmaps', 'outdir', 'curiosity', 'doomFiles', 'a3c-agent-results-test']), # Code
    # mount.MountLocal(local_dir=os.path.join(EXAMPLES_DIR, 'secretlib'), pythonpath=True), # Code
]

if MY_RUN_MODE == mode_ec2:
    output_mount = mount.MountS3(s3_path='outputs', mount_point=OUTPUT_DIR, output=True, sync_interval=900)  # use this for ec2
else:
    output_mount = mount.MountLocal(local_dir=os.path.join(EXAMPLES_DIR, 'tmp_output'),
        mount_point=OUTPUT_DIR, output=True)
mounts.append(output_mount)

# print(mounts)

THIS_FILE_DIR = os.path.realpath(os.path.dirname(__file__))
dd.launch_python(
    # target=os.path.join(THIS_FILE_DIR, 'app_main.py'),  # point to a target script. If running remotely, this will be copied over
    target=os.path.join(REPO_DIR, 'noreward-rl-private/src/train.py'),
    mode=MY_RUN_MODE,
    mount_points=mounts,
    args={
        'num-workers': 17,
        'unsup': 'action',
        'log-dir': OUTPUT_DIR.replace("richard", "ubuntu"),
        'env-id': "MonsterKongTrain-v0"
    },
    verbose=True,
)

