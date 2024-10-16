## REVIEW SCRAPING SYSTEM

The Review Scraper is a web scraping tool designed to extract reviews from various product pages. This system utilizes a combination of Playwright for browser automation and BeautifulSoup for HTML parsing, making it capable of navigating through complex web pages to retrieve
relevant review data. The scraped reviews are processed using the BLOOM language model to generate insightful summaries, enabling users to quickly understand customer sentiments and product feedback.

#### Features

Dynamic CSS Selector Identification: Utilizes Large Language Models (LLMs) to identify and extract reviews from dynamically loaded pages.<br />
Pagination Handling: Implements logic to navigate through multiple pages of reviews, ensuring comprehensive data extraction.<br />
Universal Compatibility: Designed to work with any product review page, offering flexibility in use across various e-commerce platforms.<br />
LLM Integration: Integrates the BLOOM model for processing reviews, generating concise summaries that enhance the quality of the extracted information.<br />


#### Technologies Used

Django: The web framework used to build the server-side application.<br />
Playwright: A browser automation framework for navigating web pages and simulating user interactions.<br />
BeautifulSoup: A Python library for parsing HTML and extracting data from web pages.<br />
Transformers: A library for integrating and using the BLOOM language model for text generation and summarization.<br />


#### Requirements

~~~
Python 3.8+
Django 4.0+
Django REST Framework
Django Filter
MySQL

~~~

## Installation

1. Clone the repository:

   ~~~
   git clone https://github.com/mansijain980/Movie_Content.git
   cd Movie_Content
   ~~~

2. Create a virtual environment and activate it:

   ~~~
   python3 -m venv env
   source env/bin/activate  On Windows use `env\Scripts\activate`
   ~~~

3. Install the required dependencies:

   ~~~
   pip install -r requirements.txt
   ~~~
