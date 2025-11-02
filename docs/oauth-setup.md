# Настройка OAuth 2.0 для GPT Actions

Это руководство поможет настроить GitHub OAuth 2.0 для вашего GPT, чтобы пользователи не должны были пере-авторизовываться в каждом новом чате.

## Преимущества OAuth 2.0

✅ **Персистентная авторизация** - токены сохраняются как "Connected accounts" и переиспользуются во всех чатах  
✅ **Безопасность** - токены с ограниченным временем жизни и scope'ами  
✅ **Удобство UX** - пользователь авторизуется один раз, работает везде  
✅ **Автоматическое обновление** - refresh tokens обновляются автоматически  

## Шаг 1: Создание GitHub OAuth App

1. Перейдите: https://github.com/settings/developers
2. Нажмите **"New OAuth App"**
3. Заполните форму:
   - **Application name:** `Exply.dev GPT Actions`
   - **Homepage URL:** `https://exply.dev` (или ваш основной сайт)
   - **Authorization callback URL:** `https://chatgpt.com/a/oauth/callback`
     - ⚠️ **Важно:** Это стандартный callback URL от OpenAI для всех GPT Actions
   - **Application description:** `OAuth for Exply.dev GPT Actions - manages project proposals and expert profiles`
4. Нажмите **"Register application"**
5. **Сохраните:**
   - **Client ID** (показывается сразу)
   - **Client Secret** (нажмите "Generate a new client secret" и сохраните)

## Шаг 2: Настройка в GPT Actions

1. Откройте ваш GPT в редакторе: https://platform.openai.com/gpts
2. Перейдите в раздел **Actions**
3. Загрузите OpenAPI схему: 
   ```
   https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-project-proposals-api.json
   ```
4. В разделе **"Аутентификация"**:
   - Выберите **"OAuth"** (не API Key, не "Nothing")
   - Заполните поля:
     - **Authorization URL:** `https://github.com/login/oauth/authorize`
     - **Token URL:** `https://github.com/login/oauth/access_token`
     - **Client ID:** [ваш Client ID из шага 1]
     - **Client Secret:** [ваш Client Secret из шага 1]
     - **Scope:** `public_repo read:user` (или просто оставьте пустым, схема уже содержит scopes)
5. Сохраните изменения

## Шаг 3: Проверка работы

1. Откройте новый чат с вашим GPT
2. Попробуйте создать проект (GPT вызовет Action)
3. Вы увидите диалог авторизации GitHub:
   - Нажмите "Authorize"
   - GitHub попросит подтвердить доступ
   - После подтверждения токен сохранится
4. **Откройте новый чат** с тем же GPT
5. Попробуйте снова создать проект
6. ✅ **Должно работать без повторной авторизации!**

## Проверка Connected Accounts

Пользователь может проверить подключенные аккаунты:

1. В ChatGPT: **GPT → Privacy → Connected accounts**
2. Там будет список подключенных OAuth аккаунтов для каждого GPT
3. Можно **отключить** через "Log out"

## Обработка истечения токенов

Если токен истекает:
- GPT автоматически попросит пользователя пере-авторизоваться
- Это происходит при ответе `401` от API
- Refresh tokens обрабатываются автоматически (если поддерживается провайдером)

## Важные замечания

### Домены должны совпадать
- Authorization URL, Token URL и API URL должны быть из одного корневого домена
- Для GitHub это `github.com` и `api.github.com` - это нормально
- Если используете свой домен для API - убедитесь, что все URL на одном домене

### PKCE (для безопасности)
GitHub OAuth Apps поддерживают PKCE автоматически. GPT Actions использует PKCE по умолчанию, так что дополнительная настройка не требуется.

### Scopes
Текущие scopes в схеме:
- `public_repo` - для создания/обновления issues в публичных репозиториях
- `read:user` - для чтения информации о пользователе (проверка ownership)

Эти scopes минимально необходимые. Не запрашивайте больше прав, чем нужно.

## Troubleshooting

**Ошибка: "Invalid redirect URI"**
- Проверьте, что callback URL точно: `https://chatgpt.com/a/oauth/callback`
- Должен быть без слэша в конце

**Ошибка: "Client ID/Secret mismatch"**
- Проверьте, что скопировали Client ID и Secret без пробелов
- Убедитесь, что используете правильный Client Secret (если генерировали новый - старый не работает)

**Пользователь должен авторизоваться в каждом чате**
- Проверьте, что выбрали именно **OAuth** (не API Key)
- Убедитесь, что токены сохраняются (проверьте Connected accounts)
- Попробуйте разлогинить и залогинить заново

**API отвечает 401**
- Проверьте, что токен передается в заголовке `Authorization: Bearer <token>`
- Убедитесь, что scope включает необходимые права

## Миграция с API Key или без авторизации

Если у вас уже настроен GPT без OAuth:

1. Обновите OpenAPI схему (она уже содержит OAuth)
2. Переключите Authentication на **OAuth**
3. Добавьте Client ID/Secret
4. Сохраните
5. Пользователи будут авторизоваться при первом использовании

Старые чаты с токенами продолжат работать до истечения токенов.

