# Django Tierlist Webpage.

## Overview

Welcome to my first Django project, a dynamic tierlist webpage featuring a custom-made login system and a unique statistical analysis feature. This project is a dynamic tierlist webpage, is part of my showcase and study of custom-made implemantations of Django's built-in systems

## Key Features

1. **Custom Login System**
   - Developed from scratch to gain a deeper understanding of authentication, token generation and email backend in Django.

2. **Tierlist Statistics**
   - Gain insights into character popularity with a comprehensive statistical analysis.
   - Track how many times each character has been placed on a specific tier across the entire domain.

3. **User-Friendly Image Management**
   - Create tierlists effortlessly by dragging and dropping images into the designated TextField.
   - Simple template creation using comma-separated URLs for image references.

## Project Insights

While this project represents my initial venture into Django development, I acknowledge areas for improvement, such as:

1. Refining data models:
   - Learning that adding `unique=True` to a field creates an index under the hood was a crucial revelation, if you're not aware of this in Django you can endup in a duplicated index situation that is kind of probelmatic
   - Do not use huge fields (such as Texfield, Blobs, JSON) if is not critically required. This type of fields are very huge and the DBMS will use more memory to manage these fields even though you're not putting to much information in it, this is because       the DBMS will think "Oh, this is a Textfield! (in this case) it could have a large amount of data so I'll use more resources to handle it. A better approach could be using a Charfield inside of an ArrayField but we're getting out of the topic with          technical things


2. Do *NOT* pull the entire database over the wire to do some sort of calculation:
   - If you want to do a calculation such as count the number of instances in a table, for the love of god don't pull the entire database over the wire. This approach is very inefficient for many reasons, instead something that you can do is leave this          type of calculation at the database level and retrieve the actual value that you're looking for


3. Efficient Database Querying:
   - Avoid pulling the entire database when you only need specific columns.
   - Performing `MyModel.objects.all()`, extracting a single row or a few rows for targeted use and discarding the surplus data, is highly inefficient.
   - Instead, opt for a more resource-efficient approach using the values method. For instance, you can use `MyModel.objects.values('select your columns here')` to retrieve only the necessary data, minimizing unnecessary data retrieval and optimizing performance.
