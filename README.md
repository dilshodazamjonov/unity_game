# GameTorrentHub

GameTorrentHub is a web application that allows users to discover, download game torrents, and watch trailers before downloading. Built with Django (backend), React.js (frontend), and PostgreSQL (database), this project provides a seamless gaming experience.

## Features

🕹️ Browse and search for game torrents

🎬 Watch official game trailers before downloading

📥 Download torrents with magnet links

🔍 Filter and sort games by genre, rating, and release date

🗣️ User reviews and ratings for games

🔒 Secure authentication (JWT-based)


Tech Stack

# Backend:

Django & Django Rest Framework (DRF)

PostgreSQL (Database)

PyTorrent (Torrent management)

JWT Authentication

# Installation & Setup

Prerequisites

Python 3.9+

PostgreSQL

Backend Setup
> git clone https://github.com/yourusername/GameTorrentHub.git
> cd GameTorrentHub/backend
> python -m venv venv
> source venv/bin/activate  # On Windows: venv\Scripts\activate
> pip install -r requirements.txt
> python manage.py migrate
> python manage.py runserver



# API Endpoints
GET
> /api/games/
GET

> /api/games/{id}/

Get game details

GET

> /api/games/{id}/trailer/

Fetch game trailer

POST

> /api/auth/register/

User registration

POST

> /api/auth/login/

User login

# Contributing

Contributions are welcome! Please follow these steps:

Fork the repository

> Create a feature branch (git checkout -b feature-name)

> Commit your changes (git commit -m 'Add feature')

> Push to your branch (git push origin feature-name)

> Open a Pull Request

License

This project is licensed under the MIT License - see the LICENSE file for details.

Contact

📧 Email: dilshod1526@gmail.com 💼LinkedIn: Dilshod A'zamjonov

Enjoy downloading and exploring new games with GameTorrentHub! 🎮🚀
