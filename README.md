# Project 25 — Docker Disaster Recovery Lab

A containerized Todo API built with Docker, Docker Compose, FastAPI, MySQL, and Nginx.

## Architecture

```text
Client
  |
  v
Nginx :80
  |
  v
FastAPI Backend :8000
  |
  v
MySQL :3306
  |
  v
Docker Volume
