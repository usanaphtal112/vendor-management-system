# Vendor Management System with Performance Metrics

This Vendor Management System (VMS) is built using Django and Django REST Framework. It allows users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Table of Contents

1. [Introduction](#introduction)
2. [Core Features](#core-features)
3. [Technical Requirements](#technical-requirements)
4. [Installation and Setup](#installation-and-setup)
5. [Usage](#usage)
6. [API Documentation](#api-documentation)
7. [Testing](#testing)
8. [Contributing](#contributing)

## Introduction

The Vendor Management System is designed to streamline vendor-related processes for organizations. It provides a centralized platform to manage vendor information, track purchase orders, and evaluate vendor performance based on predefined metrics.

## Core Features

- **Vendor Profile Management**: Create, update, delete, and retrieve vendor profiles.
- **Purchase Order Tracking**: Manage purchase orders, including creation, updating, deletion, and retrieval.
- **Vendor Performance Evaluation**: Calculate vendor performance metrics such as on-time delivery rate, quality rating average, response time, and fulfillment rate.

## Technical Requirements

- Python 3.9 or above
- Django
- Django REST Framework
- Other dependencies (specified in requirements.txt)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/usanaphtal112/vendor-management-system.git
   ```

2. Navigate to the project directory:

   ```bash
   cd vendor_management_system
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

## Usage

1. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

2. Access the API endpoints using a tool like Postman or curl.

## API Documentation

- **Vendor Endpoints**:

  - POST /api/vendors/: Create a new vendor.
  - GET /api/vendors/: List all vendors.
  - GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
  - PUT /api/vendors/{vendor_id}/: Update a vendor's details.
  - DELETE /api/vendors/{vendor_id}/: Delete a vendor.

- **Purchase Order Endpoints**:

  - POST /api/purchase_orders/: Create a purchase order.
  - GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
  - GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
  - PUT /api/purchase_orders/{po_id}/: Update a purchase order.
  - DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

- **Performance Metrics Endpoints**:

  - GET /api/vendors/{vendor_id}/performance/: Retrieve a vendor's performance metrics.

## Testing

To run tests, execute the following command:

```bash
python manage.py test
```

## Testing Details

- Tested all models for CRUD operations.
- Tested utils helper functions for Historical performance calculations.
- Tested JWT Authentications.
- Tested Signals.

## Pre-commit Hook

A pre-commit hook is configured to ensure PEP8 compliance and run tests before each commit. This helps maintain code quality and ensures that only passing code is committed to the repository.

## Contributing
