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
- `my_projects` - Получить проекты текущего пользователя

**Управление GitHub Projects:**
- При создании проекта автоматически создается GitHub Project
- Автоматически добавляются поля: Application Status, Expert Type, Expert Level
- Автоматически создается Draft Issue "Project Details"
- Создатель проекта добавляется как ADMIN collaborator
- Заявки экспертов автоматически добавляются в GitHub Project

**Управление заявками экспертов (для создателей проектов):**
- `list_project_applications` - Список заявок для проекта
- `update_application_status` - Обновить статус заявки
- `update_application_fields` - Обновить Expert Type и Expert Level

**Управление заявками (для экспертов):**
- `create_expert_application` - Создать заявку на проект
- `list_my_applications` - Список моих заявок
- `withdraw_application` - Отозвать заявку
- `update_my_application` - Обновить мою заявку

**Управление лейблами:**
- `get_labels` - Получить все лейблы репозитория
- `create_label` - Создать новый лейбл

**Управление профилями экспертов:**
- `create_expert_profile` - Создать или обновить профиль эксперта
- `get_expert_profile` - Получить профиль эксперта
- `list_experts` - Список всех экспертов

**Комментарии:**
- `add_issue_comment` - Добавить комментарий к issue

## 📊 GitHub Projects Integration

### Автоматическое создание GitHub Projects

При создании проекта через `create_project_issue`, API автоматически:

1. ✅ Создает GitHub Project (V2)
2. ✅ Добавляет проект issue в GitHub Project
3. ✅ Создает Draft Issue "Project Details - Full Specification"
4. ✅ Создает кастомные поля:
   - **Application Status** (Pending Review, Under Review, Approved, Rejected, Assigned)
   - **Expert Type** (Backend Specialist, Frontend Specialist, Full-Stack Engineer, DevOps Engineer, Product Lead, UI/UX Designer, AI Engineer, QA Engineer, Data Engineer, Security Specialist)
   - **Expert Level** (Junior, Mid, Senior, Lead)
5. ✅ Добавляет создателя проекта как ADMIN collaborator
6. ✅ Автоматически добавляет заявки экспертов в GitHub Project при их создании

### Работа с представлениями (Views)

**Table View (рекомендуется):**
- ✅ Готов к использованию сразу после создания проекта
- ✅ Все поля видны в одной таблице
- ✅ Фильтры и сортировка доступны

**Board View (Kanban):**
- ✅ Базовая Board view создается автоматически
- ⚠️ Колонки нужно настроить вручную (~30 секунд):
  1. Откройте проект в GitHub
  2. Перейдите в Board view
  3. Нажмите "Configure view"
  4. Установите "Column by: Application Status"
  5. Колонки создадутся автоматически

### Ограничение GitHub API: Темплейты

⚠️ **Важно:** GitHub Projects V2 GraphQL API не поддерживает применение темплейтов при программном создании проекта.

**Причина:** 
- В веб-интерфейсе GitHub можно выбрать темплейт при создании проекта
- Но мутация `createProjectV2` принимает только `ownerId` и `title`
- Параметров `templateId`, `cloneFromProjectId` и т.д. нет

**Решение:**
- API автоматически создает все необходимые поля и структуру
- Если нужен Board view с колонками - настройте вручную (~30 секунд)
- Или используйте Table view (работает сразу)

**Подробнее:** См. [GitHub Projects Limitations](github-projects-limitations.md)

