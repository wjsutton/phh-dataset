====================
Poker Hand Histories
====================

A collection of poker hand histories, covering 11 poker variants, in the poker hand history (PHH) format.

Contents:

- All 83 televised hands played in the final table of the 2023 World Series of Poker Event #43: $50,000 Poker Players Championship | Day 5
- All 10000 hands played by Pluribus and published in the supplementary of Brown and Sandholm (2019).
- 4 selections of historical poker hands.
- 1 badugi hand from the Wikipedia page on badugi.

--- 

Virtual Environment with venv

Requires Python 3.11 or higher for `pokerkit` package

Setup 
```
python -m venv venv
```

Activate with
```
venv\Scripts\activate
```

Install Packages
```
pip install -r requirements.txt
```

Run a 

```
python scripts/print_stats.py data/wsop/2023/43/5/00-02-07.phh
```