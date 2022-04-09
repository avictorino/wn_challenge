
#### Docker build

Execute to start the docker container
* docker build -t wn_challenge .
* docker run -d --publish 8001:8001 wn_challenge
* Pushed the sqlite file together the code just to start the container already filled with data

#### Django Admin:
* http://127.0.0.1:8001/admin/
* user: admin
* password: 123123
All tree models are designed to allow the edition the relationships and display the related data. 

#### View to test the elapsed time:
http://127.0.0.1:8001/buyers/
 

### Coding Challenges

#### Problem 1 (Python)
Provide some Python code that can be used to measure how long a function takes to run in a friendly
format. The amount of time can range from less than a second to several hours and should be easy
for a human to read (for example “00:00:00:00012” is not a good output).

Created one decorator to append the elapsed time in all requests
https://github.com/avictorino/wn_challenge/blob/main/core/decorators.py

#### Problem 2 (Modeling)
We have a system where products can be placed into catalogs and buyers are assigned to a catalog.
Products can have different visibility settings. 

If the visibility setting is “default” then any buyer can see the product. 
If the visibility is “catalog_members” then only buyers who are a member of a catalog
including the product can see it. 

A query for products on behalf of a buyer should return any product
that has visibility “default” OR the product exists in a catalog that includes the buyer. A product has a
name, price, and visibility setting.
##### a) How would you model these relationships?

Have a look into the models.py file:
https://github.com/avictorino/wn_challenge/blob/main/core/models.py

##### b) How would you write a SQL query to return the list of products?

```sql
SELECT
	"core_product"."id",
	"core_product"."name",
	"core_product"."price",
	"core_product"."visibility"
FROM
	"core_product"
WHERE
	("core_product"."id" IN (
	SELECT
		U0."id"
	FROM
		"core_product" U0
	INNER JOIN "core_catalog_products" U1 ON
		(U0."id" = U1."product_id")
	WHERE
		U1."catalog_id" = 1)
	OR "core_product"."visibility" = DEFAULT)
```

Result of http://127.0.0.1:8001/buyers/ after the decorator
```json
{
  "elapsed_time": "spend 0.007 seconds to process",
  "buyers": [
    {
      "name": "Jhon",
      "catalog": {
        "name": "CAT1"
      },
      "products": [
        {
          "name": "Letuce",
          "price": "100.00",
          "visibility": "default"
        },
        {
          "name": "Soybeans",
          "price": "52.00",
          "visibility": "default"
        },
        {
          "name": "Lentils",
          "price": "47.00",
          "visibility": "catalog_members"
        },
        {
          "name": "Celery",
          "price": "15.00",
          "visibility": "default"
        }
      ]
    },
    {
      "name": "Jack",
      "catalog": {
        "name": "CAT2"
      },
      "products": [
        {
          "name": "Letuce",
          "price": "100.00",
          "visibility": "default"
        },
        {
          "name": "Soybeans",
          "price": "52.00",
          "visibility": "default"
        },
        {
          "name": "Celery",
          "price": "15.00",
          "visibility": "default"
        }
      ]
    },
    {
      "name": "Johnson",
      "catalog": {
        "name": "CAT2"
      },
      "products": [
        {
          "name": "Letuce",
          "price": "100.00",
          "visibility": "default"
        },
        {
          "name": "Soybeans",
          "price": "52.00",
          "visibility": "default"
        },
        {
          "name": "Celery",
          "price": "15.00",
          "visibility": "default"
        }
      ]
    }
  ]
}
```