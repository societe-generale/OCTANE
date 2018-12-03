# AWS cIAP OCTANE

## Presentation

---

We presuppose the reader has minimal knowledge on:

* AWS technologies
* Python
* Ansible

First of all you will need to have a proper AWS environment and sufficient authorizations to perform all actions.

__All accounts, users, ports or other references are randomly created and are not related to existing ones. :-)__

There are several layers (from the most exposed to the less exposed):

* resilient load-balancers
* resilient firewalls
* resilient WAF or TCP relay (it depends on the protocole used)
* resilient firewalls
* AWS private link or VPC peering (what suits you)

Several functionnalities are implemented :

* automated SSL certificates creation
* automated haproxy configuration (if choosen)
* automated httpd and/or nginx configuration
  * modsecurity module
  * vhosts whith the availability to enable or not modsecurity
  * udp configuration with Nginx
* automated iptables configuration

## Directory structure

---

* ansible:

    all you need to populate the infrastructure (EC2, ELB, ...etc...)

```console
.
├── ansible.cfg
├── ansible-inventory.py
├── cli_api_octane
├── common -> cli_api_octane
├── grantdomain -> cli_api_octane
├── grantvpnclient -> cli_api_octane
├── group_vars
├── init -> cli_api_octane
├── low_fw -> cli_api_octane
├── low_met -> cli_api_octane
├── main.yml
├── mid_vpn -> cli_api_octane
├── mid_waf -> cli_api_octane
├── octane.yml
├── READme.md
├── revokedomain -> cli_api_octane
├── revokevpnclient -> cli_api_octane
├── roles
│   ├── common
│   │   ├── defaults
│   │   ├── files
│   │   │   └── haproxy_healthcheck_all_all_200_http_ok
│   │   ├── handlers
│   │   │   └── main.yml
│   │   ├── tasks
│   │   │   ├── grant
│   │   │   │   ├── aws_ec2.yml
│   │   │   │   ├── aws_elb.yml
│   │   │   │   ├── aws_sg.yml
│   │   │   │   ├── filebeat.yml
│   │   │   │   ├── iptables.yml
│   │   │   │   └── telegraf.yml
│   │   │   ├── init
│   │   │   │   ├── haproxy_healthcheck.yml
│   │   │   │   ├── selinux.yml
│   │   │   │   ├── softwares.yml
│   │   │   │   ├── ssl.yml
│   │   │   │   ├── system.yml
│   │   │   │   └── yum_repos.yml
│   │   │   ├── main.yml
│   │   │   ├── revoke
│   │   │   │   ├── filebeat.yml -> ../grant/filebeat.yml
│   │   │   │   ├── iptables.yml -> ../grant/iptables.yml
│   │   │   │   └── telegraf.yml -> ../grant/telegraf.yml
│   │   │   ├── start.yml
│   │   │   └── test.yml
│   │   ├── templates
│   │   │   ├── filebeat_all_all.j2
│   │   │   ├── filebeat_low_fw.j2
│   │   │   ├── filebeat_low_met.j2
│   │   │   ├── filebeat_mid_vpn.j2
│   │   │   ├── filebeat_mid_waf.j2
│   │   │   ├── filebeat_up_check.j2
│   │   │   ├── haproxy_all_all.j2
│   │   │   ├── haproxy_healthcheck_all_all.j2
│   │   │   ├── iptables
│   │   │   │   ├── low_fw.j2
│   │   │   │   ├── low_met.j2
│   │   │   │   ├── mid_vpn.j2
│   │   │   │   ├── up_check.j2
│   │   │   │   └── up_lb.j2
│   │   │   ├── motd.j2
│   │   │   ├── telegraf_all_all.j2
│   │   │   ├── telegraf_low_fw.j2
│   │   │   ├── telegraf_low_met.j2
│   │   │   ├── telegraf_mid_vpn.j2
│   │   │   ├── telegraf_mid_waf.j2
│   │   │   ├── telegraf_up_check.j2
│   │   │   └── telegraf_up_lb.j2
│   │   └── vars
│   ├── low_fw
│   │   ├── defaults
│   │   ├── files
│   │   ├── handlers
│   │   │   └── main.yml
│   │   ├── tasks
│   │   │   ├── grant
│   │   │   │   ├── filebeat.yml
│   │   │   │   ├── iptables.yml
│   │   │   │   ├── nginx_directories.yml
│   │   │   │   ├── nginx.yml
│   │   │   │   ├── sudoers.yml
│   │   │   │   └── telegraf.yml
│   │   │   ├── init
│   │   │   │   ├── nginx
│   │   │   │   ├── rsyslog.yml
│   │   │   │   ├── selinux.yml
│   │   │   │   └── softwares.yml
│   │   │   ├── main.yml
│   │   │   └── revoke
│   │   │       └── sudoers.yml
│   │   ├── templates
│   │   │   ├── grant
│   │   │   │   ├── filebeat_yml.j2
│   │   │   │   ├── iptables.j2
│   │   │   │   ├── nginx_conf.j2
│   │   │   │   ├── telegraf_conf.j2
│   │   │   │   └── telegraf_sudoers.j2
│   │   │   └── init
│   │   │       └── rsyslog_iptables.j2
│   │   └── vars
│   ├── low_met
│   │   ├── defaults
│   │   ├── files
│   │   │   ├── check_index.html
│   │   │   ├── grafana
│   │   │   │   ├── jdbranham-grafana-diagram-4406897.zip
│   │   │   │   └── NatelEnergy-grafana-discrete-panel-0.0.7-24-g5e8e975.zip
│   │   │   └── logstash
│   │   │       └── logstash_service
│   │   ├── handlers
│   │   │   └── main.yml
│   │   ├── tasks
│   │   │   ├── grafana
│   │   │   │   ├── create_accountable_user.yml
│   │   │   │   ├── create_dashboards_directories.yml
│   │   │   │   ├── create_organisations.yml
│   │   │   │   ├── delete_accountable_user.yml
│   │   │   │   ├── delete_email_organisations.yml
│   │   │   │   ├── delete_organisations.yml
│   │   │   │   ├── grant_organisation.yml
│   │   │   │   ├── populate_organisations_influxdb.yml
│   │   │   │   ├── retrieve_all_organisations.yml
│   │   │   │   ├── retrieve_certificate.yml
│   │   │   │   ├── revoke_organisation.yml
│   │   │   │   ├── set_dashboards.yml
│   │   │   │   ├── set_datasources.yml
│   │   │   │   ├── set_organisations_users.yml
│   │   │   │   └── switch_user_to_organisation.yml
│   │   │   ├── grant
│   │   │   │   └── logstash.yml
│   │   │   ├── init
│   │   │   │   ├── demo.yml
│   │   │   │   ├── grafana
│   │   │   │   │   ├── admin_password.yml
│   │   │   │   │   ├── deploy_plugins.yml
│   │   │   │   │   └── grafana_ini.yml
│   │   │   │   ├── grafana.yml
│   │   │   │   ├── haproxy.yml
│   │   │   │   ├── influxdb.yml
│   │   │   │   ├── logstash
│   │   │   │   ├── logstash.yml
│   │   │   │   ├── rsyslog.yml
│   │   │   │   ├── selinux.yml
│   │   │   │   ├── softwares.yml
│   │   │   │   └── ssl.yml
│   │   │   ├── main.yml
│   │   │   ├── revoke
│   │   │   │   └── logstash.yml
│   │   │   └── test.yml
│   │   ├── templates
│   │   │   ├── grafana
│   │   │   │   ├── dashboards
│   │   │   │   │   ├── ciap_octane_helicopter_view_json.j2
│   │   │   │   │   ├── ciap_octane_low_stage_json.j2
│   │   │   │   │   ├── ciap_octane_mid_stage_json.j2
│   │   │   │   │   ├── ciap_octane_suricata_details_json.j2
│   │   │   │   │   └── ciap_octane_up_stage_json.j2
│   │   │   │   ├── dashboards_ciap_octane_yaml.j2
│   │   │   │   ├── datasource_ciap_influxdb_yaml.j2
│   │   │   │   └── grafana_ini.j2
│   │   │   ├── haproxy.j2
│   │   │   ├── haproxy_test.j2
│   │   │   ├── httpd.conf.j2
│   │   │   ├── influxdb
│   │   │   │   └── influxdb_conf.j2
│   │   │   ├── logstash
│   │   │   │   ├── logstash_all_filter_conf.j2
│   │   │   │   ├── logstash_all_input_conf.j2
│   │   │   │   ├── logstash_conf.j2
│   │   │   │   ├── logstash_filter_haproxy_access.j2
│   │   │   │   ├── logstash_filter_havp_access.j2
│   │   │   │   ├── logstash_filter_iptables_access.j2
│   │   │   │   ├── logstash_filter_mod_security.j2
│   │   │   │   ├── logstash_filter_nginx_access.j2
│   │   │   │   ├── logstash_filter_suricata.j2
│   │   │   │   ├── logstash_filter_telegraf_json.j2
│   │   │   │   ├── logstash_filter_vpn.j2
│   │   │   │   ├── logstash_input_beats.j2
│   │   │   │   ├── logstash_input_http.j2
│   │   │   │   ├── logstash_output_haproxy_access_conf.j2
│   │   │   │   ├── logstash_output_haproxy_conf.j2
│   │   │   │   ├── logstash_output_havp_access_conf.j2
│   │   │   │   ├── logstash_output_iptables_access_conf.j2
│   │   │   │   ├── logstash_output_mod_security_conf.j2
│   │   │   │   ├── logstash_output_net_response_conf.j2
│   │   │   │   ├── logstash_output_nginx_access_conf.j2
│   │   │   │   ├── logstash_output_nginx_conf.j2
│   │   │   │   ├── logstash_output_suricata_conf.j2
│   │   │   │   └── logstash_output_vpn_access_conf.j2
│   │   │   └── rsyslog_haproxy.j2
│   ├── manage_check_instances
│   │   └── tasks
│   │       ├── common.yml
│   │       ├── main.yml
│   │       ├── start.yml
│   │       └── stop.yml
│   ├── mid_vpn
│   │   ├── defaults
│   │   │   └── main.yml
│   │   ├── files
│   │   │   ├── openssl-ca.ext
│   │   │   ├── openssl-client.ext
│   │   │   ├── openssl-server.ext
│   │   │   └── openvpn_logrotate.conf
│   │   ├── handlers
│   │   │   └── main.yml
│   │   ├── meta
│   │   ├── tasks
│   │   │   ├── grant
│   │   │   │   ├── clients.yml
│   │   │   │   └── iptables.yml
│   │   │   ├── init
│   │   │   │   ├── iptables.yml
│   │   │   │   ├── openvpn.yml
│   │   │   │   └── softwares.yml
│   │   │   ├── main.yml
│   │   │   └── revoke
│   │   │       └── clients.yml
│   │   ├── templates
│   │   │   ├── ca.conf.j2
│   │   │   ├── client.ccd.j2
│   │   │   ├── client.ovpn.j2
│   │   │   ├── iptables.j2
│   │   │   ├── revoke.sh.j2
│   │   │   └── server.conf.j2
│   │   └── vars
│   │       ├── empty.yml
│   │       └── main.yml
│   ├── mid_waf
│   │   ├── defaults
│   │   ├── files
│   │   │   ├── clamdscan.service
│   │   │   ├── clamd.service
│   │   │   ├── havp.tar.gz
│   │   │   ├── httpd_t.te
│   │   │   ├── ifcfg-lo:2
│   │   │   ├── libyajl.tar.gz
│   │   │   ├── modsecurity.data.tar.gz
│   │   │   ├── modsecurity.tar.gz
│   │   │   ├── nginx
│   │   │   ├── nginx.pm.tar.gz
│   │   │   ├── nginx.tar.gz
│   │   │   ├── suricata
│   │   │   ├── suricata.config.tar.gz
│   │   │   ├── suricata.lib.tar.gz
│   │   │   ├── suricata.tar.gz
│   │   │   └── unicode.mapping
│   │   ├── handlers
│   │   │   └── main.yml
│   │   ├── tasks
│   │   │   ├── grant
│   │   │   │   ├── filebeat.yml
│   │   │   │   ├── havp.yml
│   │   │   │   ├── iptables.yml
│   │   │   │   ├── nginx.yml
│   │   │   │   ├── ssl.yml
│   │   │   │   ├── suricata.yml
│   │   │   │   └── telegraf.yml
│   │   │   ├── init
│   │   │   │   ├── clam.yml
│   │   │   │   ├── modsecurity.yml
│   │   │   │   ├── selinux.yml
│   │   │   │   ├── softwares.yml
│   │   │   │   └── system.yml
│   │   │   ├── main.yml
│   │   │   └── revoke
│   │   │       ├── havp.yml
│   │   │       ├── nginx.yml
│   │   │       └── suricata.yml
│   │   ├── templates
│   │   │   ├── clamav.scan.j2
│   │   │   ├── crs-setup.conf.j2
│   │   │   ├── filebeat_yml.j2
│   │   │   ├── havp.blacklist.j2
│   │   │   ├── havp.config.j2
│   │   │   ├── havp.service.j2
│   │   │   ├── havp.whitelist.j2
│   │   │   ├── iptables.j2
│   │   │   ├── mingtreemodsec.conf.j2
│   │   │   ├── modsec.conf.j2
│   │   │   ├── mod_security
│   │   │   ├── modsecurity.conf.j2
│   │   │   ├── nginx.j2
│   │   │   ├── nginx.service.j2
│   │   │   ├── nginx_vhost.j2
│   │   │   ├── suricata.service.j2
│   │   │   ├── suricata.yaml.j2
│   │   │   └── telegraf_conf.j2
│   │   └── vars
│   └── up_lb
│       ├── defaults
│       ├── files
│       ├── handlers
│       │   └── main.yml
│       ├── tasks
│       │   ├── grant
│       │   │   ├── haproxy.yml
│       │   │   └── telegraf.yml
│       │   ├── init
│       │   │   ├── filebeat.yml
│       │   │   ├── iptables.yml
│       │   │   ├── rsyslog.yml
│       │   │   └── selinux.yml
│       │   └── main.yml
│       ├── templates
│       │   ├── filebeat_yml.j2
│       │   ├── haproxy_healthcheck.j2
│       │   ├── haproxy.j2
│       │   ├── iptables.j2
│       │   ├── rsyslog_haproxy.j2
│       │   └── telegraf_conf.j2
│       └── vars
└── up_lb -> cli_api_octane
```

