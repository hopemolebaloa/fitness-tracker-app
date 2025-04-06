# Fitness Tracker API

A Django-based REST API for tracking fitness activities, allowing users to log, update, delete, and view their fitness activity history. Built with Django REST Framework and deployed on Heroku.

## Live Web App
The API is deployed on Heroku and can be accessed at:  
[https://fitness-tracker-api-hope.herokuapp.com/](https://fitness-tracker-api-hope.herokuapp.com/)

> **Note:** The app may take a few seconds to start up if it has been idle.

## Project Overview
This project is a backend API for a Fitness Tracker application. It allows users to:
- Perform CRUD operations on fitness activities (e.g., running, cycling, weightlifting).
- Manage user accounts with authentication.
- View activity history with filtering options.

The API is built using Django and Django REST Framework, with PostgreSQL as the database in production (via Heroku Postgres).

## Features
- **Activity Management (CRUD)**:
  - Create, read, update, and delete fitness activities.
  - Each activity includes: Activity Type, Duration, Distance, Calories Burned, Date, and User ID.
- **User Management**:
  - Users can register, log in, and manage their own activities.
  - Authentication ensures users can only access their own data.
- **Activity History**:
  - View a list of all activities logged by the user.
- **Deployment**:
  - Deployed on Heroku with a PostgreSQL database.

## Local Setup
To run the project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd fitness-tracker
