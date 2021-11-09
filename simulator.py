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

## LOGIC

print(f'Running from {GENESIS} with lambda {LAMBDA} per period')

curtime = GENESIS
i = 0
last_full = 0

# Bootstrap
tot = 0
tot_j = TOTAL * (1 - math.exp(-LAMBDA))
new_j = math.floor(tot_j)

# Loop until issuance falls below 1 smidge
while True:
    # Copy leading values for this period from last
    tot_i = tot_j
    new_i = new_j

    # Calculate total issuance as of the end of this period
    old_tot = tot
    tot += new_i

    # Find point of last full smesh issuance
    if last_full == 0 and new_i < ONE_SMESH:
        last_full = curtime

    # Calculate end timestamp for this period
    curtime += LAYER_TIME

    # Calculate theoretical total issuance at end of _next_ period
    tot_j = TOTAL * (1 - math.exp(-LAMBDA*(i+2)))

    # Now calculate actual (integer) new issuance for _next_ period
    new_j = math.floor(tot_j - tot)

    # Find point of last smidge issuance
    # If next period issuance is zero, this is the final period
    if new_j < 1:
        print('FINAL PERIOD ISSUANCE')

    if new_j < 1 or i % SAMPLE_INTERVAL == 0:
        print(f'Period {i:11,} (end {curtime}): {new_i:16,.0f} smidge new; {tot:25,.0f} smidge tot')

    if new_j < 1:
        #print(f'tot: {tot:23,.0f}, old_tot: {old_tot:23,.0f}, tot_j: {tot_j:23,.0f}, new_j: {new_j}')
        print(f'Last full smesh issuance: {last_full}')
        break

    # End this period
    i += 1
