# Census

By Jacob and Dan

## venv

```bash
python3 -m venv env
source env/bin/activate
```

## 2011

### Data
1. Collect the [catalogue](https://www.ons.gov.uk/census/2011census/2011censusdata/2011censusdatacatalogue) on all the tables
2. Under 'All Tables', Filter to England and Wales, Quick Statistics, Output Area + District + Middle Output Area
    - England and Wales is visible in 2022. Quick Statistics are the main census findings. We also want to ensure data will be avaliable on all zoom levels.
3. Remove duplicates (use Excel or Sheets)
4. Write to tables.txt under data/2011

### Maps

Simplification in Mapshaper

- [Local Authorities](https://geoportal.statistics.gov.uk/datasets/ons::local-authority-districts-december-2011-boundaries-ew-bfc/)
- [Output Areas](https://geoportal.statistics.gov.uk/datasets/ons::output-areas-december-2011-boundaries-ew-bfc/)
- [Middle Output Area](https://geoportal.statistics.gov.uk/maps/middle-layer-super-output-areas-december-2001-boundaries-ew-bfc)