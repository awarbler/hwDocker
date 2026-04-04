# Hello Microservice Runbook

This guide shows the complete setup and exact command order to build, push, deploy, update, verify, and roll back this microservice.

## Project Structure

```
hello-microservice/
  .github/
    workflows/
      docker.yml
  app.py
  Dockerfile
  requirements.txt
  k8s/
    deployment.yaml
    service.yaml
```

Important:
1. Docker commands must run from project root (`hello-microservice`).
2. Kubernetes YAML files live in `k8s/`.

## Prerequisites

1. Docker Desktop is running.
2. Kubernetes is enabled in Docker Desktop.
3. `kubectl` is installed and configured.
4. You can push to Docker Hub (`txwarbler/hello-microservice`).

Verify environment:

```bash
docker --version
kubectl version --client
kubectl get nodes
```

## A) First-Time Setup and Run (From Scratch)

### 1) Go to project root

```bash
cd hello-microservice
```

### 2) Build and push version 1.0

```bash
docker build -t txwarbler/hello-microservice:1.0 .
docker push txwarbler/hello-microservice:1.0
```

### 3) Deploy to Kubernetes

From project root:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/hello-microservice
```

### 4) Find NodePort and test

```bash
kubectl get svc hello-microservice-service
```

Then test with the listed NodePort (example `31654`):

```bash
curl http://localhost:31654
curl http://localhost:31654/health
```

Expected response:

```json
{"message":"Hello from version 1!"}
```

## B) Release a New Version (2.0)

### 1) Edit app message

In `app.py`, set the default message to version 2.

### 2) Build and push new image

```bash
cd hello-microservice
docker build -t txwarbler/hello-microservice:2.0 .
docker push txwarbler/hello-microservice:2.0
```

### 3) Update Kubernetes deployment

Choose one method.

Method 1: update image in `k8s/deployment.yaml`, then apply:

```bash
kubectl apply -f k8s/deployment.yaml
```

Method 2: update image directly from CLI:

```bash
kubectl set image deployment/hello-microservice hello-microservice=txwarbler/hello-microservice:2.0
```

### 4) Verify rollout and response

```bash
kubectl rollout status deployment/hello-microservice
NODE_PORT=$(kubectl get svc hello-microservice-service -o jsonpath='{.spec.ports[0].nodePort}')
curl http://localhost:$NODE_PORT
```

Expected response:

```json
{"message":"Hello from version 2!"}
```

## C) Roll Back

```bash
kubectl rollout undo deployment/hello-microservice
kubectl rollout status deployment/hello-microservice
NODE_PORT=$(kubectl get svc hello-microservice-service -o jsonpath='{.spec.ports[0].nodePort}')
curl http://localhost:$NODE_PORT
```

To inspect revision history:

```bash
kubectl rollout history deployment/hello-microservice
```

## D) Run What You Have Right Now (Quick Verify)

If your service is already deployed, run this from any folder:

```bash
kubectl get deployment hello-microservice
NODE_PORT=$(kubectl get svc hello-microservice-service -o jsonpath='{.spec.ports[0].nodePort}')
echo $NODE_PORT
curl http://localhost:$NODE_PORT
curl http://localhost:$NODE_PORT/health
```

## E) Common Path Mistakes

1. `kubectl apply -f deployment.yaml` fails in project root.
Cause: file is in `k8s/`.
Fix: use `kubectl apply -f k8s/deployment.yaml`.

2. `docker build` fails in `k8s/` with missing Dockerfile.
Cause: Dockerfile is in project root.
Fix: run `docker build ...` from `hello-microservice`.

## F) Useful Debug Commands

```bash
kubectl get deployments
kubectl get pods -o wide
kubectl get svc
kubectl describe deployment hello-microservice
kubectl logs deployment/hello-microservice
kubectl rollout restart deployment hello-microservice
```

## G) Future Work (Cleaner Setup for Reliable Runs)

The project works now, but these improvements will make it easier for graders and teammates to run without path errors.

1. Move project to a path without spaces.
Reason: paths like `homework /HwDocker` are easy to mistype in terminal commands.
Suggested path: `~/ECECloud/HwDocker/hello-microservice`.

2. Keep all Kubernetes files grouped under one directory with optional overlays.
Example structure:

```text
hello-microservice/
  app.py
  Dockerfile
  requirements.txt
  k8s/
    base/
      deployment.yaml
      service.yaml
    overlays/
      dev/
      prod/
```

3. Add one-command scripts so users do not need to remember command order.
Example scripts:
1. `scripts/build_push.sh <tag>`
2. `scripts/deploy.sh`
3. `scripts/rollback.sh`

4. Add a `Makefile` with standard targets.
Suggested targets:
1. `make build TAG=2.0`
2. `make push TAG=2.0`
3. `make deploy`
4. `make verify`
5. `make rollback`

5. Add `.env.example` and read environment variables in deployment.
Reason: avoid editing code for simple message/config updates.

6. Add health probes in Kubernetes deployment.
Reason: improves startup reliability and self-healing behavior.

7. Enhance existing CI/CD (GitHub Actions).
Pipeline goal:
1. Build image
2. Run lint/tests
3. Push tagged image
4. Optionally deploy to cluster

8. Add a short `grading-checklist.md` file.
Include copy-paste steps for:
1. Fresh deploy
2. Version update
3. Rollback
4. Expected curl responses