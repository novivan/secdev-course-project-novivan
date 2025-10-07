Feature: Производительность CRUD фич
  Scenario: p95 CRUD операций в пределах порога
    Given Сервис под нагрузкой 20 RPS
    When Выполняется 5-минутный тест для /features
    Then p95 времени ответа ≤ 200 ms

  Scenario: Ошибка при превышении нагрузки
    Given Сервис под нагрузкой 100 RPS
    When Выполняется тест для /features
    Then Доля 5xx ошибок ≤ 5%

Feature: Уникальность голосов
  Scenario: Пользователь голосует один раз за фичу
    Given Пользователь авторизован
    When Он отправляет POST /features/123/vote
    Then Последующие голосы возвращают 409 Conflict

Feature: Доступность топ-фич
  Scenario: Эндпоинт /features/top доступен
    Given Сервис работает
    When Запрос GET /features/top
    Then Ответ 200 OK в 99.9% случаев за месяц
