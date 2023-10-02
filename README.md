# Boat/Load REST API
#### A RESTful API for Managing Assets on the Google Cloud Platform with Auth0 Authentication

## Description
This project is a REST API implementation of a web server application using Google Cloud Platform (GCP). The goal of the project was to showcase the implementation of various features and requirements, including resource-based URLs, pagination, status codes, user authentication, and data storage using GCP Datastore. The application utilizes a Flask framework to build the web server that provides endpoints for creating, retrieving, updating, and deleting Boat and Load records, while User records are created upon first login. It incorporates an Auth0 authentication service to handle user authentication and authorization. Users can register, log in, and log out, using a link supplied on the home page. The data is securely stored in Google Cloud Datastore, ensuring efficient data management. Error handling and response formatting functionalities, like pagination, are also included to enhance the user experience. Full specifications are detailed in the [Project Spec Sheet PDF](/assets/documents/lubranoa_project.pdf).

## Program Information
The project requirements stated to provide a simple web page for the user to log in via Auth0, copy their current JWT token, and use it as a Bearer token to access their boats on this API. The project also stated for us to have three entities, Users, one user-dependent, and one user-independent. The two non-user entities must be dependent on each other as well. I chose to have Users, Boats, and Loads as my three. Boats are dependent on Users (Users own them) so a user can only access their Boats and nobody else's. Loads are independent of users (not owned by Users) and can view all Loads but the user must still be authorized. Loads are dependent on Boats (Loads can be put on Boats). The project requirements had us access the API using Postman, so we pasted the JWT token into a Postman environment variable. One other note is that no input-validation was required. The graders followed the written specification's guidelines on any values sent to the API.

The following are some highlights of the program. Full specifications can be found in [this PDF](/assets/documents/lubranoa_project.pdf). 
1. Login
   - The first step of this program is for the user to login or create an account. This was implemented through Auth0.

   ![Screenshot of the web page of the user's information on Auth0 in JSON format after successful login](/assets/images/493-01a-welcome_page.png)

   ![Screenshot of the web page of the user's information on Auth0 in JSON format after successful login](/assets/images/493-01b-auth0_login.png)

2. Get Token
   - After successful login, the user's information on Auth0 is displayed. If this is the first time the user has logged in, a User entity is created for them on the Datastore database. Then the user must copy the value of the "id_token" for use as a bearer token.

   ![Screenshot of the web page of the user's information on Auth0 in JSON format after successful login](/assets/images/493-02-jwt_info.png)

3. Create a Boat (Create User-Boat dependency)
   - A create Boat request must have the copied JWT as a bearer token and must have a body with the three required attributes. If successfully created, a Boat is created with a Datastore generated ID, the three attributes, no loads, and an owner ID which is the 'sub' value from the JWT. The self attribute and value are not stored on Datastore but are created by the application.

   ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-03-create-boat.png)

4. Create a Load (No User-dependency)
   - A create Load request.

   ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-04-create-load.png)

5. Add/Remove a Load to/from a Boat (Add/remove Boat-Load dependency)
   - Empty Boat

    ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-05a-boat-no-load.png)
    
   - A put request for putting load on a boat

    ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-05b-add-load-to-boat.png)

   - Non-empty boat

    ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-05c-load-added.png)

   - Load has a carrier

    ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-05d-load-with-carrier.png)

    - Remove load from boat

    ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-05e-del-load-off-boat.png)

    ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-05f-load-removed.png)

    ![Screenshot of a Postman request tab displaying a POST request to create a boat with a name, type, and length as well as a response from the sent request containing a new boat with an ID, name, type, length, no loads, an owner ID, and a self attribute that contains a URL to the boat.](/assets/images/493-05g-load-carrier-removed.png)

6. Delete a Boat containing a Load (Removes User-Boat and Boat-Load dependencies)
7. Delete a Load loaded on a Boat (Removes Boat-Load dependency)


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