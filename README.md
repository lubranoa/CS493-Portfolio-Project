<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- Title Section -->
<div align="center">
  <!-- Badges -->
  <p>
    <a href="www.linkedin.com/in/lubrano-alexander">
      <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin" alt="linkedin link" />
    </a>
    <a href="https://lubranoa.github.io">
      <img src="https://img.shields.io/badge/Personal_Site-47b51b?style=for-the-badge" alt="personal website link" />
    </a>
    <a href="https://github.com/lubranoa">
      <img src="https://img.shields.io/badge/GitHub_Profile-8A2BE2?style=for-the-badge&logo=github" alt="github profile link" />
    </a>
  </p>
  <!-- Titles and Subtitles -->
  <h1 align="center">Boat-Load REST API</h1>
  <p align="center">
    <b>A RESTful API for Managing Assets on the Google Cloud Platform with Auth0 Authentication</b>
  </p>
  <p align="center">
    Spring 2023 · <a href="https://ecampus.oregonstate.edu/soc/ecatalog/ecoursedetail.htm?subject=CS&coursenumber=493&termcode=ALL">CS 493 Cloud Application Development</a> · Oregon State University
  </p>
  <br />
</div>

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
    
  - [Description](#description)
  - [Project Tech Stack](#project-tech-stack)
  - [Project Information](#project-information)
    - [Assignment Requirements](#assignment-requirements)
    - [My Project's Entities](#my-projects-entities)
    - [Notes](#notes)
  - [API Highlights](#api-highlights)
    - [Simple Login Website](#simple-login-website-using-auth0)
    - [Logged In](#logged-in)
    - [Create a Boat](#create-a-boat-create-user-boat-dependency)
    - [Create a Load](#create-a-load-no-user-dependency)
    - [Add Load to Boat](#add-a-load-to-a-boat-add-boat-load-dependency)
    - [Remove Load from Boat](#remove-a-load-from-a-boat-remove-boat-load-dependency)
    - [Update Operations](#update-operations)
    - [Delete Operations](#delete-operations)
  - [Skills Used](#skills-used)
    - [REST API Development](#rest-api-development)
    - [Google Cloud Platform](#google-cloud-platform)
    - [User Authentication](#user-authentication)
    - [Data Modeling](#data-modeling)
    - [Pagination](#pagination)
    - [Error Handling and Status Codes](#error-handling-and-status-codes)
    - [Postman Testing](#postman-testing)
    - [Documentation](#documentation)
  - [Resources](#references)

</details>

## Description
This project from Cloud Application Development is a REST API implementation of a web server application using Google Cloud Platform (GCP). The goal of the project was to showcase the implementation of various features and requirements, including resource-based URLs, pagination, status codes, user authentication, and data storage using GCP Datastore. The application utilizes a Flask framework to build the web server that provides endpoints for creating, retrieving, updating, and deleting Boat and Load records, while User records are created upon first login. It incorporates an Auth0 authentication service via a simple website deployed on GCP App Engine that provides a link where users can register, log in, and log out of the Auth0 service. Once logged in, users can copy a time-sensitive JWT token to send with API requests as a bearer token. Any data is securely stored in Google Cloud Datastore, ensuring efficient data management. Error handling and response formatting functionalities, like pagination, are also included to enhance the user experience. Full specifications are detailed in this project's [API Spec Document](/assets/documents/lubranoa_project.pdf).

## Project Tech Stack
   - [![Python][Python]][Python-url]
   - [![Flask][Flask]][Flask-url]
   - [![Auth0][Auth0]][Auth0-url]
   - [![Google Cloud][Google-cloud]][Google-cloud-url]
   - [![Postman][Postman]][Postman-url]
   - [![Dotenv][Dotenv]][Dotenv-url]

## Project Information
### Assignment Requirements
Some of the major project requirements from the assignment's guidelines:
   - Deploy a simple web page using GCP's App Engine for users to create an account and log in via Auth0, copy their current JWT token, and use it as a Bearer token to access the API using Postman. 
   - Must have three entities, Users, one User-dependent, and one User-independent. The two non-User entities must be dependent on each other in some way.
   - Have CRUD operations for each of the non-User entities. Each operation for the User-dependent entity must be protected and require a valid JWT token corresponding to the relevant User.
   - Deletions of any non-User entities that have dependencies with another non-User entity must be handled properly.
   - All endpoints must adhere to RESTful standards.
   - Must use GCP's Datastore NoSQL database to store User, Boat, and Load records.
   - No input-validation is required. Graders followed the guidelines written in the specifications document for any values sent to the API.

### My Project's Entities
My choice was for my API to have Users, Boats, and Loads as my three entities. 
  - Boats are dependent on Users (Users own them) so a user can only access their Boats and nobody else's. 
  - Loads are independent of users (not owned by Users), so Users can view all Loads
  - Loads and Boats can have a codependent relationship (if a Load is "loaded" on a Boat). 

### Notes
   - All of the responses this API sends back to the user will have an appropriate 20* and 4** status code depending on the type of request and whether the operation was successful or not. A full list of supported status codes per type of request is available in the project PDF. 
   - For all responses with body content, all of the `self` attributes and values are not stored on Datastore but are added to the response by the API.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## API Highlights
The following are some highlights of my API, which include the login website, what the user sees upon login, creating Boats and Loads, creating Boat-Load dependencies, fully or partially updating a Boat or Load, and deleting a Boat or Load, including how any Boat-Load dependencies are resolved. Full specifications can be found in this project's [API Spec Document](/assets/documents/lubranoa_project.pdf).

### Simple Login Website using Auth0
   
   This website provides a link for a user to begin a login process using Auth0. This redirects to an Auth0 page that allows a user to log in with their account or Google account or to sign up to use the website.

   ![Screenshot of the simple login website with a login link.](/assets/images/493-01a-welcome_page.png)

   ![Screenshot of the Auth0 login page with email and password fields, continue button, sign up link, and login with Google button.](/assets/images/493-01b-auth0_login.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Logged In
   
   After successful login, the user's information on Auth0 is displayed. If this is the first time the user has logged in, a User entity is created for them on the Google Datastore database. For API access, the user must copy the value of the `id_token` for use as a bearer token when making API calls.

   ![Screenshot of the web page of the user's information on Auth0 in JSON format after successful login](/assets/images/493-02-jwt_info.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Create a Boat (Create User-Boat dependency)
   
   A create Boat POST request must have the copied JWT as a bearer token and must have a body with the three required attributes. If successful, a new Boat is created on Google Datastore with a Datastore generated ID, the three attributes, an empty loads array, an owner ID which is the 'sub' value from the Auth0 JWT, and a self attribute that contains a URL that points to the Boat.

   ![Screenshot of a Postman tab displaying a POST request using the user's JWT token to create a Boat object with a name, type, and length. The screenshot also displays a successful "201 Created" response from the API containing the new Boat object with an ID, name, type, length, an empty loads array, an owner ID, and a self attribute that contains a URL to the Boat.](/assets/images/493-03-create-boat.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Create a Load (No User-dependency)
   
   A create Load POST request needs no authorization but must have a body with the three required attributes. If successful, a new Load is created on Datastore with a Datastore generated ID, the three attributes, a carrier attribute set to NULL, and a self attribute that contains a URL to the Load.

   ![Screenshot of a Postman tab displaying a POST request to create a Load with an item name, volume, and creation date. The screenshot also displays a successful "201 Created" response from the API containing the new Load object with an ID, item, volume, creation date, carrier set to NULL, and a self attribute that contains a URL to the Load.](/assets/images/493-04-create-load.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Add a Load to a Boat (Add Boat-Load dependency)
   
   GET an empty Boat using a Boat's ID value and user's JWT token. User must be the owner of the boat to view it. Note the empty loads array.
     
   ![Screenshot of a Postman tab displaying a GET request to view a Boat object using its ID value in the URL and the user's JWT token. The screenshot also displays a successful "200 OK" response that contains the requested Boat object with no loads in the load array.](/assets/images/493-05a-boat-no-load.png)
    
   PUT a Load on that Boat. This puts the Load's ID value into the loads array of the Boat and changes the Load's carrier attribute from NULL to the Boat's ID value. Then it updates both the Boat's and Load's objects on Datastore. User must be the owner of the Boat to put a Load on it.
    
   ![Screenshot of a Postman tab displaying a PUT request to put a Load on the previous Boat using their respective ID values in the URL and the user's JWT token. The screenshot also displays a "204 No Content" response from the API showing a successful PUT request was carried out.](/assets/images/493-05b-add-load-to-boat.png)

   Boat contains a Load. The Boat now contains the Load's ID value in its loads array. The Load now contains the Boat's ID value in its carrier attribute.
     
   ![Screenshot of a Postman tab displaying a GET request to view the same Boat object using it's ID value in the URL and the user's JWT token. The screenshot also displays a successful "200 OK" response that contains the requested Boat object with a single Load ID in the load array.](/assets/images/493-05c-load-added.png)

   Load has a carrier Boat. The Load's carrier attribute is now set to the Boat's ID value.
    
   ![Screenshot of a Postman tab displaying a GET request to view the same Load object using it's ID value in the URL. The screenshot also displays a successful "200 OK" response that contains the requested Load object with the carrier attribute set to the Boat's ID that holds the Load.](/assets/images/493-05d-load-with-carrier.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Remove a Load from a Boat (Remove Boat-Load Dependency)

   DELETE a Load from a Boat. This removes the Load from the Boat's loads and sets the Load's carrier attribute to NULL, then updates both entities on Datastore. Succeeds only if the Boat exists, the Load exists, this Load is on that Boat, and the User owns the Boat. The following three images show the DELETE request and the resulting Load and Boat GETs to verify deletion.
    
   ![Screenshot of a Postman tab displaying a DELETE request to remove the Load from the same Boat using their respective ID values in the URL and the user's JWT token. The screenshot also displays a "204 No Content" response from the API showing a successful DELETE request was carried out.](/assets/images/493-05e-del-load-off-boat.png)
   ![Screenshot of a Postman tab displaying a GET request to view the same Boat object using it's ID value in the URL and the user's JWT token. The screenshot also displays a successful "200 OK" response that contains the requested Boat object with an empty loads array after removing the Load from the Boat.](/assets/images/493-05f-load-removed.png)
   ![Screenshot of a Postman tab displaying a GET request to view the same Load object using it's ID value in the URL. The screenshot also displays a successful "200 OK" response that contains the requested Load object with the carrier attribute set to NULL after removing the Load from the Boat.](/assets/images/493-05g-load-carrier-removed.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Update Operations
   - Use PATCH request to partially update a Boat or Load 
   - Use PUT request to fully update a Boat or Load

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Delete Operations
   - DELETE a Boat or Load
   - Special Case: Delete a Boat containing a Load (Removes User-Boat and Boat-Load dependencies)
   - Special Case: Delete a Load loaded on a Boat (Removes Boat-Load dependency)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Skills Used
#### REST API Development:
  - The project involved designing and implementing a RESTful API using Python 3 and Flask. This included defining resource-based URLs, implementing CRUD (Create, Read, Update, Delete) operations for entities, and handling requests and responses.
#### Google Cloud Platform:
  - The project required deploying the application on Google App Engine and using Datastore as the database for storing the application data. Knowledge of GCP services and deployment process was necessary.
#### User Authentication:
  - The project required implementing user authentication and authorization. This included providing endpoints for user account creation and login, generating and validating JWT (JSON Web Tokens), and protecting access to certain resources based on user authentication.
#### Data Modeling:
  - The project involved designing and modeling entities for the application. This included defining properties for each entity, establishing relationships between entities, and ensuring that entities meet the requirements specified in the project description.
#### Pagination:
  - The project required implementing pagination for entity collections, displaying a limited number of entities per page, and providing a "next" link for navigating to the next page of results.
#### Error Handling and Status Codes:
  - The project involved handling errors and returning appropriate status codes in the API responses. Knowledge of HTTP status codes (e.g., 200, 201, 204, 401, 403, 405, 406) and how to handle them was essential.
#### Postman Testing:
  - The project required creating a Postman collection to test the API endpoints and verify their functionality. This included setting up test cases for CRUD operations, relationship creation and deletion, user account-related operations, and validating the response status codes.
#### Documentation:
  - The project required creating an API specification document that details all the endpoints, their protected/unprotected status, valid status codes, sample requests, and responses. Clear and concise documentation was essential to provide a comprehensive understanding of the API's functionality.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Resources

<!-- Markdown links and images -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=ffd343
[Python-url]: https://www.python.org/

[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/

[Auth0]: https://img.shields.io/badge/Auth0-16214d?style=for-the-badge&logo=auth0
[Auth0-url]: https://auth0.com/

[Google-cloud]: https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white
[Google-cloud-url]: https://cloud.google.com/

[Postman]: https://img.shields.io/badge/Postman-ef5b25?style=for-the-badge&logo=postman&logoColor=white
[Postman-url]: https://www.postman.com/

[Dotenv]: https://img.shields.io/badge/Dotenv-000000?style=for-the-badge&logo=dotenv&logoColor=ecd53f
[Dotenv-url]: https://pypi.org/project/python-dotenv/