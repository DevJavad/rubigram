# Rubigram Downloader Bot

A powerful Rubika / Rubino downloader bot built using **Rubigram**, allowing users to download posts simply by sending their share link.

This bot also stores users in a database and provides admin tools such as user count.

---

## 🚀 Features

- Download **Rubino posts** by share link  
- Auto-detect Rubino URLs using **Regex**  
- Save each user **only once** (database protected)  
- `/users` admin command with inline buttons  
- Async & fully optimized **Rubigram client**  
- Uses **Tortoise ORM**  
- Compatible with **Python 3.12 – 3.14**  

---

## 📦 Requirements

Make sure you have the following installed:

```
Python 3.12+
Rubigram
Tortoise ORM
SQLite (or your chosen database)
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Before running the bot, edit the following file:

### `config.py`

```python
token = "your_bot_token"
auth = "your_rubino_auth"
admin = "your_chat_id"
database = "sqlite://database.sqlite"
```

---

## ▶️ Running the Bot

Simply run:

```bash
python main.py
```