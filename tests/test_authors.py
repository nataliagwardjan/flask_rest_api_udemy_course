def test_get_authors_no_records(client):
    response = client.get("/api/v1/authors")
    expected_result = {
        "success": True,
        "data": [],
        "number_of_records": 0,
        "pagination": {
            "total_pages": 0,
            "total_records": 0,
            "current_page": "/api/v1/authors?page=1"
        }
    }

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.get_json() == expected_result


def test_get_authors(client, sample_data):
    response = client.get("/api/v1/authors")
    expected_pagination = {
        "total_pages": 2,
        "total_records": 10,
        "current_page": "/api/v1/authors?page=1",
        "next_page": "/api/v1/authors?page=2"
    }
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response_data["success"] is True
    assert response_data["number_of_records"] == 5
    assert len(response_data["data"]) == 5
    assert response_data["pagination"] == expected_pagination


def test_get_authors_with_params(client, sample_data):
    response = client.get("/api/v1/authors?fields=first_name&sort=-id&page=2&limit=2")
    expected_pagination = {
        "total_pages": 5,
        "total_records": 10,
        "current_page": "/api/v1/authors?page=2&fields=first_name&sort=-id&limit=2",
        "next_page": "/api/v1/authors?page=3&fields=first_name&sort=-id&limit=2",
        "previous_page": "/api/v1/authors?page=1&fields=first_name&sort=-id&limit=2"
    }
    expected_data = [
        {
            "first_name": "Alice"
        },
        {
            "first_name": "Dan"
        }
    ]

    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response_data["success"] is True
    assert response_data["number_of_records"] == 2
    assert response_data["data"] == expected_data
    assert response_data["pagination"] == expected_pagination
