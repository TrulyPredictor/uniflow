# Backend Interview README

# Uniflow Application Documentation

## Setup and Installation Process:

1. **Clone the Repository:**
   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies:**
   Ensure you have Python, Flask, Celery, and other project dependencies installed. You can install them using the following commands:
   ```
   pip install flask celery
   ```

3. **Build Docker Image:**
   ```
   docker build -t uniflow-app .
   ```

4. **Run Docker Container:**
   ```
   docker run -p 5000:5000 uniflow-app
   ```

5. **Start Celery Worker (in a separate terminal):**
   ```
   celery -A api.celery worker --loglevel=info
   ```

## API Documentation:

### 7.1 Asynchronous RESTful Invocation of ExpandReduceFlow:

- **Endpoint:** `/async_run_expand_reduce_flow`
- **Method:** POST
- **Request Format:**
  ```json
  {
    "nodes": [
      {"name": "node1", "value_dict": {"key1": "value1"}},
      {"name": "node2", "value_dict": {"key2": "value2"}}
    ]
  }
  ```
- **Response Format:**
  ```json
  {
    "job_id": "unique_identifier"
  }
  ```
- **Example:**
  ```
  curl -X POST -H "Content-Type: application/json" -d '{"nodes": [{"name": "node1", "value_dict": {"key1": "value1"}}]}' http://127.0.0.1:5000/async_run_expand_reduce_flow
  ```

### 7.2 Synchronous RESTful Endpoint to Verify Async Call Status:

- **Endpoint:** `/check_status/<job_id>`
- **Method:** GET
- **Response Format:**
  ```json
  {
    "status": "pending/completed"
  }
  ```
- **Example:**
  ```
  curl http://127.0.0.1:5000/check_status/unique_identifier
  ```

### 7.3 Synchronous RESTful Endpoint to Retrieve All key-value Pairs:

- **Endpoint:** `/get_all_key_value_pairs`
- **Method:** GET
- **Response Format:**
  ```json
  {
    "key_value_pairs": [{"key": "value", ...}]
  }
  ```
- **Example:**
  ```
  curl http://127.0.0.1:5000/get_all_key_value_pairs
  ```
