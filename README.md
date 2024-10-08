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
  <h1 align="center">Cloud-Deployed REST API with JWT Authentication</h1>
  <p align="center">
    <b>A RESTful API for Managing Boat and Load Assets on Google Cloud Platform with Auth0 Authentication</b>
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
    - [Gaining Full Access to the API](#gaining-full-access-to-the-api)
    - [Interacting with the API](#interacting-with-the-api)
      - [Get Collections of Entities](#get-collections-of-entities)
      - [Interactions with Boats](#interactions-with-boats-user-dependent)
      - [Interactions with Loads](#interactions-with-loads-user-independent)
      - [Interactions between Boats and Loads](#interactions-between-boats-and-loads)
  - [Skills Applied](#skills-applied)
  - [Contact](#contact)
  - [Acknowledgments](#acknowledgments)

</details>

<!-- Project Description -->
## Project Description

This project is a Flask REST API that allows users to interact with entities stored in a Google Cloud Datastore database via resource-based Flask endpoints, JSON Web Tokens (JWT), and Postman. The user can get a time-sensitive JWT by logging in to the project's simple website deployed on Google Cloud App Engine. This was the final project for Cloud Application Development and had the goals of implementing a REST API that incorporated proper resource-based URLs, pagination, and appropriate HTTP status codes as well as implementing some sort of system for creating users and authorization.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Technologies Used -->
## Technologies Used

  - Server
    - [![Python][Python]][Python-url]
    - [![Flask][Flask]][Flask-url]
    - [![Dotenv][Dotenv]][Dotenv-url]
    - [![Auth0][Auth0]][Auth0-url]
    - [![OAuth][OAuth]][OAuth-url]
    - [![JWT][JWT]][JWT-url]
    - [![App-engine][App-engine]][App-engine-url] (Deployment)
  - Database
    - [![Datastore][Datastore]][Datastore-url]
  - Client
    - [![Postman][Postman]][Postman-url] (API Testing and Use)
    - Can work with any client that can send requests with authorization such as Bearer tokens.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Features -->
## Features

  - RESTful CRUD endpoints for API interactions

  - User, Boat, and Load entities with varied relationships

  - JSON Web Token-based (JWT) authorization for Boat records

  - Token generation through website with Auth0 service

  - Stateless client-server communication

  - Integration with GCP Datastore NoSQL database

  - Relevant HTTP status codes and error handling

  - All entities represented as JSON

  - Creates resource links for entities in a response

  - Result pagination when getting collections of entities
  
  - *No Input Validation*
    - The assignment specifications stated there was no need for input validation as the graders would adhere to the guidelines outlined in our [personal documentation](/assets/documents/lubranoa_project.pdf).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Usage -->
## Usage

To use this API fully, the user must do three things, log in to the API's website, copy their generated token, and send it as a Bearer token along with API requests. Before getting to that, an explanation of the Boat, Load, and User entities of the API is in order. For a full description of the entities, their relationships, and their endpoints, see the [project documentation](/assets/documents/lubranoa_project.pdf).

### Entity Data Models and Relationships

The following is a quick outline of the API's entities' data models and relationships with the others. The assignment specifications called for three entities, a User entity and two non-User entities, one User-dependent and one User-independent, which had to be dependent on each other in some way. 

  - **User Entities**

    - Have two stored attributes, a unique `id` value, and a `name` (pulled from their Auth0 account)
    - Created when a user creates an account with the Auth0 service.
    - Cannot be edited.

  - **Boat Entities** (User-dependent)

    - Have six stored attributes:
      - a unique `id` value and a boat's `name`, `type`, `length`, `owner`, and `loads` (array that holds any Loads "loaded" on a Boat)
      - Only `name`, `type`, `length`, and `loads` can be altered by a user.
    - Will also have a dynamically generated `self` URL/link to itself, which is created at response-time by the API.
    - Never allowed to have no owner, creating User-dependency.
    - A User must be authorized to alter a Boat in any way. Thus, a User is only allowed to alter their own Boats.

  - **Load Entities** (User-independent)
  
    - Have five stored attributes:
      - a unique `id` value, a Load's `item` name, `volume`, `creation_date`, and `carrier` (the Boat that "loaded" the Load, initially set to `NULL`)
      - Only the `item`, `volume`, `creation_date`, and `carrier` can be altered by a user.
    - Will also have a dynamically generated `self` URL/link to itself, which is created at response-time by the API.
    - No User-dependency means any loads can be altered by anyone, except the special case where a `carrier` is edited. Altering it requires User authorization because this operation also alters a Boat's `loads` array.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Gaining Full Access to the API

  1) To fully access the API for interactions with Boat entities, a user must first create an account or log in to the API's simple website. This web page provides a link to the `\login` endpoint of the API, which begins an OAuth login process through the API and Auth0. Click on the pictures to view them on another page.
  
  | Home Page                  | Auth0 Login               | User Info Page with JWT  |
  | :------------------------: | :-----------------------: | :----------------------: |
  | ![Screenshot of the simple login website with a login link.](/assets/images/493-01a-welcome_page.png)  | ![Screenshot of the Auth0 login page with email and password fields, continue button, sign up link, and login with Google button.](/assets/images/493-01b-auth0_login.png)  | ![Screenshot of the web page of the user's information on Auth0 in JSON format after successful login](/assets/images/493-02-jwt_info.png) |

  2) After successful login, see above that the user's information on Auth0 is displayed to them along with a time-sensitive JWT token. If this is the first time the user has logged in, a User entity is created on the Google Datastore database. 
  
  3) For API interactions with Boats, the user must copy the JWT in `id_token` for use as a Bearer token when making API requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Interacting with the API

The API has multiple endpoints that users can utilize to interact with the API. The API will send back all responses with an appropriate HTTP status code depending on the operation and/or any errors that occur in processing the request. All of the endpoints require all request bodies to be sent in JSON format. For full specifications, status codes, and example request and responses, check the [project documentation](/assets/documents/lubranoa_project.pdf).

#### Get Collections of Entities

  | Method  | Endpoint                     | Authorization  | Description                              |    
  | ------- | ---------------------------- | -------------- | ---------------------------------------- |
  | GET     | `/users`                     | None           | Read a list of all Users. No pagination.  |
  | GET     | `/boats`                     | JWT as Bearer  | Read a list of all the user's Boats. Supports pagination.  |
  | GET     | `/boats?limit=5&offset=<n>`  | JWT as Bearer  | Read a list of all the user's Boats. Pagination skips first `n` Boats.  |
  | GET     | `/loads`                     | None           | Read a list of all Loads. Supports pagination.  |
  | GET     | `/loads?limit=5&offset=<n>`  | None           | Read a list of all Loads. Pagination skips first `n` Loads.  |

For the two operations that support pagination, a full response of results is five maximum. If there are more, the returned list of results will also contain a `next` attribute that contains a link to the next set of results. Otherwise if there are no more results, `next` will be absent.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Interactions with Boats (User-dependent)

All of the following Boat endpoints require authorization to successfully be carried out. For endpoints that need a Boat specified, use the ID value of the Boat in place of `<boat_id>`. Find full descriptions and usage of Boat operations starting on page **4** of the [project documentation](/assets/documents/lubranoa_project.pdf).
  
  - Authorization: User's time-sensitive JWT set as a Bearer token with these requests.
  
  | Method  | Endpoint            | Description                              |    
  | ------- | --------------------| ---------------------------------------- |
  | POST    | `/boats`            | Create a new Boat. [Link to screenshot.](/assets/images/493-03-create-boat.png)  |
  | GET     | `/boats/<boat_id>`  | Read one of a user's Boats.              |
  | PATCH   | `/boats/<boat_id>`  | Partially update one of a user's Boats.  |
  | PUT     | `/boats/<boat_id>`  | Fully update one of a user's Boats.      |
  | DELETE  | `/boats/<boat_id>`  | Delete one of a user's Boats. If the Boat contains any Loads, "unloads" them.  |

<p align="right">(<a href="#readme-top">back to top</a>)</p>
   
#### Interactions with Loads (User-independent)

The following Load endpoints require no authorization. This was part of the assignment specifications set forth by the university. Would it make sense to require authorization to access Loads even if they are User-independent? Yes, but that was out of scope of the assignment.

For endpoints that need a Load specified, use the ID value of the Load in place of `<load_id>`. Find full descriptions and usage for Load operations starting on page **18** of the [project documentation](/assets/documents/lubranoa_project.pdf). 
  
  - Authorization: *None*
  
  | Method  | Endpoint            | Description                              |    
  | ------- | ------------------- | ---------------------------------------- |
  | POST    | `/loads`            | Create a new Load. [Link to screenshot.](/assets/images/493-04-create-load.png)  |
  | GET     | `/loads/<load_id>`  | Read a Load.                             |
  | PATCH   | `/loads/<load_id>`  | Partially update a Load.                 |
  | PUT     | `/loads/<load_id>`  | Fully update a Load.                     |
  | DELETE  | `/loads/<load_id>`  | Delete a Load. If on a Boat, "unloads" it from there.  |

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
#### Interactions between Boats and Loads
  
These create or remove Boat and Load dependencies on each other. Because Boats are being edited, Authorization is required in the same manner as above.  Find full descriptions for Boat operations starting on page **30** of the [project documentation](/assets/documents/lubranoa_project.pdf).
  
  - Authorization: User's time-sensitive JWT set as a Bearer token with these requests.

  | Method  | Endpoint                            | Description                              |  
  | ------- | ----------------------------------- | ---------------------------------------- |
  | PUT     | `/boats/<boat_id>/loads/<load_id>`  | Add a Load to one of the user's Boats.   |
  | DELETE  | `/boats/<boat_id>/loads/<load_id>`  | Remove a Load from one of the user's Boats.  |
  
Both of these operations will fail if the user does not own the Boat that it is altering. But adding a Load to a Boat fails if the Load is already loaded somewhere, whereas removing a Load fails if the Load is not loaded on the specified Boat.

The following screenshots show the loading and removal of a Load onto and off of a Boat owned by a User:

<details>
  <summary><i>Screenshots of Putting a Load on a Boat in Postman</i></summary>

  | Put Load on Boat         | Boat with One Load Added  | Load with Carrier        |
  | :----------------------: | :-----------------------: | :----------------------: |
  | ![Screenshot of a Postman tab displaying a PUT request to add a Load to a Boat. The screenshot also displays a successful "204 No Content" response from the API.](/assets/images/493-05b-add-load-to-boat.png)  | ![Screenshot of a Postman tab displaying a GET request to get the same Boat as earlier. The screenshot also displays a successful "200 OK" response from the API containing the requested Boat object now with a Load on it.](/assets/images/493-05c-load-added.png) |  ![Screenshot of a Postman tab displaying a GET request to get the Load being loaded. The screenshot also displays a successful "200 OK" response from the API containing the requested Load object now with a carrier.](/assets/images/493-05d-load-with-carrier.png)  |
  
</details>

<details>
  <summary><i>Screenshots of Removing a Load from a Boat in Postman</i></summary>

  | Remove Load from Boat      | Boat with no Loads        | Load with No Carrier  |
  | :------------------------: | :-----------------------: | :-------------------: |
  | ![Screenshot of a Postman tab displaying a DELETE request to remove a Load from a Boat. The screenshot also displays a successful "204 No Content" response from the API.](/assets/images/493-05e-del-load-off-boat.png)  | ![Screenshot of a Postman tab displaying a GET request to get the same Boat again. The screenshot also displays a successful "200 OK" response from the API containing the requested Boat object now with no Loads.](/assets/images/493-05f-load-removed.png)  | ![Screenshot of a Postman tab displaying a GET request to get the same Load again. The screenshot also displays a successful "200 OK" response from the API containing the requested Load object now without a carrier.](/assets/images/493-05g-load-carrier-removed.png)  |
  
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

  - Deploying web applications via Google App Engine

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
  - [Introduction to JWTs][JWT-url]
  - [Google: Building a Python 3 App on App Engine][google-python-url]
  - [Shields.io][shields-url]
  - [Simple Icons][icons-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Markdown links and images -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=ffd343
[Python-url]: https://www.python.org/

[Flask]: https://img.shields.io/badge/Flask-grey?style=for-the-badge&logo=flask
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/

[Auth0]: https://img.shields.io/badge/Auth0-16214d?style=for-the-badge&logo=auth0
[Auth0-url]: https://auth0.com/

[OAuth]: https://img.shields.io/badge/Authlib_OAuth_Library-grey?style=for-the-badge
[OAuth-url]: https://docs.authlib.org/en/latest/client/

[JWT]: https://img.shields.io/badge/JSON_Web_Tokens_(JWT)-grey?style=for-the-badge&logo=jsonwebtokens
[JWT-url]: https://jwt.io/introduction

[Datastore]: https://img.shields.io/badge/Google_Cloud_Datastore-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white
[Datastore-url]: https://cloud.google.com/datastore

[App-engine]: https://img.shields.io/badge/Google_App_Engine-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white
[App-engine-url]: https://cloud.google.com/appengine/?hl=en

[Postman]: https://img.shields.io/badge/Postman-ef5b25?style=for-the-badge&logo=postman&logoColor=white
[Postman-url]: https://www.postman.com/

[Dotenv]: https://img.shields.io/badge/Dotenv-grey?style=for-the-badge&logo=dotenv&logoColor=ecd53f
[Dotenv-url]: https://pypi.org/project/python-dotenv/

[email]: mailto:lubrano.alexander@gmail.com
[linkedin-url]: https://linkedin.com/in/lubrano-alexander
[repo-url]: https://github.com/lubranoa/CS493-Portfolio-Project

[auth0-python-url]: https://auth0.com/docs/quickstart/webapp/python
[auth0-auth-url]: https://auth0.com/docs/quickstart/backend/python/01-authorization
[google-python-url]: https://cloud.google.com/appengine/docs/standard/python3/building-app
[shields-url]: https://shields.io/
[icons-url]: https://simpleicons.org/
