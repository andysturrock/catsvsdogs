FROM public.ecr.aws/lambda/python:3.8

ARG FUNCTION_DIR="/function"
RUN mkdir -p ${FUNCTION_DIR}

COPY python/requirements.txt ${FUNCTION_DIR}

RUN /bin/curl --output .//Miniconda3-latest-Linux-x86_64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

RUN /bin/bash ./Miniconda3-latest-Linux-x86_64.sh -b
RUN /root/miniconda3/bin/conda install -y --file ${FUNCTION_DIR}/requirements.txt -c conda-forge -c pytorch
RUN yum -y install mesa-libGL

RUN /root/miniconda3/bin/pip install --target ${FUNCTION_DIR} awslambdaric

COPY python/model_lambda.py ${FUNCTION_DIR}
COPY python/main.py ${FUNCTION_DIR}
COPY python/cnn.py ${FUNCTION_DIR}
COPY python/model_data.py ${FUNCTION_DIR}

COPY docker/model-2021-01-06_16.57.31.pt ${FUNCTION_DIR}
COPY docker/10017.jpg ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}
ENTRYPOINT [ "/root/miniconda3/bin/python", "-m", "awslambdaric" ]
CMD ["model_lambda.lambda_handler"]
