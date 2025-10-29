from unittest.mock import patch

from app import app


def test_send_route_success():
    client = app.test_client()
    data = {"name": "Игорь", "email": "test@example.com", "message": "Привет!"}

    with patch("app.app.send_email", return_value=True):
        response = client.post("/send", data=data)
        html = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "Сообщение успешно отправлено" in html


def test_send_route_failure():
    client = app.test_client()
    data = {"name": "Игорь", "email": "test@example.com", "message": "Привет!"}

    with patch("app.app.send_email", return_value=False):
        response = client.post("/send", data=data)
        html = response.data.decode("utf-8")

        assert response.status_code == 400
        assert "Ошибка при отправке письма" in html
