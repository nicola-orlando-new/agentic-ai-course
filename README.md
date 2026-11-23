# Agentic AI Fundamentals
![docs/assets/xebia-logo.png](docs/xebia-logo.png)
Hi! 👋🏻

This repository contains the exercises and material for the **Agentic AI** training.

## Setup

In order to follow the training, please go through the steps below. If you have problems, don't hesitate to ask your trainer.

Some exercises require a `GEMINI_API_KEY`. Your trainer will provide this during the training.

There are three options you may choose from:

1. Using Github Codespaces
2. Locally using a Devcontainer in VSCode (⭐️ Recommended)
3. Locally using your own setup

### 1. Using Github Codespaces

1. Create a Codespace on `main`:

    ![alt text](<docs/create-codespace.png>)

2. Let Codespace perform setup.

    Let the Devcontainer `postCreateCommand` run and wait until all terminal commands are completed.

3. To make sure everything is setup correctly you can run `uv run python -V`, which should return a Python version >= 3.12.

4. In order to use the correct virtual environment, select the `.venv` kernel when prompted in the notebook.

<p align="center">
<img src=docs/python-kernel.png>
</p>

### 2. Locally using a Devcontainer in VSCode

[Devcontainers](https://code.visualstudio.com/docs/devcontainers/containers) are a powerful way to easily get your environment up and running. We already configured a devcontainer for you to use. <small>In fact, GitHub Codespaces uses devcontainers under the hood.</small> Let's spin it up:

1. Install [VSCode](https://code.visualstudio.com/download) and either [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) or simply [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Clone and open this repository in VSCode
3. Now it's time to open in a Devcontainer!

   It might be the case you already got a notification in VSCode, asking you to Open in a Container. Click that button! Then your container opens up and sets up an environment for you.

   Otherwise, in VSCode, hit <kbd>CMD</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and type `Reopen in Container` (you can also click the bottom-left big button in VSCode).

   Your container should now open! 🎉 Wait a bit for your environment to be set up.


### 3. Using your own editor

These are the steps to get started with your own editor (e.g. VSCode):
1. Open a terminal
2. Clone the repository
3. Open this folder (the cloned repo) in your editor
4. Open a terminal in this folder
5. Install [`uv`](https://github.com/astral-sh/uv).
6. With `uv` installed, run:

   ```bash
   uv sync
   ```

## Exercises

If you are all setup, using either Codespaces or your own computer, start with the first exercise!
