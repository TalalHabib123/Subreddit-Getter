import pandas as pd
from RedditCredentials import reddit
from tqdm import tqdm
print("Retrieving Sub Reddits")
subreddits = reddit.subreddits.popular(limit=1000)

subreddit_data = []
print("Appending Subreddits")
for subreddit in tqdm(subreddits, desc="Fetching Subreddit Data", unit="subreddit"):
        subreddit_data.append({
            'Subreddit': subreddit.display_name,
            'Total Subscribers': subreddit.subscribers
        })

df = pd.DataFrame(subreddit_data)

try:  
    print("Removing Duplicates")
    existing_df = pd.read_csv('subreddit_data.csv')
    existing_subreddits = set(existing_df['Subreddit'])
    df = df[~df['Subreddit'].isin(existing_subreddits)]
except FileNotFoundError:
    existing_df = None

if not df.empty:
    print("Saving to File")
    df = df.sort_values(by='Total Subscribers', ascending=False)
    df['Total Subscribers'] = df['Total Subscribers'].apply(lambda x: '{:,}'.format(x))

    df.to_csv('subreddit_data.csv', mode='a', index=False, header=not (existing_df is not None))

print("Data has been written to subreddit_data.csv.")