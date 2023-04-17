FROM public.ecr.aws/lambda/python:3.8.12

COPY amplify/backend/function/chatGPTLineChatBotFunction/requirements.txt .
RUN pip install -r requirements.txt

COPY amplify/backend/function/chatGPTLineChatBotFunction/src/my_package /var/task/my_package

CMD ["my_package.index.handler"]