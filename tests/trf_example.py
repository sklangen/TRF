import trf

with open('example1.trf') as f:
    tour = trf.load(f)

print(tour.name)
for player in tour.players:
    print(player.name, '-', player.points)
