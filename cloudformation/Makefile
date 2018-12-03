S3_BUCKET?=$(bucket)
SERVICE=$(stack)
TARGZFILE=$(targzfile)
STACK_BL=BL1
STACK_ENV=TMP
AWS_DEFAULT_REGION = eu-west-1
AWS_ROLE ?= arn:aws:iam::1111122222:role/role-name
VPC_CIAP = $(vpc_ciap)
VPC_CIAP_ADMIN = $(vpc_ciap_admin)
no_proxy=169.254.169.254


export


.PHONY: check update events describe output help watch-events destroy assume-role destroy-peering upload-to-bucket wait-create wait-delete

assume-role:
	$(info your script for AWS credentials) 

help:
	$(info make <action> stack=<name>)

describe: assume-role
	@aws cloudformation describe-stacks --stack-name $(SERVICE) | jq

output: assume-role
	@aws cloudformation describe-stacks --stack-name $(SERVICE) | jq -r '.Stacks[].Outputs'

deploy: assume-role
	aws s3 cp service_$(SERVICE).yml s3://$(S3_BUCKET)/CloudFormation/$(SERVICE).yml --metadata infra=ciap,service=$(SERVICE) --region=$(AWS_DEFAULT_REGION)
	aws cloudformation create-stack --stack-name $(SERVICE) \
	--template-url https://s3.amazonaws.com/$(S3_BUCKET)/CloudFormation/$(SERVICE).yml \
	--tags Key=infra,Value=ciap Key=service,Value=$(SERVICE) Key=BL,Value=$(STACK_BL) Key=Env,Value=$(STACK_ENV) \
	--capabilities CAPABILITY_IAM

update: assume-role
	aws s3 cp service_$(SERVICE).yml s3://$(S3_BUCKET)/CloudFormation/$(SERVICE).yml --metadata infra=ciap,service=$(SERVICE)
	aws cloudformation update-stack --stack-name $(SERVICE) \
	--template-url https://s3.amazonaws.com/$(S3_BUCKET)/CloudFormation/$(SERVICE).yml \
	--tags Key=infra,Value=ciap Key=service,Value=$(SERVICE) Key=BL,Value=$(STACK_BL) Key=Env,Value=$(STACK_ENV) \
	--capabilities CAPABILITY_IAM

upload-to-bucket: assume-role
	aws s3 cp $(TARGZFILE)_$(SERVICE).tar.gz s3://$(S3_BUCKET)/CloudFormation/$(TARGZFILE)_$(SERVICE).tar.gz --region=$(AWS_DEFAULT_REGION)

wait-create: assume-role
	aws cloudformation wait stack-create-complete --stack-name $(SERVICE)

wait-delete: assume-role
	aws cloudformation wait stack-delete-complete --stack-name $(SERVICE)

events: assume-role
	@aws cloudformation describe-stack-events --stack-name $(SERVICE)

watch-events: assume-role
	@watch -n5 aws cloudformation describe-stack-events --stack-name $(SERVICE) | head -50

destroy: assume-role
	aws cloudformation delete-stack --stack-name $(SERVICE)

create-set: assume-role
	@aws cloudformation create-change-set --stack-name $(SERVICE) \
	--template-url https://s3.amazonaws.com/$(S3_BUCKET)/CloudFormation/$(SERVICE).yml \
	--change-set-name $(SERVICE)-upgrade

destroy-peering: assume-role
	$(eval TMP_PEERING = $(shell AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) AWS_SESSION_TOKEN=$(AWS_SESSION_TOKEN) AWS_DEFAULT_REGION=$(AWS_DEFAULT_REGION) aws ec2 describe-vpc-peering-connections --filters '[ { "Name": "tag:Name", "Values": [ "$(VPC_CIAP)_$(VPC_CIAP_ADMIN)" ] }, { "Name": "status-code", "Values": [ "active" ] } ]' | jq -r '.VpcPeeringConnections[].VpcPeeringConnectionId'))
	$(if $(strip $(TMP_PEERING)),aws ec2 delete-vpc-peering-connection --vpc-peering-connection-id  $(TMP_PEERING) --region $(AWS_DEFAULT_REGION),)

check: assume-role
	aws s3 cp $(SERVICE).yml s3://$(S3_BUCKET)/CloudFormation/$(SERVICE).yml --metadata infra=ciap,service=$(SERVICE)
	aws cloudformation validate-template --template-url https://s3.amazonaws.com/$(S3_BUCKET)/CloudFormation/$(SERVICE).yml