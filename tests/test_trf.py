from unittest import TestCase
import trf
import os
from tests import repeat
import tests.random_tournament as rt

CHINESE_WHISPERS_NUMBER = 100
RANDOM_TEST_NUMBER = 300
RANDOM_PLAYERS_NUMBER = 123


class TestTrt(TestCase):
    maxDiff = None

    def test_load_example1(self):
        filename = os.path.join(os.path.dirname(__file__), 'example1.trf')
        with open(filename) as f:
            tour = trf.load(f)

        self.assertEqual(tour.name, '9. Karl-Mala-Gedenkturnier')
        self.assertEqual(tour.city, 'Frankfurt (Main) /GER')
        self.assertEqual(tour.federation, '')
        self.assertEqual(tour.startdate, '28. 07. 2005')
        self.assertEqual(tour.enddate, '31. 07. 2005')
        self.assertEqual(tour.numplayers, 284)
        self.assertEqual(tour.numratedplayers, 146)
        self.assertEqual(tour.numteams, 0)
        self.assertEqual(tour.type, 'Individual: Swiss-System (Standard)')
        self.assertEqual(tour.chiefarbiter, 'Ralph Blum (SV Griesheim)')
        self.assertEqual(tour.deputyarbiters,
                         'NSR Thomas Rondio, NSR Wolfgang Hettler')
        self.assertEqual(tour.rateofplay, '40/120, 60')
        self.assertEqual(tour.rounddates, [])
        self.assertEqual(tour.numrounds, 7)

        for p in tour.players:
            self.assertIsInstance(p, trf.Player)

            for g in p.games:
                self.assertIsInstance(g, trf.Game)

        self.assertEqual(tour.players[25].name, 'Schaffer,Hendrik')
        self.assertEqual(tour.players[144].id, 24615480)
        self.assertEqual(tour.players[114].rating, 1994)
        self.assertEqual(tour.players[81].birthdate, '1965.09.07')
        self.assertEqual(tour.players[74].games[4], trf.Game(188, 'w', '1', 5))

    @repeat(RANDOM_TEST_NUMBER)
    def test_random_chinese_whispers(self):
        tour = rt.tournament(RANDOM_PLAYERS_NUMBER)
        self.chinese_whispers(tour)

    def test_example1_chinese_whispers(self):
        self.chinese_whispers_from_file('example1')

    def test_2020_06_chinese_whispers(self):
        self.chinese_whispers_from_file('2020_06')

    def test_2021_03_chinese_whispers(self):
        self.chinese_whispers_from_file('2021_03')

    def chinese_whispers_from_file(self, name):
        filename = os.path.join(os.path.dirname(__file__), name+'.trf')
        with open(filename) as f:
            trf_string = f.read()
        tour0 = trf.loads(trf_string)
        self.chinese_whispers(tour0)

    def chinese_whispers(self, tour0):
        dumped = trf.dumps(tour0)

        for i in range(CHINESE_WHISPERS_NUMBER):
            itertext = f' in iteration {i+1}'

            tour = trf.loads(dumped)
            dumped = trf.dumps(tour)

            self.assertIsInstance(tour, trf.Tournament)
            self.assertEqual(tour.name, tour0.name,
                             'Diff of {tournament.name}' + itertext)
            self.assertEqual(tour.city, tour0.city,
                             'Diff of {tournament.city}' + itertext)
            self.assertEqual(tour.federation, tour0.federation,
                             'Diff of {tournament.federation}' + itertext)
            self.assertEqual(tour.startdate, tour0.startdate,
                             'Diff of {tournament.startdate}' + itertext)
            self.assertEqual(tour.enddate, tour0.enddate,
                             'Diff of {tournament.enddate}' + itertext)
            self.assertEqual(tour.numplayers, tour0.numplayers,
                             'Diff of {tournament.numplayers}' + itertext)
            self.assertEqual(tour.numratedplayers, tour0.numratedplayers,
                             'Diff of {tournament.numratedplayers}' + itertext)
            self.assertEqual(tour.numteams, tour0.numteams,
                             'Diff of {tournament.numteams}' + itertext)
            self.assertEqual(tour.type, tour0.type,
                             'Diff of {tournament.type}' + itertext)
            self.assertEqual(tour.chiefarbiter, tour0.chiefarbiter,
                             'Diff of {tournament.chiefarbiter}' + itertext)
            self.assertEqual(tour.deputyarbiters, tour0.deputyarbiters,
                             'Diff of {tournament.deputyarbiters}' + itertext)
            self.assertEqual(tour.rateofplay, tour0.rateofplay,
                             'Diff of {tournament.rateofplay}' + itertext)
            self.assertEqual(tour.rounddates, tour0.rounddates,
                             'Diff of {tournament.rounddates}' + itertext)
            self.assertEqual(tour.xx_fields, tour0.xx_fields,
                             'Diff of {tournament.xx_fields}' + itertext)

            self.assertEqual(len(tour.players), len(tour0.players))
            for j, (player, player0) in enumerate(zip(tour.players, tour0.players)):
                self.assertIsInstance(player, trf.Player)
                self.assertEqual(player.startrank, player0.startrank,
                                 f'Diff of {{player[{j}].startrank}}' + itertext)
                self.assertEqual(player.sex, player0.sex,
                                 f'Diff of {{player[{j}].sex}}' + itertext)
                self.assertEqual(player.title, player0.title,
                                 f'Diff of {{player[{j}].title}}' + itertext)
                self.assertEqual(player.name, player0.name,
                                 f'Diff of {{player[{j}].name}}' + itertext)
                self.assertEqual(player.rating, player0.rating,
                                 f'Diff of {{player[{j}].rating}}' + itertext)
                self.assertEqual(player.fed, player0.fed,
                                 f'Diff of {{player[{j}].fed}}' + itertext)
                self.assertEqual(player.id, player0.id,
                                 f'Diff of {{player[{j}].id}}' + itertext)
                self.assertEqual(player.birthdate, player0.birthdate,
                                 f'Diff of {{player[{j}].birthdate}}' + itertext)
                self.assertEqual(player.points, player0.points,
                                 f'Diff of {{player[{j}].points}}' + itertext)
                self.assertEqual(player.rank, player0.rank,
                                 f'Diff of {{player[{j}].rank}}' + itertext)
                self.assertEqual(player.games, player0.games,
                                 f'Diff of {{player[{j}].games}}' + itertext)
