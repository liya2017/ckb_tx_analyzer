# ckb_tx_analyzer

## Pre-required
1. sudo pip3 install configparser

2. install Psycopg2 and sqlalchemy

   > sudo apt-get install libpq-dev

   > sudo apt-get install python3-pip

   > sudo pip3 install Psycopg2

   > sudo pip3 install sqlalchemy

## start service
  > sudo cp ckb-tx-monitor.service /etc/systemd/system

  > sudo systemctl start ckb-tx-monitor.service 

  > sudo systemctl enable ckb-tx-monitor.service 
## check service
> sudo systemctl status ckb-tx-monitor.service 
