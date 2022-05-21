# https://hub.docker.com/_/python
FROM python:3.9-alpine

# the only Python dependency is pygraphviz.
# pygraphviz depends on graphviz
# graphviz depends on gcc?

# https://pkgs.alpinelinux.org/package/edge/community/x86/py3-pygraphviz
# https://github.com/pygraphviz/pygraphviz/issues/141

RUN apk add --no-cache py3-pygraphviz graphviz graphviz-dev gcc musl-dev make

COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt

WORKDIR /scratch
