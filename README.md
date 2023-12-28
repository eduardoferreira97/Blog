# Django Blog System

This project is a simple ✨ blog system ✨ developed in Django. It has the following features:

    Login: Users can register and log in to the system.
    Create post: Registered users can create new posts.
    Edit post: Registered users can ✏️ edit their own posts.
    Delete post: Registered users can delete their own posts.
    Post search: Users can search for posts.
    Image addition: Users can add images to their posts.

# Requirements 

To run this project, you will need the following:

    Python 3.8 or higher
    Django 4.1 or higher
    PostgreSQL 13 or higher

# Installation

To install the project, follow these steps:

1.Clone the GitHub repository:

    git clone https://github.com/eduardoferreira97/Blog.git

2.Change to the project directory:

    cd Blog

3.Create a virtual environment:

    python3 -m venv venv

4.Activate the virtual environment:

    source venv/bin/activate

5.Install the dependencies:

    pip install -r requirements.txt

6.Create the database:

    python manage.py migrate

7.Create a superuser:

    python manage.py createsuperuser

# Running

To run the project, follow these steps:

-Start the development server:

    python manage.py runserver

Open your browser and navigate to the address http://localhost:8000.

# Usage example

To create a new post, follow these steps:

    Login to the system.
    Click the "Create post" link.
    Fill out the form with the post information.
    Click the "Create" button.

To edit a post, follow these steps:

    Log in to the system.
    Click the "Edit" link next to the post you want to edit.
    ✏️ Make the necessary changes to the form.
    Click the "Save" button.

To delete a post, follow these steps:

    Click the "Delete" link next to the post you want to delete.
    ❌ Click the "Delete" button to confirm the deletion.

To search for posts, follow these steps:

    Type the keyword you want to search for in the search bar.
    Click the "Search" button.

To add an image to a post, follow these steps:

    Click the "Edit" link next to the post you want to edit.
    Click the "Add image" button.
    Select the image you want to add.
    Click the "Save" button.
