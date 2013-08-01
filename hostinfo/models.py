from django.db import models

# Create your models here.

class Host(models.Model):
    """store host information"""
    hostname = models.CharField(max_length=30)
    osver = models.CharField(max_length=30)
    vendor = models.CharField(max_length=30)
    product = models.CharField(max_length=30)
    cpu_model = models.CharField(max_length=30)
    cpu_num = models.IntegerField(max_length=2)
    memory = models.IntegerField(max_length=8)
    sn = models.CharField(max_length=30)
    ipaddr = models.IPAddressField(max_length=15)
    identity = models.CharField(max_length=32)
    # def __init__(self):
    #     super(Host, self).__init__()
    def __unicode__(self):
        return "%s,%s" % (self.ipaddr,self.hostname)

#class IPaddr(models.Model):
#    ipaddr = models.IPAddressField()
#    host = models.ForeignKey('Host')

class HostGroup(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(Host)

    def __unicode__(self):
        return self.name

@receiver(pre_save,sender=Host)
def mod_handler(sender,**kwargs):
    ret = str(kwargs['instance'])
    ipaddr, hostname = ret.split(',')
    doconnect(ipaddr, 'xxx','xxxxxxx', hostname)

def doconnect(ip, userid, passwd, host):
    import paramiko
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=userid, password=passwd)
    paramiko.util.log_to_file('connect.log')
    stdin, stdout, stderr = client.exec_command('echo %s %s >> /etc/hosts' % (ip, host))
    print 'done.'
