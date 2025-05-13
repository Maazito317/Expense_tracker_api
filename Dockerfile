# Dockerfile
FROM python:3.11-slim

# 1) Set working directory
WORKDIR /app

# 2) Copy only requirements first (cache layer)
COPY requirements.txt .

# 3) Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the rest of your code
COPY . .

# 5) Default to bash so you can override with 'docker-compose run tester <cmd>'
CMD ["bash"]
