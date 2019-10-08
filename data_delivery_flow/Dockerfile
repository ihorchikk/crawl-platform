ARG REGISTRY
ARG REPO
ARG TAG

FROM ${REGISTRY}/${REPO}-base:${TAG} as dc_scrapy_base

FROM dc_scrapy_base as dc_scrapy

RUN pip install --upgrade pip --no-cache-dir

COPY requirements/prod.txt /tmp/requirements/prod.txt

RUN pip install -r /tmp/requirements/prod.txt --no-cache-dir

COPY . /app
WORKDIR /app

ARG GIT_COMMIT

# saves GIT_COMMIT as a variable in a file in the image
RUN echo "__version__ = \"${GIT_COMMIT}\"" >> /app/competera/__init__.py

RUN pip install . --no-cache-dir

ENTRYPOINT ["scrapy"]
CMD ["allcrawlers", "--loglevel=WARNING"]
