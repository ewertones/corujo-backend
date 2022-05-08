docker build -t corujo-backend:Dockerfile .
docker run -e PORT=8000 -p 8000:8000 corujo-backend:Dockerfile

BACKEND

POST  /login    (user-id, password)
POST  /recover  (user-id) - recover password
POST  /user - create user
PATCH /user/{user-id} - update info
GET   /user/{user-id} - info from user
POST  /funds    (user-id, amount) - add/remove balance
POST  /update   (type, symbol) - retrieve recent data from stock market
POST  /predict  (type, symbol) - predict future values for stock market

FRONTEND

home
contact
login
forgot_password
forgot_password_sent
signup
app
app_profile
funds_more
funds_less
funds_ok

ACTORS

system
user
bank