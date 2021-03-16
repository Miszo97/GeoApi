# GeoApi
REST API for storing address geolocation data

![http request](http_request.png?raw=true "Http request")

Heroku application:
```
https://still-dusk-81333.herokuapp.com
```

Docker image:
```
https://hub.docker.com/repository/docker/kol478/geo-api
```

## Register your account:

Before accessing data or creating new data you have to register your account.

```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{"username": "jacksparrow", "password": "U3CdUw"}' \
 'http://localhost:8000/register'
 ```

## Obtain JWT Token
API is protected with a JWT token. Get one with:

```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{"username": "jacksparrow", "password": "U3CdUw"}' \
 'http://localhost:8000/api/token/'
```
When this short-lived access token expires, you can get another one with an obtained refreshed token.

```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{"refresh": REFRESH TOKEN}' \
 'http://localhost:8000/api/token/refresh/'
```

## Usage:
### Get geo data from all addresses:

```
curl -i -X GET \
   -H "Authorization:Bearer TOKEN" \
 'http://localhost:8000/addresses/'
```

### Get address's details:
```
curl -i -X GET \
   -H "Authorization:Bearer TOKEN" \
'http://localhost:8000/addresses/www.google.com/'
```
### Create new address geo data:
```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -H "Authorization:Bearer TOKEN" \
   -d \
'{"address": "www.google.com"}
' \
 'http://localhost:8000/addresses/'
 ```

### Delete address geo data:

```
curl -i -X DELETE \
   -H "Authorization:Bearer TOKEN" \
 'http://localhost:8000/addresses/51.83.237.191/'
```
