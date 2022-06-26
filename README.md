# Census

By Jacob and Dan

## venv

```bash
python3 -m venv env
source env/bin/activate
```

## 2011

1. Collect the [catalogue](https://www.ons.gov.uk/census/2011census/2011censusdata/2011censusdatacatalogue) on all the tables
2. Under 'All Tables', Filter to England and Wales, Quick Statistics, Output Area + District + Middle Output Area
    - England and Wales is visible in 2022. Quick Statistics are the main census findings. We also want to ensure data will be avaliable on all zoom levels.
3. Remove duplicates (use Excel or Sheets)
4. Write to tables.txt under data/2011
