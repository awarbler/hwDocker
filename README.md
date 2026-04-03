Tools
•
Python + FastAPI for the microservice (simple, modern, and readable)
•
Docker for containerization
•
Docker Hub for publishing
Tutorial: Creating and Publishing a Microservice with Docker
Learning Objectives
By the end of this tutorial, students will be able to:
1.
Build a simple microservice
2.
Package it into a Docker container
3.
Run and test the container locally
4.
Publish the container to a public registry (Docker Hub)
Prerequisites
Students should have:
•
Docker Desktop installed https://www.docker.com/products/docker-desktop
•
A Docker Hub account https://hub.docker.com
•
Basic familiarity with command line and Python
Verify installation:
1 docker --version
Step 1: Create the Microservice
1.1 Project Structure
Create a new directory:
1 mkdir hello-microservice
2 cd hello-microservice
Project layout:
1 hello-microservice/
2 │── app.py
3 │── requirements.txt
4 │── Dockerfile
1.2 Write the Microservice (app.py)
This is a stateless REST microservice, ideal for teaching microservice principles.
1 from fastapi import FastAPI
2
3 app = FastAPI()
4
5 @app.get("/")
6 def read_root():
7 return {"message": "Hello from a Dockerized microservice!"}
8
9 @app.get("/health")
10 def health_check():
11 return {"status": "ok"}
Key teaching point:
•
REST API
•
Stateless design
•
Health endpoint (real-world microservice pattern)
1.3 Define Dependencies (requirements.txt)
1 fastapi
2 uvicorn
Step 2: Run the Microservice Locally (Without Docker)
Install dependencies:
1 pip install -r requirements.txt
Run the service:
1 uvicorn app:app --host 0.0.0.0 --port 8000
Test in browser or with curl:
1 curl http://localhost:8000
This step demonstrates that the app works before containerizing and Debugging is easier outside Docker
Step 3: Create the Dockerfile
Create a file named Dockerfile (no extension):
1 # 1. Base image
2 FROM python:3.11-slim
3
4 # 2. Set working directory
5 WORKDIR /app
6
7 # 3. Copy dependency file
8 COPY requirements.txt .
9
10 # 4. Install dependencies
11 RUN pip install --no-cache-dir -r requirements.txt
12
13 # 5. Copy application code
14 COPY app.py .
15
16 # 6. Expose port
17 EXPOSE 8000
18
19 # 7. Start the microservice
20 CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
Teaching Highlights
•
Layered filesystem
•
Reproducible builds
•
Difference between COPY, RUN, CMD
•
Why 0.0.0.0 is required in containers
Step 4: Build the Docker Image
From the project directory:
1 docker build -t hello-microservice .
Verify:
1 docker images
Step 5: Run the Container Locally
1 docker run -p 8000:8000 hello-microservice
Test again:
1 curl http://localhost:8000
2 curl http://localhost:8000/health
Explain:
•
-p host:container
•
Difference between container vs host networking
Step 6: Remove the Container Locally
Find the id of the running container:
1 docker ps -a
Delete the corresponding container:
1 docker rm <container_id>
Step 7: Tag the Image for Docker Hub
Log in:
1 docker login
Tag the image:
1 docker tag hello-microservice <dockerhub-username>/hello-microservice:1.0
Example:
1 docker tag hello-microservice abhay123/hello-microservice:1.0
Step 8: Publish the Image to Docker Hub
Push the image:
1 docker push <dockerhub-username>/hello-microservice:1.0
Verify on Docker Hub:
•
Repository becomes publicly visible
•
Students can pull it anywhere
Step 9: Pull and Run from Docker Hub (Anywhere)
On any machine with Docker:
1 docker pull <dockerhub-username>/hello-microservice:1.0
2 docker run -p 8000:8000 <dockerhub-username>/hello-microservice:1.0
This demonstrates true portability—a core Docker concept.
Step 10: Microservice Best Practices (Discussion Slide)
Single responsibility Stateless design Explicit dependencies Health check endpoint Versioned images (:1.0, :2.0) Easy horizontal scaling (Docker/Kubernetes)
[HW] scaling demo:
1 docker run -p 8001:8000 <image>
2 docker run -p 8002:8000 <image>
HW Extensions
•
Add environment variables (ENV, --env)
•
Add logging
•
Add .dockerignore
•
Convert to multi-stage build
•
Deploy to Kubernetes (next lecture!)
•
Add CI/CD with GitHub Actions
Summary
“A microservice is just an application that becomes portable, scalable, and deployable once you put it in a container.”
This tutorial cleanly bridges: Application → Container → Registry → Deployment
Next is a Kubernetes follow‑on module, assuming students already completed your Docker microservice lab.
Follow‑On Module: Deploying a Microservice with Kubernetes
Module Overview
Goal: Students will take the Dockerized microservice they already built and deploy, expose, scale, and manage it using Kubernetes.
Core idea to emphasize:
Docker packages applications. Kubernetes runs applications at scale.
Learning Objectives
By the end of this module, students will be able to:
1.
Explain core Kubernetes concepts (Pod, Deployment, Service)
2.
Deploy a containerized microservice to a Kubernetes cluster
3.
Expose the microservice using a Service
4.
Scale the microservice replicas
5.
Perform rolling updates
6.
Inspect and debug running workloads
Prerequisites
Students should already have:
•
The published Docker image
•
Docker Desktop installed with Kubernetes enabled
•
kubectl installed and configured
Verify cluster access:
1 kubectl version --client
2 kubectl get nodes
Part 1: Kubernetes Mental Model (Lecture)
Key Objects (Conceptual Slide) Object Purpose
Pod
Smallest deployable unit (one or more containers)
Deployment
Manages replicated Pods and updates
Service
Stable network endpoint
ReplicaSet
Ensures desired Pod count
Namespace
Logical isolation
Emphasize:
•
You never manage Pods directly
•
Desired state vs current state
•
Self-healing systems
Part 2: First Kubernetes Deployment
2.1 Create a Deployment YAML
Create a new directory:
1 mkdir k8s
2 cd k8s
Create deployment.yaml:
1 apiVersion: apps/v1
2 kind: Deployment
3 metadata:
4 name: hello-microservice
5 spec:
6 replicas: 1
7 selector:
8 matchLabels:
9 app: hello-microservice
10 template:
11 metadata:
12 labels:
13 app: hello-microservice
14 spec:
15 containers:
16 - name: hello-microservice
17 image: <dockerhub-username>/hello-microservice:1.0
18 ports:
19 - containerPort: 8000
Teaching Notes
•
YAML mirrors the desired state
•
spec.template defines the Pod
•
Labels connect everything together
2.2 Apply the Deployment
1 kubectl apply -f deployment.yaml
Check status:
1 kubectl get deployments
2 kubectl get pods
Inspect Pod:
1 kubectl describe pod <pod-name>
Part 3: Exposing the Microservice
3.1 Why We Need a Service
Explain:
•
Pods are ephemeral
•
IPs change
•
Services give stable networking
3.2 Create a Service YAML
Create service.yaml:
1 apiVersion: v1
2 kind: Service
3 metadata:
4 name: hello-microservice-service
5 spec:
6 selector:
7 app: hello-microservice
8 ports:
9 - protocol: TCP
10 port: 80
11 targetPort: 8000
12 type: NodePort
Apply it:
1 kubectl apply -f service.yaml
Check:
1 kubectl get services
3.3 Access the Application
For Docker Desktop:
1 kubectl get svc hello-microservice-service
Open browser:
1 http://localhost:<nodePort>
Test:
1 curl http://localhost:<nodePort>/health
Part 4: Scaling the Microservice
4.1 Manual Scaling
1 kubectl scale deployment hello-microservice --replicas=3
Verify:
1 kubectl get pods
Explain:
•
No code changes
•
Same container image
•
Horizontal scaling
4.2 Observe Load Distribution (Optional)
1 kubectl get pods -o wide
Explain kube-proxy and Service load balancing at a high level.
Part 5: Self-Healing Demonstration
Delete a Pod:
1 kubectl delete pod <pod-name>
Then:
1 kubectl get pods
Teaching moment:
Kubernetes notices deviation from desired state and fixes it automatically.
Part 6: Rolling Updates
6.1 Build Version 2 of the Image
Modify the response message:
1 return {"message": "Hello from version 2!"}
Build and push:
1 docker build -t <dockerhub-username>/hello-microservice:2.0 .
2 docker push <dockerhub-username>/hello-microservice:2.0
6.2 Update the Deployment
Edit deployment.yaml:
1 image: <dockerhub-username>/hello-microservice:2.0
Apply:
1 kubectl apply -f deployment.yaml
Watch rollout:
1 kubectl rollout status deployment hello-microservice
Explain:
•
Zero-downtime updates
•
Replica swapping
Part 7: Rollback (One-Command Magic)
1 kubectl rollout undo deployment hello-microservice
This is a great “wow” moment for students.
Part 8: Configuration via Environment Variables
Update Deployment:
1 env:
2 - name: SERVICE_NAME
3 value: "Hello Kubernetes"
Modify code:
1 import os
2 return {"message": os.getenv("SERVICE_NAME", "Hello")}
Demonstrate:
•
Dev vs prod configs
•
No image rebuild needed
Part 9: Debugging & Observability
Logs
1 kubectl logs <pod-name>
Exec into Container
1 kubectl exec -it <pod-name> -- /bin/sh
Describe Objects
1 kubectl describe deployment hello-microservice
Part 10: Clean Up
1 kubectl delete -f deployment.yaml
2 kubectl delete -f service.yaml
HW
Required
✅ Deploy microservice to Kubernetes ✅ Expose it with a Service ✅ Scale it to 3 replicas ✅ Perform rolling update to v2
Bonus
⭐ Add readiness & liveness probes ⭐ Use ClusterIP + kubectl port-forward ⭐ Add CPU requests/limits
Conceptual Summary Slide Docker Kubernetes
Builds images
Runs images
Single host
Clustered
Manual scaling
Automatic
One container
Many replicas
Docker answers “How do I package my app?” Kubernetes answers “How do I run my app reliably?”