* cloudformation:

   all you need to create the basic infrastructure (VPC, peering, ...etc...)

```console
.
├── Makefile
├── octane_vpc_peering.py
├── READMe.md
└── service_(stack).yml
```

## Infrastructure creation

---

Please refer to the READme.md file in the cloudformation directory.

## Infrastructure settings

---

Please refer to the READme.md file in the ansible directory.

## Configure your newly empty stack

---

### Global variables

---

On the `ansible/group_vars` you will find a YAML example file. This file contains global variables you may (or not) 
configure.

```yaml
v_certificates_path
```

* Default value: `/etc/ssl`
* Where all the certficates are stored

```yaml
v_clamd_temporary_directory
```

* Default value: `/var/run/clamd.scan`
* This directory is needed by CLAMD software.

```yaml
v_clamd_listening_port
```

* Default value: must be a uniq integer (1024..65535)
* The port where CLAMD is listening

```yaml
v_clamd_listening_address
```

* Default value: `127.0.0.1`
* The address to bind the CLAMD daemon.

```yaml
v_havp_root_directory
```

* Default value: `/opt/havp`
* HAVP root directory

```yaml
v_suricata_root_directory
```

* Default value: `/opt/suricata`
* Suricata root directory

```yaml
v_external_listening_address
```

* Default value: `127.0.0.1`
* Suricata: network source

