import datetime, math

# Issuance cap
# 2.4 bn + 18 decimal places, i.e., 2.4e27
TOTAL = 2_400_000_000_000_000_000_000_000_000

# Decimal places to remove when printing
FMT_DECIMALS = 18

# Print every n periods
SAMPLE_INTERVAL = 1000

# Genesis timestamp
GENESIS = datetime.datetime(2022, 1, 1)

# Half-life (in periods)
# ~352 months or ~29 years, times 5 minutes per layer
PERIODS = math.floor(351.868 * 30 * 24 * 12)

# Decay per period
LAMBDA = math.log(2)/PERIODS

print(f'Running for {PERIODS} periods from {GENESIS} with lambda {LAMBDA} per period')
print('Following figures in thousands of Smesh:')

curtime = GENESIS
tot = 0
i = 0
new = 1

# Loop until issuance falls below 1
while new >= 1:
    curtime += datetime.timedelta(minutes=5)

    # Calculate theoretical total issuance this period
    tot_i = TOTAL * (1 - math.exp(-LAMBDA*(i+1)))

    # Now calculate actual (integer) new issuance
    new = math.floor(tot_i - tot)
    tot += new

    if i % SAMPLE_INTERVAL == 0:
        print(f'Period {i:10} (end {curtime}): {new/10**FMT_DECIMALS:8.18f} new '
              f'{tot/10**FMT_DECIMALS:17,.18f} tot')

    i += 1
