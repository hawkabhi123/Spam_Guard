# SpamGuard API

SpamGuard API is a RESTful service built with Django that allows users to register, manage contacts, identify potential spam numbers, and search for individuals by name or phone number. This API is designed to be consumed by a mobile application.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Structure](#database-structure)
- [Testing](#testing)
- [Contributing](#contributing)


## Features

- User Registration and Authentication
- Contact Management
- Spam Number Identification
- Search Functionality by Name or Phone Number
- Secure and Scalable API Design

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

- Python 
- Django 


### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ZERI-SPARK/SpamGuard_API.git
   cd SpamGuard_API

**2. Steps/Install dependencies::**
      
    python -m venv myenv
    source myenv/Scripts/activate  # On Windows
    # or
    source myenv/bin/activate  # On MacOS/Linux

    pip install -r requirements.txt
    
      
**3.Run the development server:**
      
      python manage.py runserver

      
**4. Testing (To run tests, use the following command):**
   
       python manage.py test


       

# API Token Authorization using Postman
**- **Token Request****

![Screenshot 2024-08-25 123635](https://github.com/user-attachments/assets/2930111b-18de-412d-a39d-28ee57ecdaf9)

**- API Response**

![Screenshot 2024-08-25 123655](https://github.com/user-attachments/assets/f1251c9b-b891-41ad-a8ae-819864925fe8)
**- Contact Management**
![Screenshot 2024-08-25 123801](https://github.com/user-attachments/assets/e8dd5d0e-d8d1-4300-9b51-5add5dccdd5c)

**- Endpoints**

![Screenshot_25-8-2024_123316_127 0 0 1](https://github.com/user-attachments/assets/21cffec5-d477-40cc-9b56-dec7cc50783d)

**- Manual Testing / Resgistarion /**
![Screenshot_25-8-2024_123338_127 0 0 1](https://github.com/user-attachments/assets/68a8a962-63f6-44b7-8d88-ee865256bd57)
![Screenshot_25-8-2024_123551_127 0 0 1](https://github.com/user-attachments/assets/4c1fc33c-0b64-4972-ae1a-6a660a45da49)

![Screenshot_25-8-2024_12350_127 0 0 1](https://github.com/user-attachments/assets/5e5b88ec-ff00-4243-a237-09d1cebe905d)

Usage
The API is designed to be integrated with a mobile application. Use Postman or any other API testing tool to interact with the API endpoints. Refer to the API Endpoints section for more details.



