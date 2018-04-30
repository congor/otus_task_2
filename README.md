#The three most frequent nouns per week  console analysisapplication

This application’s objective is to find out and output the most three frequent nouns in articles’ titles have been published on the <https://habr.com/>  for each week.

# Main features:

- A site language is Russian.
- A programming language is Python 3.
- For the console usage.
- This application is made as a tutorial exercise.
- Before using an applications the library `pymorphy2` and `numpy` must be installed through `pip install pymorphy2`

# Main stages of an application’s script execution:

- launch the script in the console with proper parameters (see below);
- require and receive html-pages from a website;
- parse html-pages into a proper condition for handling;
- find dates and titles tags and fetch content from them;
- transform dates to datetime-objects for each article;
- prepare title’s texts for searching nouns, transform them into proper form (nominative case), and make a list-object consists of these nouns for each article;
- make a date-nouns list: a publication date – a list of nouns for each article;
- make a list of start day date (Monday) and finish day date (Sunday) for all weeks basing on dates for all received articles through a date-nouns list;
- separate records in a date-nouns list by weeks, join lists of nouns in to common one for each week, make this way a week-nouns list;
- determine the most three nouns for each week;
- show results in an user console;

# Launching parameters

- `-p` or `--page` to set pages quantity (from 1 upto 100) when a script is launching in a console;

```bash
$ pyhon3 showthreenouns.py --pages=20
```