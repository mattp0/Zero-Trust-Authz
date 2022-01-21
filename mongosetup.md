# Setup Mongo First time

This process is documented so it maybe automated in the future

- docker-compose up -d
- docker exec -it container /bin/bash
- mongo
- use admin
- create user with this json scheme
    ```db.createUser({
	# Sets the username for the administrative user
	user: "dbapi",
	# Sets the password for the administrative user
	pwd: "password123",
	# Sets the roles for the administrative user
	roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
    })
    ```
- use authn
- quit()
- exit
- restart monogo container should now be in secure mode