**Документация GitHub:**
- [createProjectV2 mutation](https://docs.github.com/en/graphql/reference/mutations#createprojectv2)
- [Managing project templates](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-project-templates)

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

Ответ включает информацию о созданном GitHub Project:
```json
{
  "success": true,
  "issue": {
    "number": 1,
    "title": "Project Proposal: My Amazing App",
    "html_url": "https://github.com/exply-dev/exply-dev-public-projects/issues/1"
  },
  "project": {
    "id": "PVT_kwDOQNbrIs7...",
    "number": 1,
    "title": "Project #1: My Amazing App",
    "url": "https://github.com/orgs/exply-dev/projects/1"
  }
}
```

### Создание заявки эксперта

```bash
POST /create_expert_application
{
  "projectIssueNumber": 1,
  "body": "👋 **Expert Candidate Application**\n\nI'm interested in joining..."
}
```

Заявка автоматически:
- Создается как отдельное issue
- Добавляется в GitHub Project
- Получает статус "Pending Review" в поле Application Status

### Управление заявками (для создателя проекта)

```bash
# Список заявок
POST /list_project_applications
{
  "projectIssueNumber": 1
}

# Обновить статус
POST /update_application_status
{
  "applicationIssueNumber": 15,
  "status": "Approved"
}

# Обновить поля
POST /update_application_fields
{
  "applicationIssueNumber": 15,
  "expertType": "Full-Stack Engineer",
  "expertLevel": "Senior"
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

API поддерживает опциональную GitHub OAuth 2.0 аутентификацию.

**Для создания ресурсов:**
- ✅ OAuth не обязателен (можно создавать анонимно)
- ✅ Но рекомендуется для сохранения авторства

**Для обновления ресурсов:**
- ⚠️ **Требуется** OAuth токен
- ⚠️ Только создатель ресурса может его обновлять

**Для управления заявками:**
- ⚠️ **Требуется** OAuth токен
- Создатель проекта может управлять заявками экспертов
- Эксперт может управлять своими заявками

### Настройка OAuth в GPT Actions

См. подробную инструкцию: [OAuth 2.0 Setup Guide](oauth-setup.md)

**Scopes (разрешения):**
- `public_repo` - доступ к публичным репозиториям
- `read:user` - чтение профиля пользователя
- `read:org` - чтение информации об организации (для GitHub Projects)

## 📊 Endpoints

**Основные:**
- `GET /` - Health check

**Проекты:**
- `POST /create_project_issue` - Создать проект (автоматически создает GitHub Project)
- `POST /update_project_issue` - Обновить проект
- `POST /get_project_issue` - Получить проект
- `POST /list_project_issues` - Список проектов
- `POST /my_projects` - Мои проекты (требует OAuth)

**Заявки экспертов:**
- `POST /create_expert_application` - Создать заявку
- `POST /list_project_applications` - Список заявок для проекта (для создателя)
- `POST /update_application_status` - Обновить статус заявки (для создателя)
- `POST /update_application_fields` - Обновить поля заявки (для создателя)
- `POST /list_my_applications` - Список моих заявок (для эксперта)
- `POST /withdraw_application` - Отозвать заявку (для эксперта)
- `POST /update_my_application` - Обновить мою заявку (для эксперта)

**Лейблы:**
- `GET /get_labels` - Список лейблов
- `POST /create_label` - Создать лейбл

**Эксперты:**
- `POST /create_expert_profile` - Создать/обновить профиль
- `POST /get_expert_profile` - Получить профиль
- `GET /list_experts` - Список экспертов

**Комментарии:**
- `POST /add_issue_comment` - Добавить комментарий

**Legacy MCP (для обратной совместимости):**
- `GET /tools/list` - Список доступных инструментов
- `POST /tools/call` - Вызов инструмента MCP

## 🧪 Тестирование

```bash
# Health check
curl https://exply-github-proxy-kwftltj4yq-uc.a.run.app/

# Создать issue (с автоматическим созданием GitHub Project)
curl -X POST https://exply-github-proxy-kwftltj4yq-uc.a.run.app/create_project_issue \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Project",
    "body": "Test description"
  }'
```

## 🔗 Связанные ресурсы

- [Project Proposals Repository](https://github.com/exply-dev/exply-dev-public-projects)
- [Experts Profiles Repository](https://github.com/exply-dev/exply-dev-public-experts)
- [OpenAPI Specification (JSON)](../api/exply-project-proposals-api.json)
- [OAuth Setup Guide](oauth-setup.md)
- [Authentication Guide](authentication.md)
- [GitHub Projects Limitations](github-projects-limitations.md)
- [Main README](../README.md)

## 💡 Архитектурное решение

**Почему один API для всех операций?**

✅ **Простота поддержки** - один сервис, одна конфигурация  
✅ **Логическая связность** - все операции связаны с exply.dev платформой  
✅ **Меньше дублирования** - общий код аутентификации и обработки ошибок  
✅ **Единая точка мониторинга** - проще отслеживать использование  

Если в будущем понадобится разделение по производительности или масштабированию, можно будет создать отдельные сервисы, но сейчас один API оптимальнее.
