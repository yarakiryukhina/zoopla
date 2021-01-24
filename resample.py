import sys
import pandas as pd


try:
    fn_in = sys.argv[1]
except IndexError:
    fn_in = input('Enter input tab delimited file name:')

city = input('Enter city name to apply filtering or leave blank for no filter:').strip().lower()

df = pd.read_csv(fn_in, delimiter='\t').drop_duplicates(subset=['listing_id', 'price_change_dt'])

df.price_change_dt = pd.to_datetime(df.price_change_dt)

filter = (df.price_change_dt >= '2020-01-01')

if city:
    filter &= (df.post_town.str.lower() == city)

df = df[filter]
df = df.set_index(pd.DatetimeIndex(df.price_change_dt))

df_1m = df[['price_change_amount']].resample('1M').mean().fillna(method='ffill')
df_1m['diff'] = (df_1m.price_change_amount - 100) / df_1m.price_change_amount

df_mean_norm = (df_1m - df_1m.mean()) / df_1m.std()
df_min_max_norm = (df_1m - df_1m.min()) / (df_1m.max() - df_1m.min())

df_1m['mean_norm'] = df_mean_norm
df_1m['min_max_norm'] = df_min_max_norm

#df_ma = df_1m.rolling(window=3).mean()

print(df_1m)
