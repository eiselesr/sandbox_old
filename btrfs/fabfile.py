import fabric.api as fabi

fabi.env.password = 'riaps'
fabi.env.sudo_password = 'riaps'

def example():
    fabi.sudo('mkdir -p /apps/test')
    fabi.put('btrfs-example.sh', '/apps/test', use_sudo=True)
    fabi.sudo('chmod +x /apps/test/btrfs-example.sh')
    fabi.sudo('cd /apps/test/ && ./btrfs-example.sh')


def btrfsQuota():
    fabi.sudo('mkdir -p /apps/btrfsQuota')
    fabi.put('btrfsQuota.sh', '/apps/btrfsQuota', use_sudo=True)
    fabi.sudo('chmod +x /apps/btrfsQuota/btrfsQuota.sh')
    fabi.sudo('/apps/btrfsQuota/btrfsQuota.sh /apps/test')
    fabi.sudo('rm -rf /apps/btrfsQuota')
