# musicdb.py
# Author: Jakub Svoboda <jakub.svoboda@gmx.ch>
# Copyright: CC0 or Beerware or WTFPL

# import the flask app
from musicdb import app

# start the flask app listening on all available IPs
if __name__ == '__main__':
  app.run(host='0.0.0.0')
