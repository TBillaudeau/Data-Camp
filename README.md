# M1 DataCamp - Data Engineering 

This project is a part of the DataCamp Data Engineering course. The project is to create a data pipeline that will extract data from web scraping or API.

It will allow users to search for a specific company and see how people are talking about it on Twitter :
* Number of positive/negatives tweets
* Most used keywords
* People thoughts about the company

# Installation

1. To install, you first need to clone or download the project.

```bash
git clone https://github.com/TBillaudeau/Data-Camp
```

2. Install dependencies

```cmd
pip install -r requirements.txt
```

3. Run the website

```python
streamlit run main.py
```

# Technologies used

This app is runned using [Streamlit](https://streamlit.io/), a Python library that allows to create web apps easily.

It uses libraries that are all available in the requirements.txt file or more easily, on [Anaconda](https://www.anaconda.com/).

# Authors
This project have been designed and developped by :
- [`Louis Arbey`](https://github.com/LuiAr)
- [`Thomas Billaudeau`](https://github.com/TBillaudeau)
- [`Pierre-Louis Cretinon`]()

# Credits
This project could not have been possible without the Twitter API and Azure Cosmos DB.
* [Twitter API](https://developer.twitter.com/en/docs)
* [Azure Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/introduction)

---
### LICENSE
[MIT](https://choosealicense.com/licenses/mit/)