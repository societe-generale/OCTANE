# AWS cIAP OCTANE 

## Presentation

---

We presupose the reader has minimal knowledge on:
* AWS technologies
* Python
* Ansible

First of all you will need to have a proper AWS environment and sufficient authorizations to perform all actions.

__All accounts, users, ports or other references are randomly created and are not related to existing ones. :-)__

There are five roles:

* common : common tasks
* lb : shunt streams based on rules
* waf : performs security tasks for HTTP/HTTPS streams
* vpn : grant customers access to theirs VPC
* fw : filter access to customers VPC
* met : statistics about this VPC

## Common role

---

Tasks implemented:

* Retrieve information about metering instances
* Elastic Load Balancers
  * add or remove ports for each configured domain
  * grant or revoke ports for VPN streams
* Security Groups: 
  * grant or revoke ports for each configured domain
  * configure metering ports
  * configure VPN ports
  * configure healthcheck ports
* Configure specific repositories:
  * centos
  * ELK
  * Grafana
  * Influx
* Install softwares:
  * epel-release
  * vim
  * iptables
  * filebeat
  * haproxy
  * telegraf
* Remove softwares:
  * firewalld
* Configure system
  * change bash behaviour
  * add motd
  * change vimrc behaviour
* Add healthcheck responder
* Generate technical SSL certificates

## Load balancer role

---

Tasks implemented:

* Create self-signed certificates (per domain, needed to start haproxy)
* Generate technical SSL certificates
* Install and configure softwares:
  * SELinux
  * haproxy (included grant/revoke per domain)
  * rsyslog
* Customization of common softwares

## WAF role

---

Tasks implemented:

* Create self-signed certificates (per domain, needed to start Nginx)
* Generate technical SSL certificates
* Customization of common softwares
* Configure SELinux
* Install and configure softwares:
  * Nginx and its dependencies
  * Mod Security (WAF module)
  * CLAMAV and its dependencies
  * HAVP (proxy for AV softwares)
  * SURICATA (IDS)
* Configure system
  * add special path onto fstab
  * create specific loopback
* Configure per domain (grant or revoke):
  * Nginx
  * HAVP
  * SURICATA
  * iptables
  * telegraf
  * filebeat

## FW role

---

Tasks implemented:

* Generate technical SSL certificates
* Customization of common softwares
* Configure SELinux
* Install and configure softwares:
  * Nginx
* Configure sudoers for telegraf
* Configure system
  * enable router mode

## VPN role

---

Tasks implemented:

* Generate technical SSL certificates
* Customization of common softwares
* Install and configure softwares:
  * OpenVPN
* Grant/Revoke VPN clients

## Metering role

---

Tasks implemented:

* Generate technical SSL certificates
* Customization of common softwares
* Install and configure softwares:
  * Logstash
  * Grafana
  * Influxdb
* Add/Remove domain meterings

## Usage

---

A CLI is provided. This CLI is one script, linked to itself by each tag.

For exemple, if you link the base script to init, then if you use:
```bash
./init -s <stack>
```
then the CLI will launch all ansible tasks with tag "init".

Eleven usages are available :

* init: initialise an OCTANE stack
* common: common role 
* up_lb: load-balancer role on exposed zone
* mid_waf: WAF role on filtered zone
* mid_vpn: VPN role on filtered zone
* low_fw: FW role on private zone
* low_met: Metering role on private zone
* revokedomain: remove an existing domain from an OCTANE stack
* grantdomain: add a new domain to an OCTANE stack
* grantvpnclient: add a new VPN client to an existing domain
* revokevpnclient: remove an existing VPN client from an existing domain

## Main Playbook used

---

```yaml
---
- name: Apply common configuration to "{{ stack }}"
  hosts: "{{ stack }}"
  become: yes
  gather_facts: yes
  roles:
    - common

- name: cIAP "{{ stack }}" setup for "up_lb"
  hosts: "{{ stack }}:&up:&lb"
  become: yes
  gather_facts: yes
  roles:
    - "up_lb"

- name: cIAP "{{ stack }}" setup for "mid_waf"
  hosts: "{{ stack }}:&mid:&waf"
  become: yes
  gather_facts: yes
  roles:
    - "mid_waf"

- name: cIAP "{{ stack }}" setup for "mid_vpn"
  hosts: "{{ stack }}:&mid:&vpn"
  become: yes
  gather_facts: yes
  roles:
    - "mid_vpn"

- name: cIAP "{{ stack }}" setup for "low_fw"
  hosts: "{{ stack }}:&low:&fw"
  become: yes
  gather_facts: yes
  roles:
    - "low_fw"

- name: cIAP "{{ stack }}" setup for "low_met"
  hosts: "{{ stack }}:&low:&met"
  become: yes
  gather_facts: yes
  roles:
    - "low_met"

- name: cIAP "{{ stack }}" checks
  hosts: "{{ stack }}:&check"
  run_once: true
  become: yes
  gather_facts: yes
  roles:
    - "check"
```

## Manage check instances playbook

---

```yaml
---

- name: Manage check instances (start/stop)
  hosts: localhost
  become: false
  gather_facts: no
  tags:
    - manage_check_instances
  roles:
    - "manage_check_instances"
```

## Dependencies

---

Does not depend on any other roles, but the host need to have:

* the function tag
* the stage tag
* the cloudformation stack name.

An `ansible.cfg` is present on the current directory with :
```ini
[defaults]
retry_files_enabled = false
inventory = ansible-inventory.py
remote_user = root
stdout_callback = debug
host_key_checking = false
```
