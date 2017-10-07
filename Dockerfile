FROM heroku/miniconda

# Get requirements.txt
ADD ./webapp/requirements.txt /tmp/requirements.txt

# Install packages
RUN pip install -qr /tmp/requirements.txt

# Add web app
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

# Start web server
CMD gunicorn --threads 20 --bind 0.0.0.0:$PORT --timeout 120 wsgi