```yaml
v_suricata_listening_address
```

* Default value: `127.0.0.2`
* The address to bind Suricata daemon

```yaml
v_region
```

* Default value: `eu-west-1`
* Default AWS region

```yaml
v_clb_up_mid
```

* Default value: `CLBUPMID`
* Classic load-balancer name between UP and MID zones

```yaml
v_clb_up_vpn
```

* Default value: `CLBUPVPN`
* Classic load-balancer name between UP and VPN zones

```yaml
v_clb_mid_low
```

* Default value: `CLBMIDLO`
* Classic load-balancer name between MID and LOW zones

```yaml
v_sg_up
```

* Default value: `SGUP`
* Security group name for UP zone

```yaml
v_sg_mid
```

* Default value: `SGMID`
* Security group name for MID zone

```yaml
v_sg_vpn
```

* Default value: `SGVPN`
* Security group name for VPN zone

```yaml
v_sg_up_vpn
```

* Default value: `SGUPVPN`
* Security group name between UP and VPN zone

```yaml
v_sg_low
```

* Default value: `SGLOW`
* Security group name for LOW zone

```yaml
v_sg_met
```

* Default value: `SGMET`
* Security group name for metrology zone

```yaml
v_haproxy_stats_listening_port
```

* Default value: must be a uniq integer (1024..65535)
* Haproxy stats listening port

