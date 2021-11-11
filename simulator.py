import datetime, math

## PARAMETERS

# Smidge per smesh
NUM_DECIMALS = 9
ONE_SMESH = 10**NUM_DECIMALS

# Issuance cap (2.4bn smesh)
TOTAL = int(2.4e9*ONE_SMESH)

# Print every n periods
SAMPLE_INTERVAL = 100000

# Genesis timestamp
GENESIS = datetime.datetime(2022, 1, 1)

# Length of a layer
LAYER_TIME = datetime.timedelta(minutes=5)

# Half-life arithmetic
# ~352 months or ~29.3 years, times 5 minutes per layer
ONE_YEAR = datetime.timedelta(days=365.2425)
HALF_LIFE = ONE_YEAR*29.32233
HALF_LIFE_PERIODS = HALF_LIFE / LAYER_TIME

# Decay per period
LAMBDA = math.log(2)/HALF_LIFE_PERIODS

# Vault vesting
VEST_TOTAL = int(120e6*ONE_SMESH)
TOTAL_REWARDS = TOTAL-VEST_TOTAL
VEST_START = ONE_YEAR
VEST_END = 4 * ONE_YEAR
VEST_START_PERIOD = math.floor(VEST_START/LAYER_TIME)
VEST_END_PERIOD = math.floor(VEST_END/LAYER_TIME)
VEST_PERIODS = VEST_END_PERIOD - VEST_START_PERIOD
VEST_PER_PERIOD = VEST_TOTAL//VEST_PERIODS

## LOGIC

print(f'Running from {GENESIS} with lambda {LAMBDA} per period')

curtime = GENESIS
i = 0
last_full = 0

# Bootstrap
tot = vested = 0
tot_j = TOTAL_REWARDS * (1 - math.exp(-LAMBDA))
new_j = math.floor(tot_j)

# Loop until issuance falls below 1 smidge
while True:
    # Copy leading values for this period from last
    tot_i = tot_j
    new_i = new_j

    # Calculate total issuance as of the end of this period
    old_tot = tot
    tot += new_i

    # Add vesting
    vest_i = VEST_PER_PERIOD if i >= VEST_START_PERIOD and i < VEST_END_PERIOD else 0
    vested += vest_i
    tot += vest_i

    # Find point of last full smesh issuance
    if last_full == 0 and new_i < ONE_SMESH:
        last_full = curtime

    # Calculate end timestamp for this period
    curtime += LAYER_TIME

    # Calculate theoretical total issuance at end of _next_ period
    tot_j = vested + TOTAL_REWARDS * (1 - math.exp(-LAMBDA*(i+2)))

    # Now calculate actual (integer) new issuance for _next_ period
    new_j = math.floor(tot_j - tot)

    # Find point of last smidge issuance
    # If next period issuance is zero, this is the final period
    if new_j < 1:
        print('FINAL PERIOD ISSUANCE')

    if new_j < 1 or i % SAMPLE_INTERVAL == 0:
        print(f'Period {i:11,} (end {curtime}): {new_i:16,.0f} new iss; {vest_i:16,.0f} new vest;'
              f' {vested:24,.0f} vested; {tot:26,.0f} smidge tot')

    if new_j < 1:
        print(f'Last full smesh issuance: {last_full}')
        break

    # End this period
    i += 1
