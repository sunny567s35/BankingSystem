FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt . 

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Set working directory for React frontend
WORKDIR /app/my-app  
# Install React dependencies
RUN npm install
RUN npm install bootstrap
RUN npm install react-scripts
RUN npm install @fortawesome/fontawesome-free

# Expose ports for Django (8000), React (3000), and Prometheus (9090)
EXPOSE 8000 9090 3000

# Ensure Prometheus config directory exists
RUN mkdir -p /etc/prometheus
COPY prometheus/prometheus-config.yaml /etc/prometheus/prometheus.yml

# Set working directory back to Django
WORKDIR /app

# Start both React and Django using a process manager
CMD ["sh", "-c", "cd my-app && npm start & python manage.py runserver 0.0.0.0:8000"]