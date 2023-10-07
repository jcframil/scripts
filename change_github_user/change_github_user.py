#!/usr/bin/env python3

import subprocess

def change_github_user(user, mail):
  """Changes the GitHub user in Visual Studio Code.

  Args:
    user: The GitHub user name.
    mail: The Github user mail. 
  """

  # Set the global Git user name.
  subprocess.run(["git", "config", "--global", "user.name", user])

  # Set the global Git email address.
  subprocess.run(["git", "config", "--global", "user.email", mail])

  # Restart Visual Studio Code.
  subprocess.run(["code", "--restart"])

# Get the new GitHub user name from the user.
user = input("Enter the new GitHub user name: ")

# Get the new GitHub mail from the user.
mail = input("Enter the new GitHub user mail: ")

# Change the GitHub user in Visual Studio Code.
change_github_user(user, mail)

