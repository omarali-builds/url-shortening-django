# Django URL Shortener API

A simple URL shortening service built with Django. Users can create shortened URLs, access statistics about them, and redirect to the original destination using a generated short code.

## Features

* Create short URLs
* Redirect users to the original URL
* Handle short URLs through dedicated endpoints
* REST-style API endpoints

---

## API Endpoints

### Create a Short URL

**POST** `/shorten`

Creates a new shortened URL.

#### Request Example

```json
{
    "url": "https://example.com"
}
```

#### Response Example

```json
{
    "short_code": "abc123",
    "short_url": "http://localhost:8000/abc123"
}
```

---

### Handle a Short URL

**GET** `/shorten/<short_code>`

Retrieves information about a specific shortened URL.

#### Example

```http
GET /shorten/abc123
```

---

### Get URL Statistics

**GET** `/shorten/<short_code>/stats`

Returns statistics for a shortened URL.

#### Example

```http
GET /shorten/abc123/stats
```

#### Sample Response

```json
{
    "short_code": "abc123",
    "clicks": 42,
    "created_at": "2025-05-15T10:30:00Z"
}
```

---

### Redirect to Original URL

**GET** `/<short_code>`

Redirects the user to the original URL associated with the provided short code.

#### Example

```http
GET /abc123
```

Response:

```http
302 Found
Location: https://example.com
```

---

## Project Structure

```text
project/
│
├── urls.py
├── views.py
├── models.py
├── serializers.py
├── migrations/
└── manage.py
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

---

## Example Workflow

1. Send a POST request to `/shorten`.
2. Receive a generated `short_code`.
3. Share the shortened URL.
4. Users visit `/<short_code>`.
5. The application redirects them to the original URL.
6. View analytics using `/shorten/<short_code>/stats`.

---

## Technologies Used

* Python
* Django
* Django REST Framework
* SQLite

---

## Future Improvements

* User authentication
* Custom short codes
* URL expiration dates
* QR code generation
* Rate limiting
* Detailed analytics dashboard

---

## License

This project is open source and available under the MIT License.
