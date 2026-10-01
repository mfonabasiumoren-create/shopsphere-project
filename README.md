# ShopSphere - Cloud-Native E-Commerce Platform



ShopSphere is a hands-on Cloud Engineering and DevOps project that demonstrates the design, containerization, automation, and deployment of a scalable e-commerce application using AWS and modern DevOps practices.



The project is being developed progressively from a locally running Flask and MySQL application into a cloud-native architecture using Docker, Amazon ECR, Terraform, Kubernetes, and Amazon EKS.



## Project Objectives



The project is designed to demonstrate practical experience with:



- Building a REST API with Python Flask and MySQL

- Designing secure and highly available AWS infrastructure

- Containerizing applications with Docker

- Managing container images with Amazon Elastic Container Registry (ECR)

- Provisioning cloud infrastructure using Terraform

- Deploying and managing containerized workloads with Kubernetes

- Implementing load balancing and application scalability

- Managing application configuration and secrets securely

- Building toward automated CI/CD deployment with GitHub Actions

- Implementing monitoring, observability, and failure recovery



## Current Project Status



ShopSphere is currently under active development.



Completed so far:



- Flask product and order management API

- MySQL database integration and persistent data storage

- Reproducible database initialization schema

- Docker containerization

- Amazon ECR private container repository and image push

- Kubernetes Deployment and Service manifests

- Kubernetes ConfigMap for application configuration

- Terraform provider configuration and initialization



In progress:



- AWS network infrastructure using Terraform

- Amazon EKS infrastructure

- Kubernetes deployment to AWS

- Secure database credential management

- CI/CD automation

- Monitoring, autoscaling, and failure testing



## Target Architecture



ShopSphere is being designed around a highly available, multi-tier AWS architecture.



```text

Users

&#x20; |

&#x20; v

Route 53

&#x20; |

&#x20; v

Application Load Balancer

&#x20; |

&#x20; v

Amazon EKS / Kubernetes

&#x20; |

&#x20; +-----------------------+

&#x20; |                       |

&#x20; v                       v

ShopSphere API        Multiple Pod Replicas

&#x20; |

&#x20; v

Amazon RDS MySQL



Supporting Services:

- Amazon ECR - Container image registry

- Amazon S3 - Product/static asset storage

- AWS Secrets Manager - Secure credential management

- Amazon CloudWatch - Monitoring and logging

- Terraform - Infrastructure provisioning

- GitHub Actions - CI/CD automation

```



## Technology Stack



| Category | Technologies |

| --- | --- |

| Cloud Platform | Amazon Web Services (AWS) |

| Compute | Amazon EC2, Amazon EKS |

| Networking | Amazon VPC, Subnets, Route Tables, Internet Gateway, NAT Gateway, Security Groups, Application Load Balancer |

| Containers | Docker, Amazon ECR |

| Orchestration | Kubernetes |

| Infrastructure as Code | Terraform |

| Configuration Management | Ansible |

| Backend | Python, Flask |

| Database | MySQL, Amazon RDS |

| Operating System | Linux / Ubuntu |

| Automation | Bash, Cron |

| Version Control | Git, GitHub |

| CI/CD | GitHub Actions (planned) |

| Monitoring | Amazon CloudWatch (planned) |

| Secrets | AWS Secrets Manager (planned) |

## Repository Structure

```text
shopsphere-project/
|
+-- app/
|   +-- app.py
|   +-- requirements.txt
|   +-- Dockerfile
|   +-- .dockerignore
|   +-- database/
|       +-- init.sql
|
+-- kubernetes/
|   +-- api-deployment.yaml
|   +-- api-service.yaml
|   +-- api-configmap.yaml
|
+-- terraform/
|   +-- providers.tf
|   +-- .terraform.lock.hcl
|
+-- docs/
|   +-- architecture.md
|
+-- .gitignore
+-- README.md
```

### Directory Purpose

