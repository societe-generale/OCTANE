# AWS cIAP OCTANE  

## Presentation

---

There are six roles:

* common : common tasks
* lb : shunt streams based on rules
* waf : performs security tasks for HTTP/HTTPS streams
* vpn : grant customers access to theirs VPC
* fw : filter access to customers VPC
* met : statistics about this VPC

The cloudformation template aims to build all needed components for OCTANE stack.

## Usage

---

A CLI is provided. This CLI is a makefile. Several targets are defined.

For example, if you want to deploy a new stack:

```bash
./make deploy octanetst
```

then the CLI will launch the template yml file named "service_octanetst.yml".

A yaml file is provided as example.

Nine targets are available :

* describe: describe an existing OCTANE stack
* output: retrieve output ressources from an existing OCTANE stack
* deploy: deploy a new OCTANE stack
* update: update an existing OCTANE stack
* events: retrieve all events from an existing OCTANE stack
* watch-events: watch events from an existing OCTANE stack
* destroy: Destroy an existing OCTANE stack
* create-set: Create a change set for an existing OCTANE stack
* check: Check template syntax

### Makefile

I'm a big fan of Makefile files :-), so I have use it for managing the AWS stack. The only mandatory parameter is the stack name. I use it for reading a YAML file (cloudformation template, described below).

There are several targets on this makefile:

* help: basic information
* describe: describe an existing stack (json format)
* output: return outputs from an existing stack (json format)
* deploy: upload the cloudformation template onto a S3 bucket and build the stack.
* update: upload the cloudformation template onto a S3 bucket and update the stack.
* wait: if you need to wait the end of a stack creation before doing another action, you may use this target
* events: return existing events from Cloudformation from an existing stack
* watch-events: return last five existing events from Cloudformation from an existing stack in order to follow the stack creation/update/destruction
* destroy: delete an existing stack
* create-set: create an AWS change-set 
* destroy-peering: destroy an existing peering
* check: Validate template 

### Cloudformation template

This file is the barebone for the OCTANE infrastructure deployment. In order to be used by the makefile, the format name is quite simple: `service_`<__stackname__>`.yml`.

As every cloudformation template, this cloudformation is splitted onto two main sections:
* Parameters
* Resources

You nust customise the parameter section, all resources are based upon it.

```yaml
  VPCName:
    Default: OCTANE
    Description: VPC name
    Type: String
```

>The main stack name.

```yaml
  VPCUuid:
    Default: SMOKETEST
    Description: VPC uuid
    Type: String
```

>If you want more than one OCTANE stack, you have to define a unique ID.

```yaml
  VPCCidr:
    Default: a.b.c.d/24
    Description: VPC instances Cidr root
    Type: String
```

>The OCTANE Cidr (must be unique, otherwise you will find some routing problems)

```yaml
  adminCidr:
    Default: x.y.w.z/21
    Description: VPC where admin instances are
    Type: String
```

>In case you have a centralized administration, you put it there.  
>If you does not have usage of this, you may delete it. But then you have to delete these resources:
>
> * PrivaterouteVPCadmin
> * PublicrouteVPCadmin
> * SGADM
> * routeadminVPC
> * adminVPCPeeringConnection
> * admRouteTable

```yaml
  browsingCidr:
    Default: e.f.g.h/16
    Description: VPC browsing
    Type: String
```

>Proxy access for items in the infrastructure.  
>You may have no use of it, but it's a good practice to know what goes outside.  
>If you do not want to use this, you have also to delete these resources:
>
> * routebrowsingVPC
> * PrivaterouteVPCbrowsing
> * PublicrouteVPCbrowsing
> * browsingVPCPeeringConnection

```yaml
  admRouteTable:
    Default: rtb-wwewedss
    Description: RouteTable to allow admin to communicate with this VPC
    Type: String
```

>Admin route table in case of you use a centralized administration.  
>Must be deleted if no use.

```yaml
  browsingRouteTable:
    Default: rtb-eddsaaeed
    Description: RouteTable to allow browsing to communicate with this VPC
    Type: String
```

>Proxy route table in case of you use a proxy for accessing foreign resources.  
>Must be deleted if no use.

```yaml
  adminSecurityGroup:
    Default: sg-eaaswddd
    Description: Security group for admin servers
    Type: 'AWS::EC2::SecurityGroup::Id'
```

>Admin Security group in case of you use a centralized administration.  
>Must be deleted if no use.

```yaml
  adminVpc:
    Default: vpc-evvsasdfdf
    Description: VPC where admin instances are
    Type: 'AWS::EC2::VPC::Id'
```

>Admin VPC in case of you use a centralized administration.  
>Must be deleted if no use.

```yaml
  browsingVpc:
    Default: vpc-012345
    Description: VPC for browsing
    Type: 'AWS::EC2::VPC::Id'
```

>Proxy VPC in case of you use a centralized proxy.  
>Must be deleted if no use.

```yaml
  sshPublicKey:
    Default: SSH_KEY
    Description: SSH pub key to connect with
    Type: 'AWS::EC2::KeyPair::KeyName'
```

>SSH key for accessing EC2 instances

```yaml
  zone53:
    AllowedValues:
      - ciap-prd.
      - ciap-hml.
      - ciap-dev.
    Default: ciap-dev.
    Type: String
```

>DNS zone declaration.  
>I think it's easy to remember structured DNS name like `octane_tst_dev_hosting_clb_up_mid.ciap-dev` than something like `internal-octanetst-CLBUPMID-9A7999MDRO9C-99999999.eu-west-1.elb.amazonaws.com`. 

```yaml
  bl:
    AllowedValues:
      - BL1
      - BL2
    Default: BL1
    Type: String
```

>Business line declaration.  
>If you have several BL, you msut put them here.  
>If you have none, you put one allowed value and set it as default.

```yaml
  env:
    AllowedValues:
      - DEV
      - HML
      - PRD
      - TMP
    Default: DEV
    Type: String
```

>Environment declaration.  
>If you have several environments, you must put them here.  
>If you have none, you put one allowed value and set it as default.

```yaml
  AZ1:
    Description: AZ 1
    Type: String
    Default: "eu-west-1a"
```

>First availability zone

```yaml
  AZ2:
    Description: AZ 2
    Type: String
    Default: "eu-west-1b"
```

>Second availability zone

```yaml
  instanceTypeUPLB:
    Description: UPLB instance type
    Type: String
    Default: t2.micro
```

> Define EC instance type for UPLB

```yaml
  instanceTypeMIDWAF:
    Description: MIDWAF instance type
    Type: String
    Default: t2.micro
```

> Define EC instance type for MIDWAF

```yaml
  instanceTypeLOWFW:
    Description: LOWFW instance type
    Type: String
    Default: t2.micro
```

> Define EC instance type for LOWFW

```yaml
  instanceTypeLOWMET:
    Description: LOWMET instance type
    Type: String
    Default: c4.xlarge
```

> Define EC instance type for LOWMET

```yaml
  instanceTypeMIDVPN:
    Description: MIDVPN instance type
    Type: String
    Default: t2.nano
```

> Define EC instance type for MIDVPN

> Define AMI id for ec2 instances

```yaml
  ImageId: 
    Description: AMI used for EC2 instances
    Default: "imageid"
```

## Dependencies

---

* A template file 
* A bucket file
* Need to have sufficients rights (AdministratorAccess for example) in order to perform the cloudformation tasks.