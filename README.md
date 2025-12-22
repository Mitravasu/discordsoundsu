<a href="https://github.com/Mitravasu/discordsoundsu">
    <img src="logos/SOUNDSU.png" alt="Discord Sounds U logo" title="Discord Sounds U" align="right" height="60" />
</a>

# Discord Sounds U

A feature-rich Discord bot for playing and managing custom sounds in your voice
channels.

## 🎵 Features

-   **Sound Playback** - Play custom sounds in voice channels with simple
    commands
-   **Sound Management** - Upload and organize your own sound files
-   **Sleep Timers** - Automatically disconnect after a specified duration
-   **Easy Setup** - Quick installation and configuration

## 📋 Prerequisites

-   Python 3.8 or higher
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

> **Note for Windows users:** 
> - In PowerShell, use `${PWD}` instead of `$(pwd)`
> - In Git Bash, prefix with `MSYS_NO_PATHCONV=1`

## 📁 Project Structure

```
discordsoundsu/
├── src/discordsoundsu/    # Main bot source code
│   ├── commands/          # Command modules
│   └── ...
├── mp3/                   # Sound files directory
└── pyproject.toml         # Project configuration
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the
issues page.

## 📬 Contact

[![@Mitravasu](https://img.shields.io/badge/GitHub-Mitravasu-green?logo=github&style=flat)](https://github.com/Mitravasu)

[![Website](https://img.shields.io/badge/Website-mitravasu.com-orange?logo=googlechrome&logoColor=white&style=flat)](https://mitravasu.com)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for
details.
