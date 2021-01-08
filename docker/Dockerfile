FROM public.ecr.aws/lambda/python:3.8

# This container needs at least 256MB memory, so need to change the default
# settings on the lambda.

ARG FUNCTION_DIR="/var/task"
RUN mkdir -p ${FUNCTION_DIR}

RUN yum -y install mesa-libGL

RUN pip install --upgrade pip
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install opencv-python
RUN pip install tqdm

COPY python/model_lambda.py ${FUNCTION_DIR}
COPY python/main.py ${FUNCTION_DIR}
COPY python/cnn.py ${FUNCTION_DIR}
COPY python/model_data.py ${FUNCTION_DIR}

COPY docker/model-2021-01-06_16.57.31.pt ${FUNCTION_DIR}
COPY docker/10017.jpg ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}
CMD ["model_lambda.lambda_handler"]
