"""Five questions about a small company, answered from twelve rows of monthly figures.

1. Is it profitable?   2. Does it generate cash?   3. Can it scale?
4. What is it worth?   5. What risk does it carry?

Run: python five_questions.py sample_company.csv
Standard library only. Figures in the sample file are illustrative.
"""
import csv
import sys

# Assumptions for question 4. Change them to fit the company and the market.
MULTIPLE_LOW, MULTIPLE_HIGH = 3.0, 5.0   # EV / EBITDA range for a small private company
MAINTENANCE_CAPEX = 0.03                 # share of sales needed to keep the assets running
DISCOUNT_RATE = 0.20                     # real, for a no-growth capitalisation


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [{k: (v if k == "month" else float(v)) for k, v in r.items()}
                for r in csv.DictReader(l for l in fh if not l.startswith("#"))]
    if len(rows) < 3:
        sys.exit("need at least three months")
    return rows


def money(x):
    return f"{x:>10,.0f}"


def analyse(rows):
    n = len(rows)
    tot = lambda k: sum(r[k] for r in rows)
    sales, cogs, fixed, interest = tot("sales"), tot("cogs"), tot("fixed_costs"), tot("interest")
    ebitda = sales - cogs - fixed
    cm = (sales - cogs) / sales                       # contribution margin
    breakeven = fixed / cm                            # sales needed for EBITDA = 0
    first, last = rows[0], rows[-1]
    nwc = lambda r: r["receivables"] + r["inventory"] - r["payables"]
    d_nwc = nwc(last) - nwc(first)
    cash_flow = ebitda - d_nwc - interest
    dso = last["receivables"] / (sales / n) * 30
    half = n // 2
    growth = sum(r["sales"] for r in rows[half:]) / sum(r["sales"] for r in rows[:half]) - 1
    annual = 12 / n
    ebitda_y = ebitda * annual
    net_debt = last["debt"] - last["cash"]
    ev_low, ev_high = ebitda_y * MULTIPLE_LOW, ebitda_y * MULTIPLE_HIGH
    as_is = (ebitda_y - sales * annual * MAINTENANCE_CAPEX) / DISCOUNT_RATE
    months_of_cash = last["cash"] / (fixed / n)
    safety = 1 - breakeven / sales
    coverage = ebitda / interest if interest else float("inf")

    def light(value, green, amber, higher_is_better=True):
        if not higher_is_better:
            value, green, amber = -value, -green, -amber
        return "GREEN" if value >= green else "AMBER" if value >= amber else "RED  "

    print(f"{n} months · sales {money(sales).strip()} · figures in the currency of the file\n")
    print("1. Is it profitable?")
    print(f"   EBITDA {ebitda:,.0f} ({ebitda / sales:.1%} of sales) · contribution margin {cm:.1%}")
    print(f"   Break-even sales {breakeven:,.0f} for the period: sales are {'above' if sales > breakeven else 'BELOW'} it by {abs(safety):.0%}\n")
    print("2. Does it generate cash?")
    print(f"   EBITDA {ebitda:,.0f} − increase in working capital {d_nwc:,.0f} − interest {interest:,.0f} = {cash_flow:,.0f}")
    print(f"   {cash_flow / ebitda:.0%} of EBITDA turns into cash · customers pay in {dso:.0f} days\n" if ebitda > 0
          else f"   No EBITDA to convert · customers pay in {dso:.0f} days\n")
    print("3. Can it scale?")
    print(f"   Each extra 100 of sales leaves {cm * 100:.0f} before fixed costs and ties up "
          f"{nwc(last) / (sales / n) / 12 * 100:.0f} of working capital")
    print(f"   Sales second half vs first half: {growth:+.0%}\n")
    print("4. What is it worth?")
    print(f"   As a going concern, {MULTIPLE_LOW:.0f}x to {MULTIPLE_HIGH:.0f}x EBITDA: enterprise value {money(ev_low).strip()} to {money(ev_high).strip()}")
    print(f"   Less net debt {money(net_debt).strip()}: equity {money(ev_low - net_debt).strip()} to {money(ev_high - net_debt).strip()}")
    print(f"   As it runs today, no growth, at {DISCOUNT_RATE:.0%}: enterprise value {money(as_is).strip()}\n")
    print("5. What risk does it carry?")
    for name, value, shown, g, a, hib in (
            ("Margin over break-even", safety, f"{safety:.0%}", 0.30, 0.10, True),
            ("Interest cover (EBITDA / interest)", coverage, f"{coverage:.1f}x", 4, 2, True),
            ("Net debt / EBITDA", net_debt / ebitda_y if ebitda_y > 0 else 99, f"{net_debt / ebitda_y:.1f}x" if ebitda_y > 0 else "n/a", 2, 3.5, False),
            ("Months of fixed costs in cash", months_of_cash, f"{months_of_cash:.1f}", 3, 1, True),
            ("Days to collect", dso, f"{dso:.0f}", 45, 90, False),
            ("Largest customer, share of sales", last.get("top_customer_share", 0), f"{last.get('top_customer_share', 0):.0%}", 0.20, 0.35, False)):
        print(f"   {light(value, g, a, hib)}  {name:<36} {shown}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    analyse(load(sys.argv[1]))
