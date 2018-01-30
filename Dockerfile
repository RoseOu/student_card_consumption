FROM python:2.7

ENV DEPLOY_PATH /stdcc
RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH
Add requirement.txt requirement.txt

RUN pip install --index-url http://pypi.doubanio.com/simple/ -r requirements.txt --trusted-host=pypi.doubanio.com

Add . .
