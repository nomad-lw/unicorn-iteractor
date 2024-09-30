# Unicorn Interactor

## Overview
Unicorn Interactor is a Python-based module with a CLI interface that enables interactionwith the Unicorn blockchain.
It currently supports the following functions:
- Transferring tokens (command: `transfer <target_addr> <amount> [memo]`)
- Querying the balance of an account (command: `balance <address>`)

## Installation
To install Unicorn Interactor, make sure you have Poetry installed, then run:

```
poetry install
```

You also need to create a `.env` file in the root directory of the project with the following content:
```
MNEMONIC=<your mnemonic>
```

## Usage
To use Unicorn Interactor, run the following command:

```
poetry run python ./unicorn_interactor [command] [arguments]
```

Available commands:
- `transfer`: Transfer tokens from one account to another
- `balance`: Query the balance of an account

Example:
```
poetry run python ./unicorn_interactor transfer unicorn1r8w2apxfl6hz5akzjn0lp4zg7z2a78a0qnzk4q 100000
```

## Dependencies
- cosmpy

## Development
To set up the development environment:

1. Clone the repository
2. Run `poetry install`
3. Activate the virtual environment with `poetry shell`

## Contributing
Although this project is just a simple POC and I do not intend to maintain/develop this further, contributions are welcome! Please feel free to submit a Pull Request.
No guarantees are made about the quality of the code.

## License
This project is licensed under the GPL License.
