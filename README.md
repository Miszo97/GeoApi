# GeoApi
REST API for storing address geolocation data

Heroku application:
```
https://still-dusk-81333.herokuapp.com
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
'{"username": "aston", "password": "SsvL48Y6TGGNKRh"}' \
 'http://localhost:8000/api/token/'
```

## Usage:
### Get geo data from all addresses:

```
curl -i -X GET \
   -H "Authorization:Bearer TOKEN" \
 'http://localhost:8000/addresses'
```

### Get address's details:
```
curl -i -X GET \
   -H "Authorization:Bearer TOKEN" \
'http://localhost:8000/addresses/www.google.com'
```
### Create new address geo data:
```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -H "Authorization:Bearer TOKEN" \
   -d \
'{"address": "www.google.com"}
' \
 'http://localhost:8000/addresses'
 ```

### Delete address geo data:

```
curl -i -X DELETE \
   -H "Authorization:Bearer TOKEN" \
 'http://localhost:8000/addresses/51.83.237.191'
```
