#!/usr/bin/python3

from app import db, User, Role, Post, Tag

# Create Tables
db.create_all()

# Add user admin and editor
admin = User(first_name = "Jose", 
			last_name  = "Ramirez", 
			email      = "jose@bloggy.com",
			username   = "admin")
admin.set_password("admin")  
db.session.add(admin)
admin.roles.append(Role(name="admin"))


editor = User(first_name = "Maria", 
			last_name  = "Lopez", 
			email      = "maria@bloggy.com",
			username   = "maria")
editor.set_password("maria")  
db.session.add(editor)
editor.roles.append(Role(name="editor"))

# commit
db.session.commit() 