```yaml
v_haproxy_stats_listening_ip
```

* Default value: `127.0.0.1`
* Exposed IP for HAProxy stats

```yaml
v_haproxy_stats_uri
```

* Default value: `haproxy-stats`
* URI to access the HAProxy stats

```yaml
v_metrology_influxdb_host
```

* Default value: `localhost`
* IP to bind the Influxdb deamon

```yaml
v_metrology_grafana_host
```

* Default value: `localhost`
* IP to bind the grafana daemon

```yaml
v_metrology_grafana_port
```

* Default value: `3000`
* Grafana listening port

```yaml
v_mingtree_port
```

* Default value: `must be a uniq integer (1024..65535)`
* Mingtree access port

```yaml
v_metrology_influxdb_port
```

* Default value: `8086`
* Influxdb listening port

```yaml
v_metrology_tcp_socket_port
```

* Default value: `8094`
* Influxdb TCP listening port

```yaml
v_metrology_influxdb_db
```

* Default value: `influxdb_database`
* Name of the database where to store all your measurments

```yaml
v_metrology_influxdb_user
```

* Default value: `influxdb_user`
* Metrology user name (restricted rights)

```yaml
v_metrology_influxdb_password
```

* Default value: `influxdb_password`
* Metrology user password (restricted rights)

