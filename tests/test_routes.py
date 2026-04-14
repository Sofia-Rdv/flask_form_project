import pytest
from app import app


@pytest.fixture
def client():
    """
    Фикстура для создания тестового клиента Flask.

    Устанавливает флаг TESTING, чтобы исключить влияние на реальные логи и базу данных во время тестов,
    и предоставляет объект клиента для имитации HTTP-запросов.

    :yield: FlaskClient: Объект для выполнения запросов к приложению.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """
    Проверяет доступность главной страницы.

    Выполняет GET-запрос на маршрут '/' и проверяет код ответа 200,
    а также наличие ключевых слов формы в HTML-коде.

    :param client: Фикстура тестового клиента.
    """
    response = client.get('/')
    assert response.status_code == 200

    # Проверяем, что на странице есть слово form (регистронезависимо)
    assert b"form" in response.data.lower()


def test_submit_form_success(client):
    """
    Проверяет успешную обработку формы с валидными данными.

    Выполняет POST-запрос с корректным именем и email.
    Ожидает код 200 и наличие имени пользователя в ответе.

    :param client: Фикстура тестового клиента.
    """
    test_data = {'name': 'Ivan', 'email': 'ivan@example.com'}
    response = client.post('/submit', data=test_data, follow_redirects=True)

    assert response.status_code == 200
    # Проверяем, что на странице результата отобразилось имя с помощью декодировки
    assert "Ivan" in response.data.decode('utf-8')


def test_submit_form_missing_data(client):
    """
    Проверяет валидацию формы при пустом поле имени.

    Отправляет пустую строку в поле 'name' и ожидает код ошибки 400
    с соответствующим сообщением об ошибке на странице.

    :param client: Фикстура тестового клиента.
    """
    test_data = {'name': '', 'email': ''}
    response = client.post('/submit', data=test_data)
    assert response.status_code == 400
    assert "не можем обработать форму без Вашего имени" in response.data.decode('utf-8')


def test_page_not_found(client):
    """
    Проверяет обработку запроса к несуществующему маршруту.

    Выполняет запрос по случайному адресу и ожидает статус-код 404
    с соответствующим сообщением об ошибке на странице.

    :param client: Фикстура тестового клиента.
    """
    response = client.get('/some_non_existent_page')
    assert response.status_code == 404
    assert "Страница потерялась в космосе" in response.data.decode('utf-8')
