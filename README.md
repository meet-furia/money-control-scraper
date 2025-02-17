# Stock Data Scraper (Python)

A Python application that automatically scrapes live stock data from the **MoneyControl** website every 30 minutes. The application fetches real-time stock information, including live price, day's low, and day's high, and stores it in a CSV file for analysis. The project demonstrates web scraping, concurrency, and automation techniques.

## Features
- **Automated Data Fetching**: Scrapes stock data every 30 minutes.
- **Concurrent Data Fetching**: Uses `ThreadPoolExecutor` for efficient concurrent scraping of multiple stock URLs.
- **Real-time Data Extraction**: Extracts live price, day's low, and day's high for each stock.
- **CSV Export**: Saves the scraped data in CSV format for easy analysis.

## Technologies Used
- **Python**: Main programming language.
- **BeautifulSoup**: For parsing and scraping data from the MoneyControl website.
- **ThreadPoolExecutor**: For concurrent scraping to speed up the process.
- **Requests**: For sending HTTP requests and handling responses.
- **PyUserAgent**: Randomizes the user-agent for web requests to avoid blocking.
- **CSV**: To save the fetched stock data into a CSV file.
