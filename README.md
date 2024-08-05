# Launch project locally:

Copy repo:
```bash
  git clone https://github.com/b1on1kkk/MalankaRouterBot.git
```

Create the `.env` file:
```bash
BOT_TOKEN="..."
CHARGING_POINTS_API=https://apigateway.malankabn.by/central-system/api/v1/locations/map/points
LOCATION_INF=https://apigateway.malankabn.by/central-system/api/v1/locations/map/info

POSTGRES_DB="..."
POSTGRES_USER="..."
POSTGRES_PASSWORD="..."
POSTGRES_HOST="..."
POSTGRES_PORT="..."

# Flask port
PORT="..."

REDIS_HOST="..."
REDIS_PORT="..."
REDIS_PASSWORD="..."
```


Run project:

```bash
  py main.py
```
