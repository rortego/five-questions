# Five questions

A terminal report that reads twelve rows of monthly figures and answers five questions about a small company, always in the same order.

1. Is it profitable?
2. Does it generate cash?
3. Can it scale?
4. What is it worth?
5. What risk does it carry?

## Why

Most owners of small companies run the business by looking at the bank balance. The five questions are the order I follow with every company I work with: each answer needs the one before it, and the order stops the conversation from jumping to "what is it worth" before knowing whether it makes money. This script is the smallest version of that method: one CSV in, one page out.

## Run it

```
python five_questions.py sample_company.csv
```

```
1. Is it profitable?
   EBITDA 645 (11.5% of sales) · contribution margin 33.2%
   Break-even sales 3,676 for the period: sales are above it by 35%

2. Does it generate cash?
   EBITDA 645 − increase in working capital 584 − interest 114 = -53
   -8% of EBITDA turns into cash · customers pay in 72 days

5. What risk does it carry?
   GREEN  Margin over break-even               35%
   GREEN  Interest cover (EBITDA / interest)   5.7x
   GREEN  Net debt / EBITDA                    0.9x
   RED    Months of fixed costs in cash        0.3
   AMBER  Days to collect                      72
   RED    Largest customer, share of sales     38%
```

The sample company is profitable and growing 17% half on half, and it is running out of cash: the whole EBITDA went into receivables, which now take 72 days to collect. That is the kind of thing the bank balance shows too late.

## Input

A CSV with one row per month: `sales`, `cogs`, `fixed_costs`, `interest`, and month-end balances for `receivables`, `inventory`, `payables`, `cash` and `debt`. `top_customer_share` is optional.

## How question 4 is answered

Two rough figures, on purpose: a range of EBITDA multiples for a small private company, and the value of the company as it runs today with no growth. The multiples, the maintenance capex and the discount rate are constants at the top of the file. A real valuation needs a projection and a discount rate built for the company; this gives the order of magnitude and shows how much of it debt takes away.

Standard library only. The figures in the sample file are illustrative.
