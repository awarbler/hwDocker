"""
Anita Woodford (AJW4987)
Creating and Publishing a Microservice with Docker
Cloud Native App Development
Instructor: Abhay Samant, Prof. of Practice, UT-ECE
April 3, 2026
"""
import os
from fastapi import FastAPI
import logging #hw extension

# A simple FastAPI application that serves as a microservice. 
# It has two endpoints: the root endpoint ("/") that returns 
# a greeting message, and a health check endpoint ("/health")
# that returns the status of the service. This is a common 
# pattern for microservices to allow for easy monitoring 
# and health checks.

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")

def read_root():
    #return {"message": "Hello from a Dockerized microservice!"}
    logging.info("Root endpoint was called")
    #return {"message": os.getenv("SERVICE_NAME", "Hello from default")}
    #return {"message": os.getenv("SERVICE_NAME", "Hello from version 1!")}
    return {"message": os.getenv("SERVICE_NAME", "Hello from version 2!")}

# Health endpoint (real-world microservice pattern)
@app.get("/health")
def health_check():
    return {"status": "ok"}
