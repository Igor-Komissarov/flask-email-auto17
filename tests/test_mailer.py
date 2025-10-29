from unittest.mock import patch

from app.mailer import send_email


@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp):
    instance = mock_smtp.return_value.__enter__.return_value
    instance.send_message.return_value = {}
    assert send_email("Игорь", "test@example.com", "Привет!") is True


@patch("smtplib.SMTP", side_effect=Exception("Ошибка SMTP"))
def test_send_email_failure(mock_smtp):
    assert send_email("Игорь", "test@example.com", "Привет!") is False
