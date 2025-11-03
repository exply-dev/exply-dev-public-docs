# GitHub Projects API Limitations

## Темплейты не поддерживаются в API

### Проблема

В веб-интерфейсе GitHub можно выбрать темплейт при создании проекта, но **GitHub Projects V2 GraphQL API не поддерживает применение темплейтов** при программном создании проекта.

### Что доступно в API

Мутация `createProjectV2` принимает только:
- `ownerId` (ID организации или пользователя)
- `title` (название проекта)

```graphql
mutation($ownerId: ID!, $title: String!) {
  createProjectV2(input: {
    ownerId: $ownerId
    title: $title
  }) {
    projectV2 {
      id
      number
      title
      url
    }
  }
}
```

**Нет параметров:**
- ❌ `templateId` или `templateNodeId`
- ❌ `cloneFromProjectId`
- ❌ `copyFromProjectId`

### Почему это так?

GitHub разделяет веб-интерфейс и API:
- **Веб-интерфейс:** Может применять темплейты (это внутренняя логика GitHub UI)
- **API:** Не предоставляет доступ к этой функциональности

Это распространенная ситуация - многие платформы имеют больше функций в UI, чем в API.

### Что делает наш API

Exply.dev Platform API автоматически создает все необходимое:

1. ✅ Создает GitHub Project через API
2. ✅ Программно создает все поля:
   - Application Status (Pending Review, Under Review, Approved, Rejected, Assigned)
   - Expert Type (Backend Specialist, Frontend Specialist, Full-Stack Engineer, и т.д.)
   - Expert Level (Junior, Mid, Senior, Lead)
3. ✅ Создает Draft Issue "Project Details - Full Specification"
4. ✅ Добавляет создателя проекта как ADMIN collaborator
5. ✅ Автоматически добавляет заявки экспертов в GitHub Project

**Результат:** Проект полностью готов к работе, все поля созданы, структура настроена.

### Работа с Views

**Table View:**
- ✅ Готов к использованию сразу
- ✅ Все поля видны в одной таблице
- ✅ Фильтры и сортировка доступны

**Board View (Kanban):**
- ✅ Базовая Board view создается автоматически
- ⚠️ Колонки нужно настроить вручную (~30 секунд):
  1. Откройте проект в GitHub
  2. Перейдите в Board view
  3. Нажмите "Configure view" или "Edit"
  4. Установите "Column by: Application Status"
  5. Колонки создадутся автоматически

**Примечание:** GitHub Projects V2 API не позволяет программно создавать колонки - это ограничение GitHub API, а не нашего кода.

### Альтернативные решения

#### Вариант 1: Использовать Table View (рекомендуется)
- Готово сразу, ничего настраивать не нужно
- Все данные видны в одной таблице
- Фильтры по всем полям
- Сортировка по любому полю

#### Вариант 2: Настроить Board View вручную
- Время: ~30 секунд на проект
- Установить "Column by: Application Status"
- Колонки создадутся автоматически

#### Вариант 3: Использовать темплейт как справочник
- Создайте темплейт один раз с настроенным View
- Используйте его как справочник для ручной настройки новых проектов

### Документация GitHub

Официальная документация GitHub Projects V2 API:
- [createProjectV2 mutation](https://docs.github.com/en/graphql/reference/mutations#createprojectv2)
- [Managing project templates](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-project-templates)

**Вывод:** API действительно не поддерживает темплейты. Это ограничение GitHub API, а не нашего кода.

### Рекомендация

**Используйте текущий подход:**
- API создает проект и все поля автоматически
- Пользователь настраивает View вручную (~30 секунд) или использует Table view
- Или используйте Table view (работает сразу без настройки)

**Если GitHub добавит поддержку темплейтов в API:**
- Мы добавим параметр `templateId` в `createProjectV2`
- Обновим код для применения темплейта
- Обновим документацию
