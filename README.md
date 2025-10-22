# Human Resource Management Sysytem



## Overview

A lightweight Human Resource Management System (HRMS) for tracking employees, roles, attendance, and basic payroll functions. Designed to be modular, easy to deploy, and adaptable to different organization sizes.

Key goals:
- Centralize employee records and role management
- Provide attendance and leave tracking
- Offer simple payroll calculations and reporting
- Be extensible and easy to integrate with other services

## Features

- Employee profiles (create, read, update, delete)
- Role and permission management
- Attendance logging and leave requests
- Payroll summary and exportable reports (CSV/PDF)
- Audit logs for changes
- RESTful API and web UI

## Tech stack

- Backend: Django
- Database: PostgreSQL (Production) /SQLite (development)
- Frontend: server-rendered templates
- Auth: ession-based authentication
- Optional: Docker for containerized deployments

## Prerequisites

Install the required tools for your chosen stack:

- Python 3.8+ and pip (if Django/Flask)
- PostgreSQL/SQLite Db
- Docker (optional)

## Setup

1. Clone the repository
    ```
    git clone git@github.com:xanorbkid/HRIS_project.git
    cd <repo-directory>
    ```

2. Configure environment variables
    - Copy the example env file and update values:
      ```
      cp .env.example .env
      ```
    - Set database connection, secret keys, and any third-party credentials.

3. Install dependencies
    
    - Python:
      ```
      pip install -r requirements.txt
      ```


4. Database setup
    - Create the database and run migrations:
      ```
      # Django equivalent commands
     
      python manage.py migrate
    
      ```

5. Seed sample data (optional)
    ```
   
    python manage.py loaddata sample_data.json
    ```

## Running the application

- Development:
  ```

  python manage.py runserver

  ```
- Access the web UI at http://127.0.0.1:8000 (or configured port).

## Testing

- Run unit and integration tests:
  ```
  
  pytest
 
  ```

## Deployment

- Docker:
  ```
  docker build -t hrms-app .
  docker run -e ENV_FILE=.env -p 80:80 hrms-app
  ```
- Use CI/CD to build images and deploy to your cloud provider (AWS, Azure, GCP, or on-prem).

## Configuration & Maintenance

- Back up the database regularly.
- Rotate secret keys and credentials.
- Monitor application logs and set up alerts for errors and performance issues.

## Contributing

- Fork the repository and create a feature branch.
- Follow the coding standards and add tests for new features.
- Open a pull request with a clear description and related issue reference.

## License

Specify the project license in LICENSE file (e.g., MIT, Apache-2.0).

## Conclusion

This HRMS provides a foundation for managing core HR workflows. Customize modules, extend integrations, and automate payroll/reporting to match organizational needs.
