### REST API microservice for user authentication written in FastAPI

Information about registered users is stored in the database. 

**Implemented endpoints**

*for everyone:*
- register a new user

*for registered users:*
- login user with JWT token,
- forgot password, 
- reset password

*for authenticated users only:*
- get user profile info,
- update user profile info,
- deactivate account,
- change password,
- logout,
- upload profile image,
- get profile image


#### Technologies
Python, FastAPI, SQLAlchemy, PostgreSQL

#### Instructions
to run project locally: 

`uvicorn main:app --host "0.0.0.0" --port 8000 --reload`
