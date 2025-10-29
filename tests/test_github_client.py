from unittest.mock import patch

from app import github_client


@patch("app.github_client.requests.get")
@patch("app.github_client.requests.put")
@patch("app.github_client.TOKEN", "fake-token")
def test_create_or_update_file_new(mock_put, mock_get, capsys):
    """Проверяет, что функция делает правильный PUT-запрос и обрабатывает ответ."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"sha": "fake-sha"}
    mock_put.return_value.status_code = 200
    mock_put.return_value.text = "OK"

    github_client.create_or_update_file(
        repo="user/repo", path="test.txt", content="hello", message="Add test.txt"
    )

    args, kwargs = mock_put.call_args
    assert "repos/user/repo/contents/test.txt" in args[0]
    assert kwargs["json"]["message"] == "Add test.txt"
    assert "content" in kwargs["json"]

    output = capsys.readouterr().out
    assert "Коммит успешно создан!" in output  # без b, т.к. output — строка


@patch("app.github_client.requests.get")
@patch("app.github_client.requests.put")
@patch("app.github_client.TOKEN", "fake-token")
def test_create_or_update_file_error(mock_put, mock_get, capsys):
    """Проверяет обработку ошибки при неудачном PUT."""
    mock_get.return_value.status_code = 404
    mock_put.return_value.status_code = 400
    mock_put.return_value.text = "Bad Request"

    github_client.create_or_update_file(
        repo="user/repo", path="fail.txt", content="data", message="Fail test"
    )

    output = capsys.readouterr().out
    assert "Ошибка" in output
