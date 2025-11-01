# Url Shortener FastAPI Project

### 1. Clone the repository

```bash
git clone https://github.com/BarunBlog/url-shortner-fastapi-project.git
```

### 2. Create a `.env` file and set the environment variables

```bash
PORT=8000
MONGO_URI=mongodb://localhost:27018/url_shortener
BASE_URL=http://localhost:8000
```

### 3. Run the project

```bash
docker-compose up --build -d
```

### 4. Check the containers:

```bash
docker ps -a
```

### 5. Test the project

POST request to create a short URL  

```bash
curl -X POST http://localhost:8000/urls -H "Content-Type: application/json" -d '{"longUrl": "https://www.google.com"}' | jq
```

> Make sure to install `jq` to parse the JSON response.

```bash
sudo apt update
sudo apt install jq -y
```

GET request to redirect to the long URL

```bash
curl -X GET http://localhost:8000/urls/<shortUrlId>
```






