aws_id := 471112781958
aws_region := us-east-1
repo_name := tti-front-end
platform := linux/arm64

build-docker:
	docker build --platform ${platform} -t $(aws_id).dkr.ecr.$(aws_region).amazonaws.com/${repo_name}:latest .

push:
	aws ecr get-login-password --region $(aws_region) | docker login --username AWS --password-stdin $(aws_id).dkr.ecr.$(aws_region).amazonaws.com
	docker push $(aws_id).dkr.ecr.$(aws_region).amazonaws.com/${repo_name}:latest

run:
	docker run -p 3000:3000 $(aws_id).dkr.ecr.$(aws_region).amazonaws.com/${repo_name}:latest 