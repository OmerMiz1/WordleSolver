class IPlayer:
    def solve(self, game):
        """
        Starts the game.

        :param game: the game object that the player solves
        :return: Nothing, the game is responsible for providing results
        """
        raise NotImplemented()

    def reset(self):
        """
        Resets all game related variables, preparing for new game.

        :return: Nothing
        """
        raise NotImplemented()
