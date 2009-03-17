import GoogleReader.reader
import sys

USERNAME = "mister.fastfinger"
PASSWORD = "1428vQe"

reader = GoogleReader.reader.GoogleReader()
reader.identify(USERNAME, PASSWORD)
reader.login()

#labels = reader.get_tag_list()['tags']
#print labels

subs = reader.get_subscription_list()

for i in subs['subscriptions']:
    print i['title'], i['id']
    feed = reader.get_feed(feed = i['id'])
    entries = feed.get_entries()
    while True:
        try:
            print entries.next().keys()
        except StopIteration:
            break

        
    