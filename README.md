# Indico Hub

This is a microservice for the Indico Community Hub.

### Development setup
```
pip install -e '.[dev]'
npm ci
```

### Running Test Server
```
flask run -p 12345
```

### Consulting API Docs
```
npm run api-docs
```

Docs available at http://localhost:5000

### Running Swagger UI (Docker required)

First, let's run the test server with CORS enabled
```
FLASK_ENABLE_CORS=1 flask run -p 12345
```

Then, run the Swagger UI:
```
npm run swagger-ui
```

Swagger UI available at http://localhost:5001

 
### Elasticsearch Config 
**This microservice uses geoip to locate instances.** Thus before using it: 
        1) open kibana's **Dev Tools** 
        2) add geoip plugin to your workspace: 
```
PUT _ingest/pipeline/geoip 
{ 
  "description" : "Add geoip info", 
  "processors" : [ 
    { 
      "geoip" : { 
        "field" : "ip" 
      } 
    } 
  ] 
}        
``` 
   3)To use geoip plugin, confugre your index to produce a geopoint upon locating the instance: 
``` 
put **nameOfYourIndex** 
{ 
  "mappings": { 
    "properties": { 
      "geoip.location": { 
        "type": "geo_point" 
      } 
    } 
  } 
} 
```

