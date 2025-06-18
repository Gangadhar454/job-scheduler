# Scheduler Microservice

## Overview
This is a Django-based scheduler microservice for managing and executing jobs with customizable scheduling using CRON expressions. It supports job creation, listing, and detailed retrieval via RESTful APIs. The service uses APScheduler for job scheduling, PostgreSQL for persistent storage, and Redis for caching. Jobs can be scheduled using standard CRON expressions (e.g., `0 9 * * 1` for every Monday at 9 AM, `0 9 1 * *` for every 1st of the month at 9 AM). The application is containerized using Docker for easy deployment and scalability.

## Setup Instructions
### Prerequisites
- Docker and Docker Compose
- Git

### Docker Setup
1. **Clone Repository**:
   ```bash
   git clone https://github.com/Gangadhar454/job-scheduler.git
   cd job-scheduler
   ```

2. **Build and Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:
   - API: `http://localhost:8000/scheduler/`
   - Swagger UI: `http://localhost:8000/swagger/`

## Access APIs
- **Endpoints**:
  - `GET /scheduler/jobs/`: List all jobs
  - `GET /scheduler/jobs/<id>/`: Get job details
  - `POST /scheduler/jobs/`: Create a new job

## Example Job Creation
### Every Monday at 9 AM
```bash
curl -X POST http://localhost:8000/scheduler/jobs/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Monday Email",
    "description": "Send weekly newsletter every Monday at 9 AM",
    "cron_expression": "0 9 * * 1",
    "start_time": "2025-06-23T09:00:00Z",
    "parameters": {"action": "send_email", "recipient": "user@example.com"}
}'
```

### Every 1st of the Month at 9 AM
```bash
curl -X POST http://localhost:8000/scheduler/jobs/ \
-H "Content-Type: application/json" \
-d '{
    "name": "Monthly Report",
    "description": "Generate report on the 1st of every month at 9 AM",
    "cron_expression": "0 9 1 * *",
    "start_time": "2025-07-01T09:00:00Z",
    "parameters": {"action": "generate_report", "type": "monthly"}
}'
```

## Scaling Strategy
To handle ~10,000 users, ~1,000 services, and ~6,000 API requests per minute:

1. **Horizontal Scaling**:
   - Deploy multiple Django containers using Docker Compose or Kubernetes behind a load balancer (e.g., NGINX, AWS ALB).
   - Use Kubernetes for auto-scaling based on CPU/memory usage.

2. **Database Optimization**:
   - Use PostgreSQL with connection pooling (e.g., PgBouncer) to handle concurrent connections.
   - Implement read replicas for read-heavy operations (GET /jobs).
   - Indexes on `next_run` and `is_active` fields (already included).

3. **Job Scheduling**:
   - Offload job execution to a distributed task queue (e.g., Celery with Redis/RabbitMQ) for high-volume jobs.

4. **Caching**:
   - Use Redis for caching frequent GET requests.
   - Cache job listings and details with a TTL of ~1 minute.

5. **API Rate Limiting**:
   - Use Django REST Framework's throttling to limit API abuse.
   - Implement rate limits per user/IP to ensure fair usage.

6. **Asynchronous Processing**:
   - Use async views or Celery for POST requests to handle job creation efficiently.
   - Process job execution in background workers to prevent API bottlenecks.

## Development Notes
- **SOLID Principles**:
  - Single Responsibility: Each module (models, services, views) has a distinct role.
  - Open/Closed: JobScheduler supports any valid CRON expression.
  - Liskov Substitution: Ensured in serializer/model design.
  - Interface Segregation: API endpoints are focused and specific.
  - Dependency Inversion: JobScheduler abstracts scheduling logic.

- **Performance**:
  - Indexes on `next_run` and `is_active` for efficient queries.
  - Pagination for job listing to handle large datasets.
  - Redis caching for frequent API calls.

- **API Documentation**:
  - Swagger UI via drf-yasg for interactive API exploration.

- **Configurable Scheduling**:
  - Uses `cron_expression` field for standard 5-field CRON patterns.
  - Validates CRON expressions with `croniter`.

- **Dockerization**:
  - `Dockerfile` uses a slim Python image with Gunicorn for production.
  - `docker-compose.yml` orchestrates Django, PostgreSQL, and Redis services.
  - `wait-for.sh` ensures the database is ready before migrations and application start.
  - Environment variables for flexible configuration.

- **Fix for Migration Issue**:
  - Modified `jobs/apps.py` to skip `reschedule_all_jobs` during `migrate` or `makemigrations` commands, preventing premature database queries.

## Future Improvements
- Add authentication/authorization for secure job management.
- Implement job history tracking.
- Integrate Celery for distributed job execution.
