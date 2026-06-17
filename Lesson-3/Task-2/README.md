# Smart Gmail Agent with n8n and Groq AI

## Overview

This project implements an AI-powered Gmail Agent using n8n, Groq LLM, and HTTP Request APIs. The workflow automatically monitors incoming emails, classifies them into predefined categories using an AI Agent, retrieves users from an external API, and routes emails to the appropriate recipients based on their roles.

---

## Objective

Build an intelligent email routing system that:

* Monitors incoming Gmail messages
* Uses an AI Agent powered by Groq LLM to classify queries
* Retrieves user information from an external API
* Filters users based on their roles
* Sends emails only to the relevant users

---

## Tech Stack

| Technology        | Purpose                |
| ----------------- | ---------------------- |
| n8n               | Workflow Automation    |
| Groq LLM          | Email Classification   |
| Gmail Trigger     | Detect Incoming Emails |
| HTTP Request Node | Fetch User Data        |
| Gmail Node        | Send Routed Emails     |
| REST API          | User Management        |

---

## Workflow Architecture

```text
Gmail Trigger
      ↓
Edit Fields
      ↓
AI Agent (Groq)
      ↓
HTTP Request (Users API)
      ↓
IF Node
      ↓
Gmail Send
```

---

## Workflow Description

### Step 1: Gmail Trigger

The workflow starts whenever a new email arrives in the Gmail inbox.

### Step 2: Extract Email Content

The email body and subject are extracted using the Edit Fields node.

Example:

```json
{
  "query": "I was charged twice this month.",
  "subject": "Billing Issue"
}
```

### Step 3: AI Classification

The extracted email content is sent to a Groq-powered AI Agent.

The agent classifies emails into one of the following categories:

#### Customer

* Product Inquiry
* General Support
* Sales Question
* Billing Inquiry
* Feature Request

#### Admin

* Technical Escalation
* System Issue
* Security Concern
* Data Issue
* Integration Problem

Example Output:

```json
{
  "output": "Customer"
}
```

---

### Step 4: Fetch Users

The workflow makes an HTTP GET request to:

```http
https://api.escuelajs.co/api/v1/users
```

Sample Response:

```json
{
  "id": 3,
  "email": "admin@mail.com",
  "role": "admin"
}
```

---

### Step 5: Role-Based Filtering

The workflow compares the AI classification result with the user role retrieved from the API.

Examples:

```text
Admin = admin → TRUE
Customer = customer → TRUE
```

Only matching users continue to the next step.

---

### Step 6: Email Routing

The Gmail node sends the classified email to the matching users.

Example Customer Query:

```text
I was charged twice this month.
```

Route:

```text
Customer Users
```

Example Admin Query:

```text
URGENT: API integration is down in production.
```

Route:

```text
Admin Users
```

---

## AI Agent Prompt

```text
You are an email classification agent.

Classify the email into exactly one category.

Customer:
- Product Inquiry
- General Support
- Sales Question
- Billing Inquiry
- Feature Request

Admin:
- Technical Escalation
- System Issue
- Security Concern
- Data Issue
- Integration Problem

Return ONLY one word:

Customer

or

Admin
```

---

## Sample Test Cases

| Email Query                                        | Expected Classification |
| -------------------------------------------------- | ----------------------- |
| I was charged twice this month.                    | Customer                |
| Can you add dark mode support?                     | Customer                |
| I need help with my subscription plan.             | Customer                |
| API integration is failing in production.          | Admin                   |
| Recent suspicious login detected.                  | Admin                   |
| Database connection errors are impacting services. | Admin                   |

---

## API Used

### Users API

```http
GET https://api.escuelajs.co/api/v1/users
```

Purpose:

* Retrieve user information
* Identify user roles
* Route emails based on classification

---

## Assignment Requirements Covered

* Gmail Integration
* AI Agent using Groq
* HTTP Request Tool
* Query Classification
* Role-Based Routing
* Email Automation
* End-to-End Workflow in n8n

