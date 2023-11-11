from copy import deepcopy
import pygame
from search import create_initial_node, Search
import sokoPuzzle
from threading import Timer
import time
from sys import exit



class Sokoban():

    def __init__(self):
        pygame.init()

        self.level = 0
        self.game_is_solved = False

        self.load_images()
        self.new_game()

        self.height = len(self.map)
        self.width = len(self.map[0])

        self.scale = self.images[0].get_width()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode(
            (window_width, window_height + self.scale))
        self.game_font = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Sokoban")

        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ["floor", "wall", "target", "box", "robot", "done", "target_robot"]:
            self.images.append(pygame.image.load("images/" + name + ".png"))

    def new_game(self):
        if (self.game_is_solved):
            self.level = 0
            self.game_is_solved = False

        maps = [
            [
         [1, 1, 1, 1, 1, 1, 1, 1,    1,],
         [1, 0, 0, 0, 1, 1, 1, 1,    1,],
         [1, 0, 0, 0, 0, 1, 1, 1,    1,],
         [1, 1, 1, 0, 3, 0, 0, 1,    1,],
         [1, 1, 0, 3, 5, 6, 0, 1,    1,],
         [1, 1, 0, 0, 2, 0, 0, 1,    1,],
         [1, 1, 1, 1, 1, 1, 1, 1,    1,],

         [1, 1, 1, 1, 1, 1, 1,1, 1,],
         [1, 1, 1, 1, 1, 1, 1, 1, 1,]
        ],
        [
         [1, 1, 1, 1, 1, 1, 1,    1, 1,],
         [1, 1, 1, 0, 0, 1, 1,    1, 1,],
         [1, 1, 1, 0, 0, 1, 1,    1, 1,],
         [1, 1, 1, 0, 4, 1, 1,    1, 1,],
         [1, 0, 5, 3, 2, 0, 1,    1, 1,],
         [1, 0, 0, 0, 0, 0, 1,    1, 1,],
         [1, 1, 0, 0, 1, 1, 1,    1, 1,],
         [1, 1, 1, 1, 1, 1, 1,    1, 1,],

         [1, 1, 1, 1, 1, 1, 1, 1, 1,]
        ],
        [[1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 2, 0, 3, 0, 1 ,1 ,1 ,1],
        [1, 0, 1, 4, 0, 1 ,1 ,1 ,1],
        [1, 0, 0, 0, 0, 1 ,1 ,1 ,1],
        [1, 0, 0, 0, 0, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1]],
        [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 6, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 3, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]],
        [[1, 1, 1, 1, 1, 1, 1, 1 ,1],
        [1, 0, 0, 0, 1, 0, 0, 1 ,1],
        [1, 0, 0, 3, 4, 0, 0, 1 ,1],
        [1, 0, 0, 0, 1, 3, 0, 1 ,1],
        [1, 1, 1, 1, 1, 0, 2, 1 ,1],
        [1, 1, 1, 1, 1, 0, 2, 1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1, 1, 1 ,1]],
        [[1, 1, 1, 1, 1, 1, 1 ,1 ,1],
        [1, 1, 0, 0, 1, 1, 1 ,1 ,1],
        [1, 1, 0, 0, 1, 1, 1 ,1 ,1],
        [1, 1, 0, 5, 0, 0, 1 ,1 ,1],
        [1, 1, 3, 1, 3, 0, 1 ,1 ,1],
        [1, 0, 2, 4, 2, 0, 1 ,1 ,1],
        [1, 0, 0, 0, 0, 1, 1 ,1 ,1],
        [1, 1, 1, 0, 0, 1, 1 ,1 ,1],
        [1, 1, 1, 1, 1, 1, 1 ,1 ,1]],
        [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 2, 1, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 3, 0, 1, 1],
        [1, 0, 3, 0, 4, 0, 0, 2, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 1, 1, 3, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 2, 1, 1, 1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]],
        [[1, 1, 1, 1, 1, 1, 1 ,1 ,1],
        [1, 2, 0, 1, 0, 4, 1 ,1 ,1],
        [1, 0, 0, 1, 3, 0, 1 ,1 ,1],
        [1, 2, 0, 0, 3, 0, 1 ,1 ,1],
        [1, 0, 0, 1, 3, 0, 1 ,1 ,1],
        [1, 2, 0, 1, 0, 0, 1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1, 1 ,1 ,1]],
        [[1, 1, 1, 1, 1, 1, 1, 1 ,1],
        [1, 2, 2, 2, 0, 1, 1, 1 ,1],
        [1, 0, 2, 0, 3, 0, 0, 1 ,1],
        [1, 0, 0, 3, 3, 3, 0, 1 ,1],
        [1, 1, 1, 1, 0, 0, 4, 1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1, 1, 1 ,1]],
        [[1, 1, 1, 1, 1, 1, 1, 1 ,1],
        [1, 0, 0, 0, 0, 1, 1, 1 ,1],
        [1, 0, 0, 0, 3, 0, 0, 1 ,1],
        [1, 2, 2, 2, 5, 3, 4, 1 ,1],
        [1, 0, 0, 0, 3, 0, 0, 1 ,1],
        [1, 0, 0, 0, 1, 1, 1, 1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1, 1, 1 ,1]],
        [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 2, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 2, 0, 2, 0, 1, 1, 1, 1],
        [1, 0, 3, 0, 3, 3, 0, 0, 1],
        [1, 1, 1, 2, 0, 0, 3, 4, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1 ,1 ,1 ,1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]]
        ]

        self.map = maps[self.level]
        self.moves = 0

    def main_loop(self):
        while True:
            self.draw_window()
            self.check_events()
            
    def draw_window(self):
        self.window.fill((0, 0, 0))

        game_text = self.game_font.render(
            "Moves: " + str(self.moves), True, (255, 0, 0))
        self.window.blit(game_text, (25, self.height * self.scale + 10))

        game_text = self.game_font.render(
            "Niveau: "+str(self.level), True, (255, 0, 0))
        self.window.blit(game_text, (200, self.height * self.scale + 10))

        # game_text = self.game_font.render("F2 = new try", True, (255, 0, 0))
        # self.window.blit(game_text, (400, self.height * self.scale + 10))

        # game_text = self.game_font.render("Esc = exit game", True, (255, 0, 0))
        # self.window.blit(game_text, (600, self.height * self.scale + 10))

        for y in range(self.height):
            for x in range(self.width):
                square = self.map[y][x]
                self.window.blit(
                    self.images[square], (x * self.scale, y * self.scale))

        if self.all_game_solved():
            game_text = self.game_font.render(
                "Congratulations, you solved the game! F2 = NEW GAME", True, (255, 0, 0))
            game_text_x = self.scale * self.width / 2 - game_text.get_width() / 2
            game_text_y = self.scale * self.height / 2 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0), (game_text_x,
                                                      game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))

        pygame.display.flip()
    
    #if event.key == pygame.K_RETURN: 
    def check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.auto_solve()
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)
                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

    def find_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [4, 6]:
                    return (y, x)

    def move(self, move_y, move_x):
        if self.all_game_solved():
            return
        robot_old_y, robot_old_x = self.find_robot()
        robot_new_y = robot_old_y + move_y
        robot_new_x = robot_old_x + move_x

        if self.map[robot_new_y][robot_new_x] == 1:
            return

        if self.map[robot_new_y][robot_new_x] in [3, 5]:
            box_new_y = robot_new_y + move_y
            box_new_x = robot_new_x + move_x

            if self.map[box_new_y][box_new_x] in [1, 3, 5]:
                return

            self.map[robot_new_y][robot_new_x] -= 3
            self.map[box_new_y][box_new_x] += 3

        self.map[robot_old_y][robot_old_x] -= 4
        self.map[robot_new_y][robot_new_x] += 4
        self.moves += 1

    def all_game_solved(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [2, 6]:
                    return False
        if self.level != 8:
            self.level += 1
            self.new_game()
        elif self.level == 4:
            self.game_is_solved = True
            return True


    # Auto solver using A_star algorithm
    def auto_solve(self): 
       #convert the board to fit the sokopuzzle. 
       #initial_node = create_initial_node(board=board5)
       #goalNode, num_steps = Search.breadthFirst(initial_node)
       #moves = goalNode.moves;
       #for each move in moves:
            #execute move in this game
            #sleep 0.2 seconds
       dictionnary = {
        0:' ',
        1:'O',  
        2:'S',
        3:'B',
        4:'R',
        5:'*',
        6:'.'
       }
       board = deepcopy(self.map);

       for i in range (len(board)):
            for j in range (len(board[0])):
                board[i][j] = dictionnary[board[i][j]]
            
       initial_node = create_initial_node(board)
       # goalNode, num_steps = Search.breadthFirst(initial_node)
       goalNode, num_steps = Search.A(initial_node, heuristic=3)
       moves = goalNode.moves
       print('Moves are: ', moves)


       for move in moves:
            if move == 'U':
                self.move(-1, 0)
                self.draw_window()
                time.sleep(0.2)
            if move =='L':
                self.move(0, -1)
                self.draw_window()
                time.sleep(0.2)
            if move == 'R': 
                self.move(0,1)
                self.draw_window()
                time.sleep(0.2)
            if move == 'D':
                self.move(1, 0)
                self.draw_window()
                time.sleep(0.2)
       
if __name__ == "__main__":
    Sokoban()

