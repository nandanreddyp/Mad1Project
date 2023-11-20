<div align="center">
  <a href="https://github.com/nandanreddyp/Mad1Project">
    <img src="Musica/static/images/MusicaFavIcon.png" alt="Logo" width="80" height="80">
  </a>
 
  <h3 align="center">MAD1 Project </h3>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This Project is made by NandanReddy Parnapalli, for Modern Application Devlopment 1 course prject.

Main theme of this project is to make a Music streaming application, enabling its users to explore
songs and albums uploaded by other users who became creators by registering, and creating playlists by
adding those songs. For overall control over users, Admin role can flag content uploaded by creators or
add them in blacklist and approve or reject premium requests made by users.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!--BUILT WITH -->
### Built With

* HTML & CSS and some Java Script
* Flask
Flask is a micro web framework for Python that is designed to be lightweight, flexible, and
easy to use.
* Flask Sqlalchemy
Flask-SQLAlchemy is an extension for Flask that simplifies the integration of SQLAlchemy,
it is a Object-Relational Mapping (ORM) library. SQLAlchemy provides a powerful and
flexible way to interact with databases using Python.
* Flask Migrate
Flask-Migrate is an extension that integrates the Alembic migration framework with Flask
applications, providing a convenient way to handle database schema changes.
* Flask Restful
Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs. It
simplifies the process of creating web services by providing tools and abstractions to
handle common tasks associated with RESTful APIs.
* Flask Login
Flask-Login is an extension for Flask that provides user session management, including
user authentication. It simplifies the process of managing user logins and sessions in Flask
applications.
* Bcrypt
Bcrypt is a Python library, used for implementing Bcrypt hashing the passwords before
storing them in a database to enhance security.
* Mutagen
Mutagen is a Python library that provides a set of tools for working with audio files. In this
project this is used to store song duration data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Set the root folder such that it includes Musica folder, requirements.txt, run.py.

Create a virtual environment by running command 'python -m venv FOLDER_NAME_YOU_WANT'

### Prerequisites

Prerequisits are mentioned in requirements.txt,


### Installation

After creating a virtual environment, run command 'pip install -r requirements.txt' and then all required packages will be installed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

After successful installnation, to run the project you need to run the run.py file.
In the root folder terminal you can run the command 'python run.py' and then we can see flask will provide link to view the project.

With that link any new user will be redirected to signup page and there they can create account and explore the app.

The app has types of user roles:
1. User : By registering for the first time anyone can get a user role, with user role users can
explore songs, albums and can create playlists and add songs to it. They can also download songs
but premium is required, for that they need to submit a form and the admin should accept it.
2. Creator : After registering any user can become a creator by registering as a creator and get that
role. With a creator role, users can upload songs, create albums and assign songs to it. If users do
something which violates the rules, their uploaded or created content gets flagged and its visibility
is removed for users or removed; or they can get blacklisted and further they can’t perform any
creator actions.
3. Admin : Admin can only be added in the backend, admin can login as normal users and they will
be redirected to the admin page. With an admin role a user can flag content and remove its
visibility in normal users, or they can directly blacklist a user to not do any creator task.

default admin credentials is email_id: 'admin@musica' and password is '12345678'


<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- CONTACT -->
## Contact

NandanReddy P - [@Telegram](https://t.me/nandanreddyp) - parnapalli2004@gmail.com

Project Link: [https://github.com/nandanreddyp/MAD1Project](https://github.com/nandanreddyp/MAD1Project)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Flask documentaion and its extension's documnetations help me to understand well and impliment basic structure and wire them for my main purpose.
* Stackoverflow for understanding errors and getting out of them.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
