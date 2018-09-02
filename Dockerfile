FROM gcr.io/google-appengine/python
LABEL python_version=python

#RUN virtualenv --no-download /env -p python
# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate
#ENV VIRTUAL_ENV /env
#ENV PATH /env/bin:$PATH

RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  python-gdal \
  python-opencv

RUN pip install flask gunicorn

EXPOSE 8080

ADD . /app/
CMD gunicorn -b :8080 main:app
