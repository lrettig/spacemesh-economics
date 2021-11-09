import datetime, math

# Smidge per smesh
NUM_DECIMALS = 9
ONE_SMESH = 10**NUM_DECIMALS

# Issuance cap (2.4bn smesh)
TOTAL = int(2.4e9*ONE_SMESH)

# Print every n periods
SAMPLE_INTERVAL = 100000

# Genesis timestamp
GENESIS = datetime.datetime(2022, 1, 1)

# Half-life (in periods)
# ~352 months or ~29 years, times 5 minutes per layer
PERIODS = math.floor(351.868 * 30 * 24 * 12)

# Decay per period
LAMBDA = math.log(2)/PERIODS

print(f'Running from {GENESIS} with lambda {LAMBDA} per period')

curtime = GENESIS
i = 0
last_full = 0

# Bootstrap
tot = tot_j = TOTAL * (1 - math.exp(-LAMBDA))
new_j = math.floor(tot_j)

# Loop until issuance falls below 1 smidge
while True:
    # Copy leading values for this period from last
    tot_i = tot_j
    new_i = new_j

    # Find point of last full smesh issuance
    if last_full == 0 and new_i < ONE_SMESH:
        last_full = curtime

    # End of this period
    curtime += datetime.timedelta(minutes=5)

    # Calculate theoretical total issuance at end of next period
    tot_j = TOTAL * (1 - math.exp(-LAMBDA*(i+2)))

    # Now calculate actual (integer) new issuance for next period
    new_j = math.floor(tot_j - tot)

    # Find point of last smidge issuance
    # If last period issuance is zero, this is the final period
    if new_j < 1 or i % SAMPLE_INTERVAL == 0:
        print(f'Period {i:11,} (end {curtime}): {new_i:18,.0f} smidge new; '
              f'{tot/ONE_SMESH:23,.9f} smesh tot')

    if new_j < 1:
        print('FINAL PERIOD ISSUANCE')
        print(f'tot: {tot:23,.0f}, tot_j: {tot_j:23,.0f}, new_j: {new_j:23,.0f}')
        print(f'Last full smesh issuance: {last_full}')
        break

    # End this period
    tot += new_i
    i += 1
