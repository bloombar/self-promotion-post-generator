# Self Promotion Post Generator

Python tool to generate and post fake self-promotional material to LinkedIn. Uses OpenAI's GPT-3 API to generate fake self-promotional material text and images and then posts them to LinkedIn.

## Installation

You must first create an OpenAI account and get an API key. Then, create a `.env` file in the root directory and add your API key to it. See the file named `env.example` for example.

Install dependencies with `pip install -r requirements.txt` or `pipenv install`.
Run `main.py` and the generated images and text will be placed in the `posts` directory.

## Bugs

- Doesn't yet post to LinkedIn automatically... looking into using [Automate-LinkedIn](https://pypi.org/project/Automate-LinkedIn/) for this.
- Currently looks for fonts in the `/System/Library/Fonts/`, which works only on Macs... easy to change for PC.
- Currently picks a random font, and sometimes gets illegible fonts.... need to be more selective
