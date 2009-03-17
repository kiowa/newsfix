import GoogleReader.reader
import ho.pisa as pisa
import sys

USERNAME = "mister.fastfinger"
PASSWORD = "1428vQe"
TAG = "tech"

FILENAME = "newspaper.pdf"

reader = GoogleReader.reader.GoogleReader()
reader.identify(USERNAME, PASSWORD)
reader.login()

feed = reader.get_feed(feed = "user/-/label/%s" % TAG)
entries = feed.get_entries()

html = ""
count = 0
while count < 20:
    try:
        sys.stdout.write(".")
        entry = entries.next()
        title = entry["title"]
        summary = entry["summary"]
        content = entry["content"]
        link = entry["link"]
        published = entry["published"]
        author = entry["author"]

        html = html+"<h1>%s</h1>" % title
        html = html+content
        count +=1
        #reader.set_read(entry)

    except StopIteration:
        print "error"
        break

pdf = pisa.CreatePDF(html, file(FILENAME, "wb"))
