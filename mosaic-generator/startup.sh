cd MMGs
(
cd reducer
nohup python3 -m flask run --port=6000 --host=0.0.0.0 &
)
(
cd albums
nohup python3 -m flask run --port=5001 --host=0.0.0.0 &
)
(
cd beverages
nohup python3 -m flask run --port=5002 --host=0.0.0.0 &
)
(
cd candy
nohup python3 -m flask run --port=5003 --host=0.0.0.0 &
)
(
cd cats_dogs
nohup python3 -m flask run --port=5004 --host=0.0.0.0 &
)
(
cd fast_food
nohup python3 -m flask run --port=5005 --host=0.0.0.0 &
)
(
cd fish
nohup python3 -m flask run --port=5006 --host=0.0.0.0 &
)
(
cd flags
nohup python3 -m flask run --port=5007 --host=0.0.0.0 &
)
(
cd flowers
nohup python3 -m flask run --port=5008 --host=0.0.0.0 &
)
(
cd marvel
nohup python3 -m flask run --port=5009 --host=0.0.0.0 &
)
(
cd pokemon 
nohup python3 -m flask run --port=5010 --host=0.0.0.0 &
)
(
cd south_park
nohup python3 -m flask run --port=5011 --host=0.0.0.0 &
)
(
cd sports_logos
nohup python3 -m flask run --port=5012 --host=0.0.0.0 &
)
(
cd star_wars
nohup python3 -m flask run --port=5013 --host=0.0.0.0 &
)
wait