# Варламов Дамир | Backend Developer (Go)

## 👨‍💻 Обо мне

Backend-разработчик из Самары с 6+ годами коммерческого опыта. Специализируюсь на FinTech и высоконагруженных системах: Go, gRPC, Kafka, PostgreSQL, Kubernetes. Работал с платёжным шлюзом на 20 000 RPS, миграцией монолита на микросервисы, Transactional Outbox/Saga и PCI DSS. Высшее образование получаю заочно, совмещаю обучение с работой.

## 🛠 Технологический стек

### Backend
- **Go**, gRPC, Protobuf, REST, net/http, Chi
- Микросервисы, Clean Architecture, SOLID
- Transactional Outbox, Saga, идемпотентность

### Базы данных
- **PostgreSQL** (партиционирование, реплики, оптимизация запросов)
- **Redis**, **ClickHouse**, **Elasticsearch**

### Асинхронность и интеграции
- **Apache Kafka**, **RabbitMQ**
- Retry/backoff, circuit breaker, rate limiting

### Инфраструктура и observability
- **Docker**, **Kubernetes**, Linux, GitLab CI, Git
- **Prometheus**, **Grafana**, **OpenTelemetry**, Jaeger
- SLO/SLA, алертинг, on-call

### Качество
- Unit- и интеграционные тесты (testcontainers, testify)
- pprof, профилирование, код-ревью, golangci-lint

## 💼 Опыт

- **FinTech / платёжный процессинг (NDA)** — 3 микросервиса платёжного ядра на Go и gRPC, 20 000 RPS, Kafka, Outbox/Saga, PCI DSS.
- **E-commerce / маркетплейс** — микросервисы синхронизации остатков и ценообразования, Redis, RabbitMQ, Elasticsearch, PostgreSQL.

## 🏆 Достижения

- 🥇 **WorldSkills Russia** — победитель национального чемпионата «Разработка блокчейн-решений» (2022)
- 🥈 **WorldSkills Russia** — 2 место, региональный этап (2021)
- Благодарность Губернатора Самарской области
- Благодарность Министерства образования Самарской области
- Участник проектной сессии BRICS

## 📁 Кейсы

- [Платёжный шлюз (NDA)](project-fintech.html) — FinTech, 20 000 RPS, Go, Kafka, PCI DSS
- [CarInSight](project-carinsight.html) — backend на Go, SQLite, AI-диагностика кузова
- [ServiceDesk РЖД](project-rzd.html) — внутренняя тикет-система, PHP, PostgreSQL

## 🏗 Структура сайта

- `index.html` — главная страница
- `portfolio.html` — кейсы и достижения
- `resume.html` — резюме
- `project-*.html` — страницы кейсов
- `assets/data/projects.json` — данные проектов
- `tools/project-template.html` — шаблон страницы проекта
- `tools/build-projects.py` — генератор страниц проектов

### Перегенерация страниц проектов

После изменений в `assets/data/projects.json` или добавления новых скриншотов запустите:

```bash
python tools/build-projects.py
```

## 📞 Контакты

- **Telegram**: [@Ghosers](https://t.me/Ghosers)
- **GitHub**: [Xeney](https://github.com/Xeney)
- **Email**: damir.itwar@yandex.ru
- **Резюме**: [resume.html](resume.html)

---

> Открыт к предложениям Middle+/Senior Backend (Go). FinTech · Highload · удалённо / гибрид.
