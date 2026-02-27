# 🎓 Bot-Studeo

> Automação acadêmica para o Studeo (Unicesumar EAD)
> — Prazos, notas, materiais e notificações no piloto automático.

## ✨ Features

- 📡 **Scraper HTTP** — Coleta dados do Studeo via chamadas diretas (httpx), sem Selenium
- 📅 **Atividades pendentes** — Extrai prazos, MAPAs, fóruns e provas
- 📊 **Notas** — Monitora notas com cálculo de média ponderada
- 🔔 **Detecção de mudanças** — Identifica novidades a cada scrape
- 🤖 **Bot Telegram** — Notificações push + comandos `/prazos`, `/notas`, `/status`
- ⏰ **Scheduler** — Scraping automático a cada 6h (configurável)
- 🗄️ **SQLite** — Histórico persistente de todas as coletas

## 🏗 Arquitetura

```
┌─────────────────────────────────────────┐
│              BOT-STUDEO                 │
├─────────────────────────────────────────┤
│  Scraper (httpx) → SQLite → Telegram   │
│       ↑                                │
│   Scheduler (APScheduler, 6h)          │
└─────────────────────────────────────────┘
```

## 🚀 Como usar

### 1. Clonar e instalar

```bash
git clone https://github.com/seu-usuario/bot-studeo.git
cd bot-studeo
pip install -e ".[dev]"
```

### 2. Configurar

```bash
cp .env.example .env
# Editar .env com suas credenciais
```

### 3. Rodar

```bash
python -m src.main
```

### Com Docker (opcional)

```bash
docker-compose up -d
```

## 🛠 Stack

| Componente | Tecnologia |
|-----------|-----------|
| Linguagem | Python 3.11+ |
| HTTP Client | httpx |
| Banco de dados | SQLite |
| Scheduler | APScheduler |
| Bot | python-telegram-bot |
| Config | pydantic-settings |
| Testes | pytest |

## 🧪 Testes

```bash
pytest tests/ -v
```

## 📁 Estrutura

```
bot-studeo/
├── src/
│   ├── scraper/        # Comunicação com a API do Studeo
│   ├── storage/        # SQLite: modelos, queries, detecção de mudanças
│   ├── integrations/   # Telegram Bot
│   ├── config.py       # Configuração centralizada (.env)
│   ├── scheduler.py    # Jobs periódicos
│   └── main.py         # Entry point
├── tests/              # Testes com dados mockados
├── docs/               # Documentação das APIs descobertas
└── data/               # Banco SQLite + materiais (gitignored)
```

## 📖 Por que construí isso

Estudante de ADS na Unicesumar EAD. O Studeo não tem alertas decentes — prazos se perdem, notas saem sem aviso, materiais ficam espalhados. Este bot resolve tudo isso: coleta dados automaticamente, detecta novidades e me avisa no Telegram.

Projeto genuíno, problema real, solução funcional.

## 📄 License

MIT