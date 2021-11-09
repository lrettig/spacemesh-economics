import datetime, math

# Issuance cap
# 2.4 bn + 18 decimal places, i.e., 2.4e27
TOTAL = 2_400_000_000_000_000_000_000_000_000

# Decimal places to remove when printing (i.e., print thousands)
FMT_DECIMALS = 21

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
for i in range(PERIODS):
    curtime += datetime.timedelta(minutes=5)
    # Calculate total issuance this period
    tot_i = TOTAL * (1 - math.exp(-LAMBDA*(i+1)))
    new = tot_i - tot
    tot = tot_i

    print(f'Period {i:10} (end {curtime}): {new/10**FMT_DECIMALS:10.3f} new '
          f'{tot/10**FMT_DECIMALS:10.3f} tot')
