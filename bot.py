__author__ = 'Eli'

import praw
import login_details
import time
import atexit

r = praw.Reddit(user_agent="Kelman bot by /u/Eli485 used as an inside joke on the /r/kegkrusherkelman subreddit.")
r.login(username=login_details.usernameKelman, password=login_details.passwordKelman)

call = '!kelman'
# add more commands
# commands = ['worship', 'fast', 'god', 'king', 'certificate']
# commands list is no longer used in preferation of just using logical statements.
comment_cache = []
praiseInt = 0


def read_cache(cache_to_read='cache.commentCache'):
    print("Reading comment cache.")
    file = open(cache_to_read, 'r')
    # appending comment ids to comment_cache.
    for line in file:
        print("Appending comment: " + line.rstrip())
        comment_cache.append(line.rstrip())
        # rstrip() removes the newline return \n.
    file.close()
    print("Read successful, file closed.")


def write_cache(cache_to_write=comment_cache):
    print("Writing current comment ids to cache.")
    file = open('cache.commentCache', 'w')
    # writes each comment id followed by a newline.
    for cache in cache_to_write:
        print("Writing id: " + cache)
        file.write(cache + "\n")
    file.close()
    print("Ids written to cache and file closed.")


def read_praise(praisefile='praises.praiseCount'):
    print("Reading praise count.")
    file = open(praisefile, 'r')
    int_praise = int(file.readline())
    file.close()
    print("Read successful, file closed. Found: " + str(int_praise))
    return int_praise


def write_praise(praisefile='praises.praiseCount'):
    print("Writing praise count.")
    file = open(praisefile, 'w')
    file.write(str(praiseInt))
    file.close()
    print("Successful write, file closed. Wrote: " + str(praiseInt))

atexit.register(write_cache, cache_to_write=comment_cache)
atexit.register(write_praise, praisefile='praises.praiseCount')
# register file to be written on program close.


def append_comment(cmt_id):
    print("Appending to cache.")
    comment_cache.append(str(cmt_id))
    print("Appended comment id to cache.")


def set_praise(int_to_set):
    global praiseInt
    praiseInt = int_to_set


def main():
    print("Getting subreddit kegkrusherkelman.")
    sub_reddit = r.get_subreddit("kegkrusherkelman")
    print("Getting comments.")
    comments = sub_reddit.get_comments(limit=30)
    for cmt in comments:
        text = cmt.body.lower()
        if text.startswith(call) and cmt.id not in comment_cache:
            print("Found comment calling !kelman: " + str(cmt.id))
            split_text = text.split()
            try:
                s = split_text[1]  # second word after !kelman
                if s == 'worship':
                    global praiseInt
                    cmt.reply("I accept your praise loyal follower of Kelman.\nI have been worshipped " + str(praiseInt) + " times.")
                    praiseInt += 1
                    print("Praises raised to: " + str(praiseInt))
                elif s == 'fast':
                    url = 'http://i.imgur.com/0ehC856.jpg'
                    cmt.reply("[gotta go fast](" + url + ")")
                elif s == 'god':
                    # reply should theoretically be quite long.
                    cmt.reply('kelmanisgod' * 10)
                elif s == 'king':
                    url = 'http://i.imgur.com/kCkHvlT.jpg'
                    cmt.reply("[the king](" + url + ")")
                elif s == 'certificate':
                    url = 'http://i.imgur.com/qWGED8x.jpg'
                    cmt.reply("[sik certs bro](" + url + ")")
                else:
                    cmt.reply('You high bro?')
                print("Replied to comment.")
                append_comment(cmt.id)

            except IndexError:
                cmt.reply("What do you want from me?")
                print("Replied to parameter of comment referencing kelman.")
                append_comment(cmt.id)

        elif cmt.id in comment_cache:
            print("Found comment already in cache: " + cmt.id)

        else:
            print("Found comment not containing kelman.")

read_cache()
praiseInt = read_praise()
# Get comment cache and praise int.
while True:
    try:
        main()
        write_cache()
        write_praise()
        sleep = 10
        print("Sleeping for " + sleep + " seconds.")
        time.sleep(sleep)
    except praw.errors.RateLimitExceeded:
        sleep = 60 * 10
        minutes = sleep / 60
        print("Cannot reply: rate limit encountered now sleeping for " + str(sleep) + " seconds. (" + str(minutes) + " minutes)")
        print("Backing up cache and praise count.")
        write_cache()
        write_praise()
        time.sleep(sleep)
