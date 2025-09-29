# Fortexs

<p align="center">
    <em>🔍 A web scraper for fetching products from <code>www.fortex.ir</code></em>
</p>

**Fortexs** is a simple Python project that scrapes product listings from [`www.fortex.ir`](https://fortex.ir), an Iranian online store specializing in industrial hardware and plumbing components.

> [!WARNING]
> Currently, price information is not fetched due to site structure or access restrictions.

This project was created for educational purposes, and demonstrates a real-world scraping use case.

## Usage

### Setup with Poetry

This project uses [Poetry](https://python-poetry.org/) to manage dependencies and virtual environments.

1. **Install Poetry** (if you don’t have it already):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

or follow the instructions on the [official Poetry site](https://python-poetry.org/docs/#installation).

2. **Clone this repository** (or download the code):

```bash
git clone https://github.com/ashkanfeyzollahi/fortexs.git
cd fortexs
```

3. **Install dependencies and create a virtual environment:**

```bash
poetry install
```

This will create a virtual environment and install the needed packages.

4. **Run the script:**

```bash
poetry run python src/fortexs.py
```

You should see a progress bar and after fetching all products you should see a message `Done!`.
