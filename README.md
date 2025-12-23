<a href="https://github.com/Mitravasu/discordsoundsu">
    <img src="logos/SOUNDSU.png" alt="Discord Sounds U logo" title="Discord Sounds U" align="right" height="60" />
</a>

# Discord Sounds U

A feature-rich Discord bot for playing and managing custom sounds in your voice
channels.

## 🎵 Features

-   **Sound Playback** - Play custom sounds in voice channels with simple
    commands and auto completion
-   **Sound Management** - Upload and organize your own sound files
-   **Sleep Timers** - Automatically kick all members from the call when its time to sleep 😴
-   **Easy Setup** - Quick installation and configuration

## 📋 Prerequisites

-   Python 3.11 only
-   [uv](https://github.com/astral-sh/uv) package manager
-   A Discord bot token

## 🚀 Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Mitravasu/discordsoundsu.git
    cd discordsoundsu
    ```

2. Install dependencies:

    ```bash
    uv sync
    ```

3. Configure your bot token by adding the `.env` file

## 💻 Usage

Run the bot with:

```bash
uv run discordsoundsu
```

### Using Docker

Build the Docker image:

```bash
docker build -t discordsoundsu .
```

Run the container with volume mount for mp3 files:

```bash
docker run -v $(pwd)/mp3:/app/mp3 discordsoundsu
```

### Clean up UV cache

Run this comand to clear UV cache and do a fresh install

```bash
rm -rf .venv __pycache__ && rm -rf ~/.cache/uv && pip cache purge
```

## Linting
```bash
uv run ruff check
```

```bash
uv run ruff format
```

## Run on startup
1. Add your project directory to `run_discordsoundsu.sh`
1. `chmod +x run_discordsoundsu.sh`
1. `crontab -e`
1. Add the following line and save

    `@reboot /full/path/to/run_discordsoundsu.sh`
1. Reboot and discordsoundsu should run on startup

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the
issues page.

## 📬 Contact

[![@Mitravasu](https://img.shields.io/badge/GitHub-Mitravasu-green?logo=github&style=flat)](https://github.com/Mitravasu)

[![Website](https://img.shields.io/badge/Website-mitravasu.com-orange?logo=googlechrome&logoColor=white&style=flat)](https://mitravasu.com)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for
details.
