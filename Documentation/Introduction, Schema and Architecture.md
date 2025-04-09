# 💳 BankingSystem

## 📌 Introduction

A modern banking institution needs a robust, secure, and scalable system to manage various banking operations such as customer onboarding, account management, transactions (deposit, withdrawal, transfer), user authentication, and support ticketing. The system must also maintain historical records for auditing and regulatory compliance.

**BankingSystem** is a robust, production-ready online banking application built using Django, React, MySQL, and modern DevOps tooling. It simulates core banking operations including account management, transactions, interest calculations, and user authentication. This project integrates modern SRE (Site Reliability Engineering) principles, ensuring high availability, observability, scalability, and operational efficiency.

The application architecture adopts a microservices-inspired modular design, allowing services like account management, transaction processing, interest calculations, and authentication to work independently and communicate seamlessly.


---

Team Contribution:
- Backend - Vishnu, Chaitanya, Sandeep
- Frontend - Sindhuja, Himaansh
- Dockerfile - Hema
- Kubernetes - Khushi, Himaansh
- Jenkins - Sandeep, Vishnu
- Prometheus & Grafana - Sindhuja, Khushi

---

## 🎯 Project Motivation

We chose to develop this **BankingSystem** project to challenge ourselves with:

- Designing a **complex, real-world domain** — banking — with interrelated models, transaction integrity, and strict consistency requirements.
- Practicing **Site Reliability Engineering (SRE)** principles by integrating:
  - Metrics and dashboards with **Prometheus + Grafana**
  - Scheduled background tasks via **Celery + Redis**
  - Continuous deployment with **Docker + Kubernetes**
- Developing a **fully containerized**, production-grade system with proper CI/CD workflows and optional cloud-native deployment.

This project not only strengthens backend and frontend development skills, but also enhances our understanding of infrastructure, observability, and production monitoring — key pillars of SRE.

---

## 🗃️ Database Schema Overview

The core schema models the essential entities and relationships in a banking ecosystem. Below is an explanation of all key tables and how they connect:

![Schema 1](https://github.com/user-attachments/assets/9fc32c38-d287-471c-935d-54032c100d9b)

### 🧩 Key Tables and Relationships

- **Customer**: Holds all customer details (name, DOB, occupation, income, etc.). Connected to:
  - `address` (One-to-One)
  - `account` (One-to-Many)
  - `login/logout` tracking

- **Account**: Represents customer bank accounts with details like type, branch, account number, balance, and last transaction date.
  - Linked to `accounttype`, `branch`, and `customer`
  - Participates in `transaction`, `withdraw`, `deposit`, and transfer (`transferin`, `transferout`)

- **AccountType**: Defines types of accounts (e.g., savings, current), with associated minimum balance and interest rate. Used by `account` and referenced in `intereststable`.

- **Transaction**: Logs all transactions (deposit, withdraw, transfer), with amount and timestamp.

- **Withdraw / Deposit**: Separate tables capturing withdrawal and deposit metadata, both referencing a `transaction_id`.

- **TransferIn / TransferOut**: Track inter-account money movements with sender/recipient info and timestamps.

- **Balance**: Holds the latest balance for each account, regularly updated post transactions.

- **EditAccount**: Logs changes made to account details for auditability, including who edited and what was changed.

- **DeletedAccount**: Archives deleted accounts with metadata like reason, deleted by, and original balance.

- **Branch**: Stores details of all banking branches.

- **User**: Represents admin/staff users with permissions (RBAC), also links with Django’s auth system.

- **Login / Logout**: Tracks customer login/logout activity for session and security auditing.

- **Ticket**: Support ticket system allowing customers to raise issues; tracks resolution, status, and admin response.

- **InterestTable**: Stores calculated interest per account type, updated periodically.

- **Announcements**: System-wide message board for customers (e.g., policy changes, maintenance notices).

---

## 🧱 System Architecture

The following diagram represents the complete system architecture:

<img width="611" alt="image" src="https://github.com/user-attachments/assets/e3c2321e-6d3f-42a9-adfc-0a8ee3f279b3" />

### 🎯 Core Components

#### 🖥️ Frontend
- **React + Bootstrap UI**: A clean and responsive web interface allowing users to register, login, manage accounts, and perform transactions.

#### 🔧 Backend
- **Django + Django REST Framework**: Serves as the primary backend framework, handling all HTTP requests, APIs, and business logic.
- **SQLite3**: Used in development; can easily be swapped with MySQL/PostgreSQL for production.
- **Celery + Redis**: Used for background tasks such as interest calculation, email alerts, and scheduled reports.

#### 🔄 Banking Services
- **Accounts Service**: Handles creation, modification, and tracking of accounts.
- **Transactions Service**: Manages transfers, deposits, withdrawals, and transaction history.
- **Interest Calculation Service**: Periodically calculates and updates interest rates using Celery.

#### 🔐 User Management
- **Django Authentication + OTP Service**: Secures customer logins, password resets, and sensitive actions.
- **Role-Based Access Control (RBAC)**: Differentiates access between customers, staff, and superusers.

#### 📊 Observability
- **Prometheus + Grafana**: Monitors backend service health, database activity, Celery queues, and system metrics.
- **Loki + Alerting System**: Aggregates logs for debugging and triggers alerts based on anomalies.

#### 🚀 Deployment
- **Dockerized Microservices**: All components run in isolated containers, improving scalability and portability.
- **CI/CD Pipeline**: Automated testing and deployment with shell scripts and Jenkins integration.
- **Kubernetes (optional)**: For cloud deployment, autoscaling, and service orchestration.
