# Data Model: Local Kubernetes Deployment for Todo AI Chatbot

**Feature**: 001-k8s-minikube-deployment
**Date**: 2026-02-05

## Kubernetes Resources

### 1. Deployment

**Definition**: Represents a set of identical Pods with no unique identities
**Fields**:
- apiVersion: apps/v1
- kind: Deployment
- metadata: name, labels, annotations
- spec: replicas, selector, template (Pod template)

**Relationships**: Connected to Service via label selectors

### 2. Service

**Definition**: An abstract way to expose an application running on a set of Pods
**Fields**:
- apiVersion: v1
- kind: Service
- metadata: name, labels
- spec: selector, ports, type

**Relationships**: Selects Pods from corresponding Deployment

### 3. ConfigMap

**Definition**: Stores non-confidential data in key-value pairs
**Fields**:
- apiVersion: v1
- kind: ConfigMap
- metadata: name, namespace
- data: configuration key-value pairs

**Relationships**: Referenced by Deployments for configuration

### 4. Secret

**Definition**: Objects of roughly the same size as unix passwords
**Fields**:
- apiVersion: v1
- kind: Secret
- metadata: name, namespace
- data: base64 encoded secret data

**Relationships**: Referenced by Deployments for sensitive configuration

## Helm Chart Structure

### 1. Chart.yaml

**Definition**: Contains metadata about the chart
**Fields**:
- name: chart name
- version: chart version
- description: chart description
- apiVersion: Helm API version

### 2. values.yaml

**Definition**: Contains default values for templates
**Fields**:
- image: repository, tag, pullPolicy
- service: type, port
- resources: limits and requests
- replicaCount: number of desired pods

### 3. Template Files

**Definition**: Kubernetes manifest templates with Helm templating
**Files**:
- deployment.yaml: Pod deployment configuration
- service.yaml: Service configuration
- ingress.yaml: Optional ingress configuration
- _helpers.tpl: Template helper functions

## Container Configuration

### 1. Dockerfile Elements

**Definition**: Instructions for building container images
**Elements**:
- Base image specification
- Dependency installation
- Application code copying
- Port exposure
- Startup command

### 2. Environment Variables

**Definition**: Configuration passed to running containers
**Variables**:
- BACKEND_URL: URL for backend service
- DATABASE_URL: Database connection string
- API_KEYS: Various API authentication keys