```yaml
v_metrology_logstash_port
```

* Default value: `5044`
* Default logstash listening port

```yaml
v_healthcheck_port
```

* Default value: `must be a uniq integer (1024..65535)`
* Healthcheck port for all items in OCTANE infrastructure

```yaml
v_grafana_admin
```

* Default value: `admin`
* Grafana admin name

```yaml
v_grafana_admin_password
```

* Default value: `new_password`
* Grafana admin password

```yaml
v_influxdb_admin
```

* Default value: `influxdb_admin`
* Influxdb master admin name

```yaml
v_influxdb_admin_password
```

* Default value: `influxdb_admin_new_password`
* Influxdb master admin password

```yaml
v_influxdb_logstash_writer
```

* Default value: `logstash_writer`
* Influxdb logstash name (Write only)

```yaml
v_influxdb_logstash_writer_password
```

* Default value: `logstash_writer_password`
* Influxdb logstah password

```yaml
v_influxdb_grafana_reader
```

* Default value: `grafana_reader`
* Influxdb grafana name (Read only)

```yaml
v_influxdb_grafana_reader_password
```

* Default value: `grafana_reader_password`
* Influxdb grafana password

```yaml
v_vpn_port
```

* Default value: `must be a uniq integer (1024..65535)`
* VPN port on VPN zone

