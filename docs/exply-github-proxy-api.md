# Exply.dev Platform API

Единый HTTP API для управления ресурсами платформы exply.dev:
- **Проекты** в `exply-dev/exply-dev-public-projects`
- **Профили экспертов** в `exply-dev/exply-dev-public-experts`

## 🌐 Service URL

```
https://exply-github-proxy-kwftltj4yq-uc.a.run.app
```

## 📋 OpenAPI Specification

**Актуальная схема (рекомендуется):**
```
https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-project-proposals-api.json
```

**Старая схема (legacy, не рекомендуется):**
```
https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-github-proxy-api.json
```

## 🔧 Использование в ChatGPT

### Шаг 1: Добавление API в Custom GPT

1. Откройте редактор вашего GPT
2. Перейдите в раздел **Actions** (Действия)
3. Нажмите **Create new action** (Создать новое действие) или используйте существующее
4. В поле **Schema** вставьте ссылку на OpenAPI спецификацию:
   ```
   https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-project-proposals-api.json
   ```
5. ChatGPT автоматически загрузит схему и обнаружит все доступные операции

### Шаг 2: Доступные операции

После добавления схемы GPT получит доступ к следующим операциям:

**Управление проектами:**
- `create_project_issue` - Создать новое предложение проекта
- `update_project_issue` - Обновить существующее предложение
- `get_project_issue` - Получить детали проекта
- `list_project_issues` - Список всех проектов

**Управление лейблами:**
- `get_labels` - Получить все лейблы репозитория
- `create_label` - Создать новый лейбл

**Управление профилями экспертов:**
- `create_expert_profile` - Создать или обновить профиль эксперта
- `get_expert_profile` - Получить профиль эксперта
- `list_experts` - Список всех экспертов

## 📝 Примеры использования

### Создание проекта

```bash
POST /create_project_issue
{
  "title": "Project Proposal: My Amazing App",
  "body": "### Concept\n\nMy app description...",
  "labels": ["project-proposal"]
}
```

### Создание профиля эксперта

```bash
POST /create_expert_profile
{
  "filename": "john-doe.md",
  "content": "# John Doe - Full-Stack Engineer\n\n**Status:** Active...",
  "message": "Create expert profile: john-doe.md"
}
```

### Получение профиля эксперта

```bash
POST /get_expert_profile
{
  "filename": "john-doe.md"
}
```

## 🔐 Аутентификация

API публичный и не требует аутентификации. GitHub токен хранится на сервере.

## 📊 Endpoints

**Основные:**
- `GET /` - Health check

**Проекты:**
- `POST /create_project_issue` - Создать проект
- `POST /update_project_issue` - Обновить проект
- `POST /get_project_issue` - Получить проект
- `POST /list_project_issues` - Список проектов

**Лейблы:**
- `GET /get_labels` - Список лейблов
- `POST /create_label` - Создать лейбл

**Эксперты:**
- `POST /create_expert_profile` - Создать/обновить профиль
- `POST /get_expert_profile` - Получить профиль
- `GET /list_experts` - Список экспертов

**Legacy MCP (для обратной совместимости):**
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

- [Project Proposals Repository](https://github.com/exply-dev/exply-dev-public-projects)
- [Experts Profiles Repository](https://github.com/exply-dev/exply-dev-public-experts)
- [OpenAPI Specification (JSON)](../api/exply-project-proposals-api.json)
- [Main README](../README.md)

## 💡 Архитектурное решение

**Почему один API для всех операций?**

✅ **Простота поддержки** - один сервис, одна конфигурация  
✅ **Логическая связность** - все операции связаны с exply.dev платформой  
✅ **Меньше дублирования** - общий код аутентификации и обработки ошибок  
✅ **Единая точка мониторинга** - проще отслеживать использование  

Если в будущем понадобится разделение по производительности или масштабированию, можно будет создать отдельные сервисы, но сейчас один API оптимальнее.

