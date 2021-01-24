import sys, requests, csv, json

from time import sleep

url = 'http://api.zoopla.co.uk/api/v1/property_listings.js'
api_key = ''
min_price = 80

try:
    area, min_price = sys.argv[1].split(':')
except:
    sys.exit('Usage: zoopla.py <region:min_price>')

fn = '{}-{}.csv'.format(area, min_price)

for pg in range(0, 100):
    payload = {
        'area': area,
        'radius': 10,
        'include_sold': 0,
        'include_rented': 1,
        'listing_status': 'rent',
        'order_by': 'price',
        'ordering': 'ascending',
        'property_type': 'flats',
        'minimum_price': min_price,
        'page_size': 100,
        'page': pg + 1,
        'api_key': api_key
    }

    print('Payload:', payload)

    with requests.get(url, params=payload) as req:
        if req.status_code == 200:
            f = open(fn, 'a', newline='', encoding='utf-8')

            csvwriter = csv.writer(f, delimiter='\t', quotechar = '"', quoting=csv.QUOTE_MINIMAL)

            res = req.json()

            for r in res['listing']:
                row = [
                        r['listing_id'],
                        r['latitude'],
                        r['longitude'],
                        r['outcode'],
                        r['post_town'],
                        r['county'],
                        r['category'],
                        r['property_type'],
                        r['status'],
                        r['furnished_state'],
                        r['num_floors'],
                        r['num_bedrooms'],
                        r['num_bathrooms'],
                        r['num_recepts'],
                        r['displayable_address'],
                        r['first_published_date'],
                        r['rental_prices']['per_week'],
                        r['rental_prices']['per_month']
                    ]

                try:
                    for p in r['price_change']: csvwriter.writerow(row + list(p.values()))

                except KeyError:
                    print(json.dumps(r, indent=4))

            f.close()

            print('Sleep for 9 sec')

            sleep(9)

        elif req.status_code == 403:
            sys.exit('Rate limit reached')

        else:
            print('Error', req.status_code, 'has occured')
