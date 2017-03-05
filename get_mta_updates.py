from google.transit import gtfs_realtime_pb2
from google.cloud import datastore
import requests
import time

def query_train_feed(mta_feed_id):
    line_updates = []
    feed = gtfs_realtime_pb2.FeedMessage()
    request_attempts = 0

    while request_attempts < 3:
        try:
            #http://datamine.mta.info/list-of-feeds
            response = requests.get('http://datamine.mta.info/mta_esi.php?key=0b20b10d41a37168a43ce3ca8f0890f2&feed_id={}'
                                    .format(mta_feed_id), data = {'key':'value'})
            if response.status_code != 200:
                raise Exception
            
            feed.ParseFromString(response.content)
        except Exception:
            request_attempts += 1
        else:
            break

    delay = 'On Schedule'
    train_route = ''
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            train_route = entity.trip_update.trip.route_id
            date = entity.trip_update.trip.start_date
            arrival_epoch = entity.trip_update.stop_time_update[0].arrival.time
            depart_epoch = entity.trip_update.stop_time_update[0].departure.time
            arrival = time.strftime('%H:%M', time.gmtime(arrival_epoch)) #Convert Epoch to human readable time.
            depart = time.strftime('%H:%M', time.gmtime(depart_epoch))

        if entity.HasField('alert'):
            delay = entity.alert.header_text.translation[0].text

        line_updates.append({'trainRoute': train_route, 'isDelay': delay,
                              'date': date, 'arrivalTime': arrival, 'departTime': depart})
    # print train_route, delay, date, arrival, depart
    return line_updates

def gather_train_information():
    mta_feed_ids = [1, 2, 16, 21] #http://datamine.mta.info/list-of-feeds
    all_line_updates = []
    for mta_feed in mta_feed_ids:
        all_line_updates.append(query_train_feed(mta_feed))
    return all_line_updates

def submit_to_datastore(all_mta_feeds):
    data_store = datastore.Client('fancy-mta')

    for mta_feed in all_mta_feeds:
        for mta_line in mta_feed:
            train_key = data_store.key('aazz')
            train = datastore.Entity(key=train_key)
            train['date'] = mta_line['date']
            train['isDelay'] =  mta_line['isDelay']
            train['trainRoute'] =  mta_line['trainRoute']
            train['departTime'] =  mta_line['departTime']
            train['arrivalTime'] = mta_line['arrivalTime']    
            data_store.put(train)
    return

def main():
    all_mta_feeds =  gather_train_information()
    submit_to_datastore(all_mta_feeds)

if __name__ == '__main__':
    main()
