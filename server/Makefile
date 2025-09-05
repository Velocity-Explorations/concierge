aws_id := 471112781958
aws_region := us-east-1
repo_name := tti-server
platform := linux/amd64
pub_alias  := j8j9j8z5
pub_region := us-east-1

build-docker:
	docker build --platform ${platform} -t $(aws_id).dkr.ecr.$(aws_region).amazonaws.com/${repo_name}:latest .

push:
	aws ecr get-login-password --region $(aws_region) | docker login --username AWS --password-stdin $(aws_id).dkr.ecr.$(aws_region).amazonaws.com
	docker push $(aws_id).dkr.ecr.$(aws_region).amazonaws.com/${repo_name}:latest

run:
	docker run -p 3000:3000 --env-file ./.env $(aws_id).dkr.ecr.$(aws_region).amazonaws.com/${repo_name}:latest 

image := public.ecr.aws/${pub_alias}/${repo_name}:latest

build-public:
	docker build --platform ${platform} -t ${image} .

login-public:
	aws ecr-public get-login-password --region ${pub_region} \
	| docker login --username AWS --password-stdin public.ecr.aws

push-public: login-public
	docker push ${image}