```yaml
v_log_path
```

* Default value: `/var/log`
* Path log

```yaml
v_http_proxy
```

* Default value: `http://proxy:3128/`
* System proxy for reaching foreign resources

```yaml
v_https_proxy
```

* Default value: `http://proxy:3128/`
* System proxy for reaching foreign resources

### Domain variables

---

The example files `ansible/vars/granted_domains_(stack)_example.yml` and `ansible/vars/revoked_domains_(stack)_example.yml` contains variables you have to set. All are mandatories.

This file must begin with:

```yaml
---

granted_domains:
```

or

```yaml
---

revoked_domains:
```

You must repeat for each domain you want to grant access to the following lines. Order is not important, but you must start the first item with `-`

```yaml
-  backend_ip_or_fqdn: my.backend.none | 192.168.0.1
```

FQDN or IP of the backend (usually on AWS with several servers, this will be the FQDN of the ELB or an alias on it). I strongly advise using FQDN in AWS environment. This item may be repeated for several domains.

Example: if you declare two domains myfirst.domain.org and mysecond.domain.org, they may have the same backend common.domain.org.

```yaml
  backend_port: 1234
```

The listening port of the backend. May be defined also for other domains.

```yaml
  backend_protocol: http | https
```

If the backend use http (not encrypted stream) or https (encrypted stream).

If you use https, the infrastructure will not check the validity of the backend certificate.

```yaml
  domain: my.public.domain
```

This is the exposed (public) FQDN of your domain. This must be uniq for each domain.

```yaml
  email: my_name@my.public.domain
```

Contact mail.

```yaml
  havp_listening_ip: 127.0.0.1
```

The listening IP for HAVP software. For security reason, you should not change this, since the communication between nginx and havp is not crypted. Therefor, limiting exchange to the loopback is more secure. 

Now, using an another IP than one linked to the loopback is not supported.

```yaml
  havp_listening_port: 12350
```

Uniq HAVP listening port. This must be uniq for each domain. Do not share this port with others ports.

```yaml
  havp_protocol: http
```

Only http is supported.

```yaml
  http: false
```

Set if the exposed domain is listening also on http. Otherwise the domain will listen only on https.

```yaml
  http2_listening_ip: 127.0.0.1
```

Second nginx vhost listening IP (from where the name :-)).

on the midwaf EC2 instance, the stream is:

* (http&|https)_listening_ip:(http&|https)_listening_port: nginx with mod_security -> havp
* havp -> suricata
* http2_listening_ip:http2_listening_port: suricata -> last nginx vhost.

```yaml
  http2_listening_port: 12360
```

Second nginx vhost listening port (from where the name :-)). Do not share this port with others ports.

on the midwaf EC2 instance, the stream is:

* (http&|https)_listening_ip:(http&|https)_listening_port: nginx with mod_security -> havp
* havp -> suricata
* http2_listening_ip:http2_listening_port: suricata -> last nginx vhost.

```yaml
  http_listening_ip: 0.0.0.0
```

HTTP nginx vhost listening IP. Only support 0.0.0.0.

on the midwaf EC2 instance, the stream is:

* (http&|https)_listening_ip:(http&|https)_listening_port: nginx with mod_security -> havp
* havp -> suricata
* http2_listening_ip:http2_listening_port: suricata -> last nginx vhost.

```yaml
  http_listening_port: 12370
```

HTTP nginx vhost listening port. Do not share this port with others ports.

on the midwaf EC2 instance, the stream is:

* (http&|https)_listening_ip:(http&|https)_listening_port: nginx with mod_security -> havp
* havp -> suricata
* http2_listening_ip:http2_listening_port: suricata -> last nginx vhost.

```yaml
  https_listening_ip: 0.0.0.0
```

HTTPS nginx vhost listening IP. Only support 0.0.0.0.

on the midwaf EC2 instance, the stream is:

* (http&|https)_listening_ip:(http&|https)_listening_port: nginx with mod_security -> havp
* havp -> suricata
* http2_listening_ip:http2_listening_port: suricata -> last nginx vhost.

