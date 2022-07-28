# Final Project
#### Video Demo:  <https://youtu.be/nB-lPZdIVVk>

# In the final project, the user can create his username and password, create his own article, edit it and delete it. Can leave comments on the article.

## Registration function.
Asks the user to enter an email, login, password and confirm the password. Checks if the user entered an email,
login, password and password confirmation, if the user forgot to enter the login, password and confirm the password,
it will display an error. If the user has entered all the data, it writes them to the database. After registration,
go to the login function.

## Login function.
Prompts the user to enter a username and login. If the user has not entered a username or password, or has entered
an incorrect password, an error will be displayed. If everything is entered correctly, the user will be logged in.

## Index function.
Displays all categories and title of all entered articles, the name of the user who created the article and
the time it was created. There is also a link to read the article to the user. All data is taken from the table of articles.

## Editing function.
The edit function allows the user to edit the article he has added. It opens a page with fields in which text has already
been inserted with the category, name and text of the article. After the user makes changes, he saves the changes to the database.

## Delete function.
Allows the user to delete an article. When deleting an article, it checks which user created the article and if the
name of the user who wants to delete the article and the name of the author of the article does not match, it gives an
error that the user does not have the right to delete it. If the username and the author of the article match, deletes the article.

## Comment function.
Allows the user to post comments on the article. When you open an article, it shows the category, the name of
the article and the text of the article and then the comments that users left, shows the text of the comment, the name
of the user who left the comment and the date the comment was created.

## Password change function.
Allows the user to change the password. Opens a page on which prompts the user to enter the old password, new
password and confirm the new password. Checks if the user has not entered the old password or entered the wrong
password or has not entered a new password generates an error. Checks if the new passwords match; if the new passwords
do not match, it throws an error. If the user has entered the correct old password and entered new passwords, the new password
hash is saved to the database.
