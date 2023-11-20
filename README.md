<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- Title Section -->
<div align="center">
  <!-- Badges -->
  <p>
    <a href="https://linkedin.com/in/lubrano-alexander">
      <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin" alt="linkedin link" />
    </a>
    <a href="https://lubranoa.github.io">
      <img src="https://img.shields.io/badge/Personal_Site-47b51b?style=for-the-badge" alt="personal website link" />
    </a>
    <a href="https://github.com/lubranoa">
      <img src="https://img.shields.io/badge/GitHub-8A2BE2?style=for-the-badge&logo=github" alt="github profile link" />
    </a>
  </p>
  <br />
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

  - [Project Description](#project-description)
  - [Technologies Used](#technologies-used)
  - [Features](#features)
  - [Usage](#usage)
  - [Skills Applied](#skills-applied)
  - [Contact](#contact)
  - [Acknowledgments](#acknowledgements)

</details>

<!-- Project Description -->
## Project Description

This project is a Flask REST API that allows users to interact with entities stored in a Google Cloud Datastore database via resource-based Flask endpoints, JSON Web Tokens (JWT), and Postman. The user can get a time-sensitive JWT by logging in to the project's simple website deployed on Google Cloud App Engine. This was the final project for Cloud Application Development and had the goals of implementing a REST API that incorporated proper resource-based URLs, pagination, and appropriate HTTP status codes as well as implementing some sort of system for creating users and authorization.

<!-- Technologies Used -->
## Technologies Used

   - [![Python][Python]][Python-url]
   - [![Flask][Flask]][Flask-url]
   - [![Auth0][Auth0]][Auth0-url]
   - [![Google Cloud][Google-cloud]][Google-cloud-url]
   - [![Postman][Postman]][Postman-url]
   - [![Dotenv][Dotenv]][Dotenv-url]

<!-- Features -->
## Features
  
  - **API Access via Auth0**: 
    - The project provides a simple website for users to create accounts and login to Auth0 to get an authorization token for API interactions.
  - **Token-based Authorization**: 
    - Once logged in, the Auth0 service generates a time-sensitive JSON Web Token to authorize API interactions.
  - **Boat, Load, and User Entities**: 
    - The API provides the entities, Boats, Loads, and Users, for a user to interact with. They each have different dependencies on each other in certain ways laid out in the [Usage section](#usage).
  - **Boat Entity Authorization**:
    - Due to assignment requirements, Boat entities are protected from alterations unless the Boat is owned by the User who is interacting with it.
  - **RESTful CRUD Endpoints**: 
    - Provides create, read, update, and delete endpoints that adhere to REST standards for Boat and Load entities, but only create and read for User entities.
  - **Integration with GCP Datastore**:
    - Persists Boat, Load, and User records on Google Cloud's Datastore NoSQL database when the user interacts with the API.
  - **HTTP Status Code and Errors**:
    - Provides appropriate HTTP 200 and 400 status codes and error messages to send back in API responses to the user.
  - **Data Representation**:
    - All entities are represented as JSON. Any responses with entities will have an API-generated `self` link pointing to its own record on Datastore. These `self` attributes are not stored persistently.
  - **Result Pagination**:
    - Paginates any responses to requests for reading all boats or all loads via a `next` link on every page of results except the last.
  - *No Input Validation*:
    - The assignment specifications stated there was no need for input validation as the graders would adhere to the guidelines outlined in our [personal documentation](/assets/documents/lubranoa_project.pdf).
  

### Assignment Requirements

Some of the major requirements from the assignment's guidelines:
   - Deploy a simple web page using GCP's App Engine for users to create an account and log in via Auth0, copy their current JWT token, and use it as a Bearer token to access the API using Postman. 
   - Must have three entities, Users, one User-dependent, and one User-independent. The two non-User entities must be dependent on each other in some way.
   - Have CRUD operations for each of the non-User entities. Each operation for the User-dependent entity must be protected and require a valid JWT token corresponding to the relevant User.
   - Deletions of any non-User entities that have dependencies with another non-User entity must be handled properly.
   - All endpoints must adhere to RESTful standards.
   - Must use GCP's Datastore NoSQL database to store User, Boat, and Load records.
   - No input-validation is required. Graders followed the guidelines written in the specifications document for any values sent to the API.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Usage -->
## Usage

To use this API, the user must do three things, log in to the API's website, copy their generated token, and send it as a bearer token along with API requests. Before getting to that, an explanation of the Boat, Load, and User entities of the API is in order. For a full description of the entities, their relationships, and their endpoints, see the [project documentation](/assets/documents/lubranoa_project.pdf).

#### Entity Data Models and Relationships

The following is a quick outline of the API's entities' data models and relationships with the others. The assignment specifications called for three entities, a User entity and two non-User entities, one User-dependent and one User-independent, which had to be dependent on each other in some way. 

  - **User Entities**
    - Have two stored attributes, a unique ID and a name pulled from their Auth0 account.
    - Created when a user creates an account with the Auth0 service.
    - Cannot be edited.
  - **Boat Entities** (User-dependent)
    - Have six stored attributes, a unique ID number, name, Boat type, length, owner, and loads. Only name, type, length, and loads can be altered.
    - Never allowed to have no owner, creating User-dependency.
    - The `loads` attribute contains any Loads that are loaded onto a Boat.
    - A User must be authorized to alter a Boat in any way.
    - A User can only alter their own Boats and never anyone else's.
  - **Load Entities** (User-independent)
    - Have five stored attributes, a unique ID number, the item name it contains, its volume, creation date, and a carrier. Only the item name, volume, creation date, and carrier can be altered.
    - The `carrier` attribute holds the ID number of the Boat that holds the Load or `NULL` if it hasn't been loaded onto a Boat, which creates the non-User entities' dependencies on each other.
    - No User-dependency means any loads can be altered by anyone, except the special case where `carrier` is edited.
    - Altering the `carrier` attribute requires User authorization because this operation also alters a Boat's `loads` attribute.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Gaining Access to the API

  1) To access the API, a user must first create an account or log in to the API's simple website. This web page provides a link to the `\login` endpoint of the API, which begins a login process through Auth0. Click on the pictures to make them larger.

  Home Page                  | Auth0 Login               | User Info Page with JWT
  :-------------------------:|:-------------------------:|:-------------------------:
  ![Screenshot of the simple login website with a login link.](/assets/images/493-01a-welcome_page.png)  |  ![Screenshot of the Auth0 login page with email and password fields, continue button, sign up link, and login with Google button.](/assets/images/493-01b-auth0_login.png)  |  ![Screenshot of the web page of the user's information on Auth0 in JSON format after successful login](/assets/images/493-02-jwt_info.png)

  2) After successful login, see above that the user's information on Auth0 is displayed to them along with a time-sensitive JWT token. If this is the first time the user has logged in, a User entity is created on the Google Datastore database. 
  
  3) For API interactions, the user must copy the value of the `id_token` for use as a bearer token when making API requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Interacting with the API

The API has multiple endpoints that users can utilize to interact with the API. The API will send back all responses with an appropriate HTTP status code depending on the operation and/or any errors that occur in processing the request. All of the endpoints require any request bodies to be sent in JSON format. For full specifications, status codes, and example responses, check the [project documentation](/assets/documents/lubranoa_project.pdf).

  - **READ** a Collection of All Users (No pagination)
    - Method and Endpoint: GET `/users`
    - Authorization: *None*
    - The only endpoint for the Users entity.
    - Allows a user to get a list of all users on the platform.
  - **READ** Collections of Boats and Loads (Both support pagination)
    - *Read* all Boats of a User (Read)
      - Method and Endpoint: GET `/boats`
      - Authorization: user JWT from Auth0
      - Returns all boats owned by the user, 5 per page maximum.
    - *Read* all Loads
      - Method and Endpoint: GET `/loads`
      - Authorization: *None*
      - Returns all loads in the database
    - Responses from both of these will contain a `next` attribute with a link to the next page of results. If not present in a response, then there are no more results.
   - 
      - Method and Endpoint: POST `/boats`
      - Request body must contain a name, boat type, and length. Creation fails otherwise.
      - During creation, the API uses Datastore to set up a unique ID, the owner of the boat, and an empty loads array.
        
        <details>
          <summary>Screenshot of Boat Creation on Postman</summary>

          ![Screenshot of a Postman tab displaying a POST request to create a Boat object with a name, type, and length. The screenshot also displays a successful "201 Created" response from the API containing the new Boat object with an ID, name, type, length, an empty loads array, an owner ID, and a self attribute that contains a URL to the Boat.](/assets/images/493-03-create-boat.png)

        </details>


  - Load Endpoints

  - Non-user Relationship
   
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

<!-- Skills Applied -->
## Skills Applied

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

<!-- Contact -->
## Contact

Alexander Lubrano - [lubrano.alexander@gmail.com][email] - [LinkedIn][linkedin-url]

Project Link: [https://github.com/lubranoa/<repo-name>][repo-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Acknowledgements -->
## Acknowledgments

  - [Shields.io][shields-url]
  - [Simple Icons][icons-url]

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

[email]: mailto:lubrano.alexander@gmail.com
[linkedin-url]: www.linkedin.com/in/lubrano-alexander
[repo-url]: https://github.com/lubranoa/CS493-Portfolio-Project