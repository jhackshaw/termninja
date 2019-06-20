import socketserver
import socket
import threading
import itertools
import time
import random
from shared import Cursor


class SnakeBoard:
    WIDTH = 45
    HEIGHT = 15
    PADDING = 10
    DIRECTIONS = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1)
    }
    INVALID_TURNS = {
        "a": "d",
        "d": "a",
        "w": "s",
        "s": "w"
    }

    def __init__(self):
        self.init_board()
        self.init_fills()
        self.init_snake()
        self.init_food()
        self.score = 0
        self.game_over = False
        self.direction = random.choice(
            list(self.DIRECTIONS.keys())
        )

    def init_board(self):
        top = " " * (self.PADDING+1) + \
              Cursor.blue("=" * self.WIDTH) + "\n"
        mid = " " * self.PADDING + \
              Cursor.blue("|") + \
              "{}" * self.WIDTH + \
              Cursor.blue("|\n") 
        self.board = "\n\n" + top + mid*self.HEIGHT + top

    def init_fills(self):
        self.fills = [
            [" " for _ in range(self.WIDTH)]
            for _ in range(self.HEIGHT)
        ]
    
    def init_snake(self):
        head = (self.HEIGHT // 2, self.WIDTH // 2)
        self.snake = [head,]
        self.fills[head[0]][head[1]] = Cursor.red("@")
    
    def init_food(self):
        self.food_options = set(
            (r, c)
            for r in range(self.HEIGHT)
            for c in range(self.WIDTH)
        )
        self.spawn_food()

    def spawn_food(self):
        choices = self.food_options - set(self.snake)
        self.food = random.choice(list(choices))
        self.fills[self.food[0]][self.food[1]] = Cursor.green("*")

    def turn(self, turn):
        if self.is_valid_turn(turn):
            self.direction = turn
    
    def is_valid_turn(self, turn):
        invalid = self.INVALID_TURNS.get(self.direction)
        return turn in self.INVALID_TURNS and turn != invalid

    def tick(self):
        delta_y, delta_x = self.DIRECTIONS[self.direction]
        new_head = (self.snake[0][0] + delta_y, self.snake[0][1] + delta_x)
        if self.check_game_over(new_head):
            print("GO")
            self.game_over = True
        else:
            self.update_snake(new_head)

    def check_game_over(self, new_head):
        new_y, new_x = new_head
        if new_x >= self.WIDTH or new_x < 0:
            # hit side will
            return True
        if new_y >= self.HEIGHT or new_y < 0:
            # hit top or bot wall
            return True
        for y, x in self.snake:
            # hit themself
            if new_y == y and new_x == x:
                return True

    def eats_food(self, new_head):
        return self.food[0] == new_head[0] and self.food[1] == new_head[1]

    def update_snake(self, new_head):
        self.fills[self.snake[0][0]][self.snake[0][1]] = Cursor.yellow("#")
        self.fills[new_head[0]][new_head[1]] = Cursor.red("@")
        self.snake.insert(0, new_head)
        if self.eats_food(new_head):
            self.score += 1
            self.spawn_food()
        else:
            tail = self.snake.pop()
            self.fills[tail[0]][tail[1]] = " "
    
    @property
    def effective_height(self):
        return self.HEIGHT + 2

    def render(self):
        return self.board.format(*itertools.chain(*self.fills))


class SnakeController(socketserver.BaseRequestHandler):
    DELAY = 0.18

    def setup(self):
        self.board = SnakeBoard()
        self.disconnected = False
        self.request.setblocking(False)

    def handle(self):
        while not self.disconnected and not self.board.game_over:
            self.handle_input()
            self.board.tick()
            self.send_board()
            time.sleep(self.DELAY)

    def handle_input(self):
        try:
            data = self.request.recv(8).decode().strip()
            if data == "":
                self.disconnected = True
            else:
                self.board.turn(data[-1])
        except socket.error as e:
            # ignore non-blocking errors, throw anything else
            if e.errno != 11:
                raise e

    def ready_up(self):
        self.send("hi there")
    
    def send_board(self):
        self.send(
            Cursor.reset(self.board.effective_height) + \
            self.board.render()
        )

    def send(self, msg):
        try:
            self.request.sendall(msg.encode())
        except socket.error:
            self.disconnected = True


class SnakeServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, host, port):
        self.host = host
        self.port = port
        super().__init__((host, port), SnakeController)

    def process_request(self, request, client_address):
        print(f"[+] {threading.active_count()} "
              f"{client_address[0]}:{client_address[1]}")
        return super().process_request(request, client_address)


if __name__ == "__main__":
    with SnakeServer("0.0.0.0", 3002) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass