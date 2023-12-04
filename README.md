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
    - [Entity Data Models and Relationships](#entity-data-models-and-relationships)
    - [Gaining Access to the API](#gaining-access-to-the-api)
    - [Interacting with the API](#interacting-with-the-api)
      - [Interactions with Users](#interactions-with-users)
      - [Interactions with Boats](#interactions-with-boats-user-dependent)
      - [Interactions with Loads](#interactions-with-loads-user-independent)
      - [Interactions between Boats and Loads](#interactions-between-boats-and-loads)
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
    - The project provides a simple website for users to create accounts and secure OAuth 2.0 login via Auth0 to get an authorization token for some API interactions.
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
  - **HTTP Status Codes and Errors**:
    - Provides appropriate HTTP 200 and 400 status codes and error messages to send back in API responses to the user.
  - **Data Representation**:
    - All entities are represented as JSON. Any responses with entities will have an API-generated `self` link pointing to its own record on Datastore. These `self` attributes are not stored persistently.
  - **Result Pagination**:
    - Paginates any responses to requests for reading all boats or all loads via a `next` link on every page of results except the last.
  - *No Input Validation*:
    - The assignment specifications stated there was no need for input validation as the graders would adhere to the guidelines outlined in our [personal documentation](/assets/documents/lubranoa_project.pdf).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Usage -->
## Usage

To use this API fully, the user must do three things, log in to the API's website, copy their generated token, and send it as a bearer token along with API requests. Before getting to that, an explanation of the Boat, Load, and User entities of the API is in order. For a full description of the entities, their relationships, and their endpoints, see the [project documentation](/assets/documents/lubranoa_project.pdf).

### Entity Data Models and Relationships

The following is a quick outline of the API's entities' data models and relationships with the others. The assignment specifications called for three entities, a User entity and two non-User entities, one User-dependent and one User-independent, which had to be dependent on each other in some way. 

  - **User Entities**

    - Have two stored attributes:
      - unique ID value
      - name (pulled from their Auth0 account)
    - Created when a user creates an account with the Auth0 service.
    - Cannot be edited.

  - **Boat Entities** (User-dependent)

    - Have six stored attributes:
      - unique ID value
      - name
      - boat type
      - length
      - owner
      - loads (array that holds any Loads "loaded" on the Boat)
    - Only name, type, length, and loads can be altered by a user.
    - Never allowed to have no owner, creating User-dependency.
    - A User must be authorized to alter a Boat in any way. Thus, a User is only allowed to alter their own Boats.

  - **Load Entities** (User-independent)
  
    - Have five stored attributes:
      - unique ID value
      - name of the Load's item
      - volume
      - creation date
      - carrier (set to `NULL`, can hold a Boat that "loaded" the Load)
    - Only the item name, volume, creation date, and carrier can be altered by a user.
    - No User-dependency means any loads can be altered by anyone, except the special case where a `carrier` is edited. Altering it requires User authorization because this operation also alters a Boat's `loads` array.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Gaining Access to the API

  1) To access the API, a user must first create an account or log in to the API's simple website. This web page provides a link to the `\login` endpoint of the API, which begins a login process through Auth0. Click on the pictures to make them larger.

  Home Page                  | Auth0 Login               | User Info Page with JWT
  :-------------------------:|:-------------------------:|:-------------------------:
  ![Screenshot of the simple login website with a login link.](/assets/images/493-01a-welcome_page.png)  |  ![Screenshot of the Auth0 login page with email and password fields, continue button, sign up link, and login with Google button.](/assets/images/493-01b-auth0_login.png)  |  ![Screenshot of the web page of the user's information on Auth0 in JSON format after successful login](/assets/images/493-02-jwt_info.png)

  2) After successful login, see above that the user's information on Auth0 is displayed to them along with a time-sensitive JWT token. If this is the first time the user has logged in, a User entity is created on the Google Datastore database. 
  
  3) For API interactions with Boats, the user must copy the JWT in `id_token` for use as a bearer token when making API requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Interacting with the API

The API has multiple endpoints that users can utilize to interact with the API. The API will send back all responses with an appropriate HTTP status code depending on the operation and/or any errors that occur in processing the request. All of the endpoints require any request bodies to be sent in JSON format. For full specifications, status codes, and example responses, check the [project documentation](/assets/documents/lubranoa_project.pdf).

#### Interactions with Users
  
  - Read a Collection of All Users (No pagination)
    - GET `/users`
    - Allows a user to get a list of all users on the application.
    - Authorization: *None*
    - Full description on page **3** of the [project documentation](/assets/documents/lubranoa_project.pdf).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Interactions with Boats (User-dependent)

  - Find full descriptions for Boat operations starting on page **4** of the [project documentation](/assets/documents/lubranoa_project.pdf).
  - All of the following Boat endpoints require authorization to successfully be carried out. 
    - **Authorization**: User's time-sensitive JWT set as a bearer token with Boat endpoint requests.
  
  - Create a Boat
    - **POST** `/boats`
    - Allows a user to create a new Boat.
    - Request body must contain a Boat's three required attributes, a name, boat type, and length. The API will set up a unique ID and a loads array to track any Loads it will carry.

      <details>
        <summary><i>Screenshot of Boat Creation in Postman</i></summary>

        ![Screenshot of a Postman tab displaying a POST request to create a Boat. The screenshot also displays a successful "201 Created" response from the API containing the new Boat object.](/assets/images/493-03-create-boat.png)

      </details>
  
  - Read a single Boat
    - **GET** `/boats/<boat_id>`
    - Allows a user to get one of their existing Boats.

  - Read all Boats (Supports pagination)
    - **GET** `/boats` (no queries defaults to an offset of zero)
    - **GET** `/boats?limit=5&offset=<n>` (where `n` is the number of Boats to skip)
    - Allows a user to get a list of all of their Boats, 5 per page max.
    - If the returned list contains an attribute `next`, then there are more Boats on another page.
    
  - Partially Update a Boat
    - **PATCH** `/boats/<boat_id>`
    - Allows a user to partially update one of their existing Boats.

  - Fully Update a Boat
    - **PUT** `/boats/<boat_id>`
    - Allows a user to completely update one of their existing Boats.
  
  - Delete a Boat
    - **DELETE** `/boats/<boat_id>`
    - Allows a user to delete one of their existing Boats.
    - If the Boat holds any Loads, "unloads" them by changing any Loads' carrier value to `NULL`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
   
#### Interactions with Loads (User-independent)

  - Find full descriptions for Load operations starting on page **18** of the [project documentation](/assets/documents/lubranoa_project.pdf).    
  - The following Load endpoints require no authorization. This was part of the assignment specifications set forth by the professor. Would it make sense to require authorization to access Loads even if they are User-independent? Yes, but that was out of scope of the assignment.
    - Authorization: *None*
  
  - Create a Load
    - **POST** `/loads`
    - Allows a user to create a new Load.
    - Request body must contain a Load's three required attributes, an item name, volume, and creation date. The API will set up a unique ID and a carrier attribute to track any Boat it will be loaded on.

      <details>
        <summary><i>Screenshot of Load Creation in Postman</i></summary>

        ![Screenshot of a Postman tab displaying a POST request to create a Load. The screenshot also displays a successful "201 Created" response from the API containing the new Load object.](/assets/images/493-04-create-load.png)

      </details>
  
  - Read a single Load
    - **GET** `/loads/<load_id>`
    - Allows a user to get an existing Load with its information.

  - Read all Loads (Supports pagination)
    - **GET** `/loads` (no queries defaults to an offset of zero)
    - **GET** `/loads?limit=5&offset=<n>` (where `n` is the number of Loads to skip)
    - Allows a user to view all existing Loads, 5 per page max.
    - If the returned list contains an attribute `next`, then there are more Loads to be read.
  
  - Partially Update a Load
    - **PATCH** `/loads/<load_id>`
    - Allows a user to partially update an existing Load.

  - Fully Update a Load
    - **PUT** `/loads/<load_id>`
    - Allows a user to completely update an existing Load.
  
  - Delete a Load
    - **DELETE** `/loads/<load_id>`
    - Allows a user to delete an existing Load.
    - If the Load being deleted is "loaded" on a Boat, unloads it from the Boat.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
#### Interactions between Boats and Loads
  
  - Find full descriptions for Boat operations starting on page **30** of the [project documentation](/assets/documents/lubranoa_project.pdf).
  - These create or remove Boat and Load dependencies on each other. Because Boats are being edited, Authorization is required in the same manner as above.
    - **Authorization**: User's time-sensitive JWT set as a bearer token with Boat endpoint requests.
  
  - Add a Load to a Boat
    - **PUT** `/boats/<boat_id>/loads/<load_id>`
    - Allows a user to put a Load on one of their Boats.
    - Only succeeds if the Boat and Load exist, the Boat is owned by the user, and the Load is not already on another Boat.

      <details>
        <summary><i>Screenshots of Putting a Load on a Boat in Postman</i></summary>

        Put Load on Boat           | Boat with One Load Added  | Load with Carrier
        :-------------------------:|:-------------------------:|:-------------------------:
        ![Screenshot of a Postman tab displaying a PUT request to add a Load to a Boat. The screenshot also displays a successful "204 No Content" response from the API.](/assets/images/493-05b-add-load-to-boat.png)  |  ![eenshot of a Postman tab displaying a GET request to get the same Boat as earlier. The screenshot also displays a successful "200 OK" response from the API containing the requested Boat object now with a Load on it.](/assets/images/493-05c-load-added.png)  |  ![Screenshot of a Postman tab displaying a GET request to get the Load being loaded. The screenshot also displays a successful "200 OK" response from the API containing the requested Load object now with a carrier.](/assets/images/493-05d-load-with-carrier.png)
        
      </details>

  - Delete a Load from a Boat
    - **DELETE** `/boats/<boat_id>/loads/<load_id>`
    - Allows a user to remove an Load from one of their Boats.
    - Only succeeds if the Boat and Load exist, the Boat is owned by the user, and the Load is on the specified Boat.

      <details>
        <summary><i>Screenshot of Load Removal from a Boat in Postman</i></summary>

        Remove Load from Boat      | Boat with no Loads        | Load with No Carrier
        :-------------------------:|:-------------------------:|:-------------------------:
        ![Screenshot of a Postman tab displaying a DELETE request to remove a Load from a Boat. The screenshot also displays a successful "204 No Content" response from the API.](/assets/images/493-05e-del-load-off-boat.png)  |  ![Screenshot of a Postman tab displaying a GET request to get the same Boat again. The screenshot also displays a successful "200 OK" response from the API containing the requested Boat object now with no Loads.](/assets/images/493-05f-load-removed.png)  |  ![Screenshot of a Postman tab displaying a GET request to get the same Load again. The screenshot also displays a successful "200 OK" response from the API containing the requested Load object now without a carrier.](/assets/images/493-05g-load-carrier-removed.png)
        
      </details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Skills Applied -->
## Skills Applied

  - REST API Design and Implementation
  - User authentication and authorization using Auth0 and JWTs
  - Database integration using Google Cloud Datastore
  - HTTP Status Codes and API Error Handling
  - Google Cloud Platform services
  - Writing API Documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Contact -->
## Contact

Alexander Lubrano - [lubrano.alexander@gmail.com][email] - [LinkedIn][linkedin-url]

Project Link: [https://github.com/lubranoa/CS493-Portfolio-Project][repo-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Acknowledgements -->
## Acknowledgments
  
  - [Auth0: Python Tutorial][auth0-python-url]
  - [Auth0: Python API: Authorization][auth0-auth-url]
  - [Google: Building a Python 3 App on App Engine][google-python-url]
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

[auth0-python-url]: https://auth0.com/docs/quickstart/webapp/python
[auth0-auth-url]: https://auth0.com/docs/quickstart/backend/python/01-authorization
[google-python-url]: https://cloud.google.com/appengine/docs/standard/python3/building-app
[shields-url]: https://shields.io/
[icons-url]: https://simpleicons.org/
