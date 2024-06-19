FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

ENV workingDir=/app/

RUN mkdir -p ${workingDir}

WORKDIR ${workingDir}

COPY requirements.txt ${workingDir}

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Copy all the docker directory
COPY . ${workingDir}

RUN ln -snf /usr/share/zoneinfo/America/Caracas /etc/localtime && echo "America/Caracas" > /etc/timezone

EXPOSE 8080

ENTRYPOINT [ "/app/build.sh" ]