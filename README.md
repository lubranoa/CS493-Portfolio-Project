# CS 493 - Cloud Application Development Portfolio Project

## Description
This project is a REST API implementation of a web server application using Google Cloud Platform (GCP). The goal of the project was to showcase the implementation of various features and requirements, including resource-based URLs, pagination, status codes, user authentication, and data storage using GCP Datastore. The application utilizes a Flask framework to build the web server that provides endpoints for creating, retrieving, updating, and deleting boat and load records. User records are created upon first login. It incorporates Auth0 authentication service to handle user authentication and authorization. Users can register, log in, and log out, while authenticated users have access to perform operations on boats and users. The data is securely stored in Google Cloud Datastore, ensuring efficient data management. Error handling and response formatting functionalities, like pagination, are also included to enhance the user experience. Full specifications are detailed in the Project Spec Sheet PDF.

## Program Information
Put some details about the data model, how to it should work/run, etc.

## Skills Used
- REST API development:
  - The project involved designing and implementing a RESTful API using Python 3 and Flask. This included defining resource-based URLs, implementing CRUD (Create, Read, Update, Delete) operations for entities, and handling requests and responses.
- Google Cloud Platform:
  - The project required deploying the application on Google App Engine and using Datastore as the database for storing the application data. Knowledge of GCP services and deployment process was necessary.
- User Authentication:
  - The project required implementing user authentication and authorization. This included providing endpoints for user account creation and login, generating and validating JWT (JSON Web Tokens), and protecting access to certain resources based on user authentication.
- Data Modeling:
  - The project involved designing and modeling entities for the application. This included defining properties for each entity, establishing relationships between entities, and ensuring that entities meet the requirements specified in the project description.
- Pagination:
  - The project required implementing pagination for entity collections, displaying a limited number of entities per page, and providing a "next" link for navigating to the next page of results.
- Error Handling and Status Codes:
  - The project involved handling errors and returning appropriate status codes in the API responses. Knowledge of HTTP status codes (e.g., 200, 201, 204, 401, 403, 405, 406) and how to handle them was essential.
- Postman Testing:
  - The project required creating a Postman collection to test the API endpoints and verify their functionality. This included setting up test cases for CRUD operations, relationship creation and deletion, user account-related operations, and validating the response status codes.
- Documentation:
  - The project required creating an API specification document that details all the endpoints, their protected/unprotected status, valid status codes, sample requests, and responses. Clear and concise documentation was essential to provide a comprehensive understanding of the API's functionality.

## Resources