# TRF
A parser and dumper for the fide approved tournament report format: trf
The trf file format is used by the [Fide](https://en.wikipedia.org/wiki/FIDE) to report tournament results and calculate elo ratings based on them.

- Specification: <https://www.fide.com/FIDE/handbook/C04Annex2_TRF16.pdf>
- Example: <http://ratings.fide.com/download/example1.txt>

This project is a *working* reimplementation of <https://github.com/erral/fidetournament> for python3.8 and aims to be the goto trf parser on pypi.

## Simple usage exmaple

```python
import trf

with open('example1.trf') as f:
    tour = trf.load(f)

print(tour.name)
for player in tour.players:
    print(player.name, '-', player.points)
```
