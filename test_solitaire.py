import unittest
from solitaire_game import SolitaireGame


class TestSolitaireGame(unittest.TestCase):

    def test_center_is_empty(self):
        game = SolitaireGame("English", 7)
        self.assertEqual(game.get_board()[3][3], 0)

    def test_valid_move(self):
        game = SolitaireGame("English", 7)

        result = game.make_move(3, 1, 3, 3)

        self.assertTrue(result)
        self.assertEqual(game.count_pegs(), 31)

    def test_invalid_move(self):
        game = SolitaireGame("English", 7)

        result = game.make_move(3, 2, 3, 3)

        self.assertFalse(result)

    def test_board_type(self):
        game = SolitaireGame("Diamond", 7)

        self.assertEqual(
            game.get_board_type(),
            "Diamond"
        )

    def test_size_5_board(self):
        game = SolitaireGame("English", 5)

        self.assertEqual(
            game.get_board_size(),
            5
        )

        self.assertEqual(
            game.count_pegs(),
            20
        )

    def test_size_7_board(self):
        game = SolitaireGame("English", 7)

        self.assertEqual(
            game.get_board_size(),
            7
        )

        self.assertEqual(
            game.count_pegs(),
            32
        )

    def test_size_9_board(self):
        game = SolitaireGame("English", 9)

        self.assertEqual(
            game.get_board_size(),
            9
        )

        self.assertEqual(
            game.count_pegs(),
            44
        )


if __name__ == "__main__":
    unittest.main()