```yaml
  https_listening_port: 12380
```

HTTPS nginx vhost listening port. Do not share this port with others ports.

on the midwaf EC2 instance, the stream is:

* (http&|https)_listening_ip:(http&|https)_listening_port: nginx with mod_security -> havp
* havp -> suricata
* http2_listening_ip:http2_listening_port: suricata -> last nginx vhost.

```yaml
  id: 1..65535
```

This id must be uniq for each domain.

```yaml
  mod_security: 'on'
```

Two available settings:

* `on`: mod_security is enabled (default)
* `off`: mod_security is disabled

```yaml
  preserve_host: true
```

Two available settings:

* `true`: this setting is active (default)
* `false`: this setting is inactive

You may refere to Nginx internet documentation for behaviour of this setting.

```yaml
  proxy_timeout: 5
```

If you use the IDS as an IPS, this will set the Nginx proxy timeout. Why using this setting ? Suricata is not rejecting the stream in case it identifies a threat, it drops. There is no mecanism for Nginx to know that it's the IDS whom had dropped the connection. Fromwhere this timeout.

### VPN clients variables

---

The `ansible/vars/grant_clients_(stack)_example.yml` and `ansible/vars/revoke_clients_(stack)_example.yml` contains variables you have to set. All are mandatories.

This file must begin with:

```yaml
---

openvpn_grant_these_clients:
```

or

```yaml
---

openvpn_revoke_these_clients:
```

You must repeat for each domain you want to grant/revoke access to the following lines. Order is not important, but you must start the first item with `-`

```yaml
- name: "<whatever name you want>"
```

This item must be uniq.

```yaml
  ip: 1..254
```

This item must be uniq. the interval depends on the `openvpn_server_network` variable.

```yaml
  email: "<whatever mail you want>"
```

This item must be uniq.

```yaml
  client_network: "<whatever network you want>"
```

This is used by `OpenVPN` for routing traffic to the client backend network.

```yaml
  client_netmask: "<whatever netmask you want>"
```

This is used by `OpenVPN` for routing traffic to the client backend network.

## Recipes

---

For all this recipes, since I'm a lazy guy, so I design and provide wrapper :-).

You will find a comprehensive list of them on the `ansible` directory, described on the READMe.md.

### Add a new domain

---

Two steps are mandatory before creating a new domain:

* Configure the `ansible/vars/granted_domains_<stack_name>.yml` file with your new domain
* Link the base CLI `cli_api_octane` to `grantdomain`

Then execute the magical command:

```console
~$: ./grantdomain -s <stack_name>
```

If the domain is an https one and you do not provide a certificat, a selfsigned one is automatically generated.

### Modify an existing domain

---

Currently, you cannot modify an existing domain. You have to proceed on two steps:

* Remove the domain
* Add it again

### Remove an existing domain

---

Three steps are mandatory before deleting a new domain:

* Remove all informations about the existing domain from `ansible/vars/granted_domains_<stack_name>.yml`
* Add the removed informations to the `ansible/vars/revoked_domains_<stack_name>.yml`
* Link the base CLI `cli_api_octane` to `revokedomain`

Then execute the magical command:

```console
~$: ./revokedomain -s <stack_name>
```

### Add a VPN user

---

Two steps are mandatory before adding a new VPN user:

* Configure the `ansible/vars/grant_clients_<stack_name>.yml` file with your new user
* Link the base CLI `cli_api_octane` to `grantvpnclient`

Then execute the magical command:

```console
~$: ./grantvpnclient -s <stack_name>
```

### Remove an existing VPN user

---

Three steps are mandatory before adding a new VPN user:

* Remove all informations about the user from `ansible/vars/grant_clients_<stack_name>.yml`. 
* Configure the `ansible/vars/revoke_clients_<stack_name>.yml` with the ones from the grant file.
* Link the base CLI `cli_api_octane` to `revokevpnclient`

Then execute the magical command:

```console
~$: ./revokevpnclient -s <stack_name>
```

