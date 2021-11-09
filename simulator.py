import datetime, math

# Genesis timestamp
GENESIS = datetime.datetime(2022, 1, 1)

# Half-life (in periods)
# ~352 months or ~29 years, times 5 minutes per layer
PERIODS = math.floor(351.868 * 30 * 24 * 12)

# Decay per period
LAMBDA = math.log(2)/PERIODS

print(f'Running for {PERIODS} periods from {GENESIS} with lambda {LAMBDA} per period')

curtime = GENESIS
for i in range(PERIODS):
    print(f'Period {i} datetime {curtime}')
    curtime += datetime.timedelta(minutes=5)
