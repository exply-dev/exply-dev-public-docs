# Exply GitHub Proxy MCP API

HTTP API для управления проектами в репозитории `exply-dev/exply-dev-public-projects`.

## 🌐 Service URL

```
https://exply-github-proxy-kwftltj4yq-uc.a.run.app
```

## 📋 OpenAPI Specification

**Ссылка на спецификацию:**
```
https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-github-proxy-api.json
```

## 🔧 Использование в ChatGPT

### Шаг 1: Добавление API в Custom GPT

1. Откройте редактор вашего GPT
2. Перейдите в раздел **Actions** (Действия)
3. Нажмите **Create new action** (Создать новое действие)
4. В поле **Schema** вставьте ссылку на OpenAPI спецификацию:
   ```
   https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-github-proxy-api.json
   ```
5. ChatGPT автоматически загрузит схему и обнаружит доступные операции

### Шаг 2: Доступные операции

После добавления схемы GPT получит доступ к следующим операциям:

- **`create_project_issue`** - Создать новое предложение проекта
- **`update_project_issue`** - Обновить существующее предложение
- **`get_project_issue`** - Получить детали проекта
- **`list_project_issues`** - Список всех проектов

## 📝 Примеры использования

### Создание проекта

```json
{
  "name": "create_project_issue",
  "arguments": {
    "title": "Project Proposal: My Amazing App",
    "body": "### Concept\n\nMy app description...",
    "labels": ["project-proposal"]
  }
}
```

### Получение проекта

```json
{
  "name": "get_project_issue",
  "arguments": {
    "issueNumber": 1
  }
}
```

## 🔐 Аутентификация

API публичный и не требует аутентификации. GitHub токен хранится на сервере.

## 📊 Endpoints

- `GET /` - Health check
- `GET /tools/list` - Список доступных инструментов
- `POST /tools/call` - Вызов инструмента MCP

## 🧪 Тестирование

```bash
# Health check
curl https://exply-github-proxy-kwftltj4yq-uc.a.run.app/

# Создать issue
curl -X POST https://exply-github-proxy-kwftltj4yq-uc.a.run.app/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "create_project_issue",
    "arguments": {
      "title": "Test Project",
      "body": "Test description"
    }
  }'
```

## 🔗 Связанные ресурсы

- [Repository: exply-dev-public-projects](https://github.com/exply-dev/exply-dev-public-projects)
- [API Specification (JSON)](../api/exply-github-proxy-api.json)

