# AWS cIAP OCTANE 

## Presentation

---

This documentation will lead you on a way to install an octane stack.

We presupose the reader has minimal knowledge on:

* AWS technologies
* Python
* Ansible

First of all you will need to have a proper AWS environment and sufficient authorizations to perform all actions.

__All accounts, users, ports or other references are randomly created and are not related to existing ones. :-)__

## Prerequisite

<TO BE COMPLETED BY ANTHONY GEA>

## Pre installation

---

Create a virtualenv:

``` bash
virtualenv myciap
```

Use the following requirements (create a file named requirements.txt in the myciap directory):

```bash
asn1crypto==0.24.0
awscli==1.16.26
bcrypt==3.1.4
boto==2.49.0
boto3==1.9.16
botocore==1.12.16
cffi==1.11.5
colorama==0.3.9
cryptography==2.3.1
docutils==0.14
fabric==2.4.0
idna==2.7
invoke==1.2.0
jmespath==0.9.3
paramiko==2.4.2
prettytable==0.7.2
pyasn1==0.4.4
pycparser==2.19
PyNaCl==1.3.0
python-dateutil==2.7.3
PyYAML==3.13
rsa==3.4.2
s3transfer==0.1.13
six==1.11.0
urllib3==1.23
```

Then execute this command:

```bash
cd myciap
source bin/activate
pip install -r requirements.txt
```

## Installation

---

Simply clone the repository on your newly created virtualenv directory:

```bash
git clone <<path to github.com repository>> (eg https://github.com/societe-generale/OCTANE.git)
```

