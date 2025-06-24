# LLM Chess Player ♟️

# Introduction

This project is a simple chess game where you can play against a language model (LLM). The game is designed to be played in a terminal, and uses the `MCP Chess` project to handle the chess logic and board state. The LLM will make moves based on the current state of the board and the rules of chess.

![Chess Game](docs/Chess.gif)

> [!NOTE]
> By default, the model used is `qwen3:0.6B`, but you can change it to any other model qvailable in Ollama. This model is a `thinking model`, meaning it will think before making a move, which can take some time. If you want a faster response, you can use a classic model like `llama3:8B`.

# Usage

To use this project, you will first need to install the required dependencies. You can do this by running:

```bash
pip install -r requirements.txt
```

Then, you must start the MCP server. By following the instructions in the `MCP Chess` project. You can found it [here](https://github.com/nathan-hoche/MCP_Chess)

Then, you can run the LLM chess player using:

```bash
python src/main.py
```