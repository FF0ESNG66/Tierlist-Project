# This is my first project in Django.
# It's a tlerlist webpage with a custom (made from scratch) login system and an extra feature. This feature is that you can go to the statistics of the tierlist to see how many times each character has been placed on a specific tier within the entire domain.
# On this project I haven't used the built-in login views of Django because I wanted to test and understand how it works.
# I read a lot and look for many resources to see what interested me and then add it to my project.
# Since I've been coding lot more since this project now I see a couple of thing I could've made better (specially defining a model), however, I do think is fine for a first try in Django and still works for me to improve it in a future :)

# The way this works is with the URLs of the images, when you create a template you gotta use the urls separated by a comma (",")

example: ur,url,url    <-- (no spaces)

Also, once you've created the template, you create a new tierlist by selecting the template and you only drag and drop the image to the TextField
Once created you'll see it on the main page and you can also see its statistics
