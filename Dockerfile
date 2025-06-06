FROM python:3.9-slim

# Set working directory
WORKDIR /usr/src/app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create outputs directory
RUN mkdir -p outputs

# Set Python path to include app directory
ENV PYTHONPATH=/usr/src/app

# Default command (can be overridden by docker-compose or docker run)
CMD ["python", "app/main.py", "--help"] 