from collections import defaultdict
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime


def main():
    """Usage: posts-by-user.py filename.json keyword

Assumes filename.json is a JSON GroupMe transcript.
    """

    if len(sys.argv) < 3:
        print(main.__doc__)
        sys.exit(1)

    transcriptFile = open(sys.argv[1])
    keyword = sys.argv[2]
    transcript = json.load(transcriptFile)
    transcriptFile.close()

    names = {}
    counts = defaultdict(lambda: {'messages': 0, 'likes_given': 0, 'likes_received': 0})
    totalLikes = 0
    totalMessagesWithKeyword = 0

    for message in transcript:
        text = message[u'text']
        if text is None or keyword.lower() not in text.lower():
            continue
        totalMessagesWithKeyword += 1
        name = message[u'name']
        id = message[u'user_id']
        names[id] = name
        counts[id]['messages'] += 1
        counts[id]['likes_received'] += len(message['favorited_by'])
        for user_id in message['favorited_by']:
            counts[user_id]['likes_given'] += 1
            totalLikes += 1

    print('total message count: ' + str(totalMessagesWithKeyword))

    output = {
        'messages': [],
        'likes_given': [],
        'likes_received': [],

    }
    for id, stats in counts.items():
        name = names[id]
        count = stats['messages']
        like_given_count = stats['likes_given']
        like_received_count = stats['likes_received']
        output['messages'].append(u'{name}: messages: {count} ({msg_pct:.1f}%)'.format(
            name=name, count=count, msg_pct=count/float(totalMessagesWithKeyword) * 100,
        ))
        output['likes_received'].append(u'{name}: likes received: {like_count} ({like_pct:.1f} per message)'.format(
            name=name, like_count=like_received_count, like_pct=like_received_count/float(count),
        ))
        output['likes_given'].append(u'{name}: likes given: {like_count} ({like_pct:.1f}%)'.format(
            name=name, like_count=like_given_count, like_pct=like_given_count/float(totalLikes) * 100
        ))
    for category, values in output.items():
        print '\n'
        print category
        print '--------'
        print '\n'.join(values)

if __name__ == '__main__':
    main()
    sys.exit(0)