- **app/** - Contains the Flask API, Python dependencies, Docker configuration, and database initialization schema.
- **kubernetes/** - Contains Kubernetes manifests for deploying and exposing the ShopSphere API and managing non-sensitive application configuration.
- **terraform/** - Contains Infrastructure as Code configuration for provisioning ShopSphere AWS infrastructure.
- **docs/** - Contains supporting project and architecture documentation.

## Security & Engineering Decisions

ShopSphere is being developed with security, maintainability, and infrastructure reproducibility in mind.

- Application credentials are not hard-coded into the source code.
- Local database credentials are loaded through environment variables using a `.env` file that is excluded from Git.
- Sensitive credentials are not stored in Kubernetes ConfigMaps.
- AWS Secrets Manager is planned for secure credential management in the cloud environment.
- Database access is designed to be restricted to the application tier rather than exposed publicly.
- Application workloads are intended to run in private subnets behind an internet-facing Application Load Balancer.
- Infrastructure is being defined with Terraform to make cloud resources reproducible and version-controlled.
- Docker provides a consistent application runtime between development and deployment environments.
- Kubernetes manifests separate application deployment, networking, and non-sensitive configuration.
- Multiple application replicas and load balancing are planned to improve availability and resilience.

## Running ShopSphere Locally

### Prerequisites

Before running the application locally, ensure the following are installed:

- Python 3
- MySQL
- Git
- Docker (optional for containerized execution)

### 1. Clone the Repository

```bash
git clone https://github.com/mfonabasiumoren-create/shopsphere-project.git
cd shopsphere-project/app
```

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Database

Create a MySQL database named:

```text
shopsphere
```

Then execute the database initialization script located at:

```text
app/database/init.sql
```

Create an `.env` file inside the `app` directory using the following structure:

```env
DB_HOST=localhost
DB_NAME=shopsphere
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

Do not commit the `.env` file or real database credentials to Git.

### 5. Start the Application

```bash
python app.py
```

The ShopSphere API will run on:

```text
http://localhost:8080
```

### 6. Run with Docker

Build the container image from the `app` directory:

```bash
docker build -t shopsphere-api .
```

Run the container while connecting it to a MySQL instance running on the host machine:

```bash
docker run --name shopsphere-api-container -p 8080:8080 --env-file .env -e DB_HOST=host.docker.internal shopsphere-api
```

The API will then be available at:

```text
http://localhost:8080
```

## API Endpoints

The current ShopSphere backend provides REST API endpoints for managing products and customer orders.

### Products

#### Get All Products

```http
GET /products
```

Returns the products currently stored in the ShopSphere MySQL database.

#### Get a Product

```http
GET /products/{product_id}
```

Returns a specific product using its product ID.

Example:

```http
GET /products/2
```

### Orders

#### Get All Orders

```http
GET /orders
```

Returns existing orders together with associated product information.

#### Create an Order

```http
POST /orders
```

Example request body:

```json
{
  "product_id": 2,
  "quantity": 2
}
```

When an order is successfully created, the application:

- Validates the requested product.
- Checks the available product stock.
- Calculates the order total.
- Creates the order in MySQL.
- Reduces the corresponding product stock.
- Uses a database transaction to maintain data consistency.

## Example API URLs

When running ShopSphere locally:

```text
http://localhost:8080/products
```

```text
http://localhost:8080/products/2
```

```text
http://localhost:8080/orders
```

## Project Roadmap

ShopSphere is being developed incrementally to demonstrate the progression from local application development to production-oriented cloud deployment.

- [x] Build Flask product and order API
- [x] Integrate MySQL persistent storage
- [x] Create reproducible database initialization schema
- [x] Containerize the application with Docker
- [x] Push the container image to Amazon ECR
- [x] Create Kubernetes Deployment and Service manifests
- [x] Externalize non-sensitive configuration using Kubernetes ConfigMap
- [x] Initialize Terraform and configure the AWS provider
- [ ] Provision AWS VPC and networking with Terraform
- [ ] Provision Amazon RDS MySQL
- [ ] Provision Amazon EKS
- [ ] Deploy ShopSphere containers to Kubernetes
- [ ] Integrate AWS Secrets Manager
- [ ] Configure application ingress and load balancing
- [ ] Implement Kubernetes Horizontal Pod Autoscaling
- [ ] Configure monitoring and centralized logging
- [ ] Build CI/CD pipeline with GitHub Actions
- [ ] Configure Route 53 and HTTPS with AWS Certificate Manager
- [ ] Perform resilience and failure-recovery testing

## What This Project Demonstrates

ShopSphere is intended to demonstrate practical Cloud Engineering and DevOps skills across:

- Cloud architecture and AWS networking
- Linux-based application deployment
- Containerization and container registries
- Infrastructure as Code
- Kubernetes orchestration
- Database integration
- Application and infrastructure security
- High availability and scalability
- CI/CD automation
- Monitoring and observability
- Technical documentation and version control

## Author

**Mfonabasi Umoren**

B.Eng. Computer Engineering
Cloud Engineering Student - AltSchool Africa
Cloud Engineering / DevOps Intern

GitHub: https://github.com/mfonabasiumoren-create

---

This repository documents my hands-on Cloud Engineering and DevOps learning journey. The project is continuously improved as additional infrastructure, automation, security, and deployment components are implemented.
