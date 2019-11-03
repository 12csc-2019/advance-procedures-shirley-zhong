import sys
import pygame
import time

#ball velocity
#[X,Y]
#[5,-5] up-right direction
#[-5,-5] up-left direction
#[-5,5] down-right direction
#[-5,-5]  down-left direction

WINDOW_SIZE = 700,500

#Object sizes
BRICK_WIDTH = 50
BRICK_HEIGHT = 15
PADDLE_WIDTH = 75
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS   = BALL_DIAMETER // 2

#ball and paddle movement boundaries
MAX_PADDLE_X = WINDOW_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X = WINDOW_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y = WINDOW_SIZE[1] - BALL_DIAMETER

#paddle Y coordinate
PADDLE_Y = WINDOW_SIZE[1] - PADDLE_HEIGHT - 10

#colours
BLUE = (2, 39, 77)
YELLOW = (229, 229, 76)
PINK = (209, 72, 118)
WHITE = (255, 255, 255)

#states
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3


class Breakout:

    def __init__(self):
        
        pygame.font.init()
        global font
        font = pygame.font.SysFont("Arial", 25)          #make font object
        
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Breakout Challenge")

        self.clock = pygame.time.Clock()
        
        self.init_game()
        

    def init_game(self):
        self.state = STATE_BALL_IN_PADDLE
        self.paddle = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)                #paddle properties
        self.ball = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)    #ball properties
        self.create_bricks()
        

    def screen_message(self, msg, location, colour):
        screen_text = font.render(msg, True, colour)
        self.screen.blit(screen_text, location)


    def create_bricks(self):
        self.bricks = []
        y_pos = 50
        for y in range(7):
            x_pos = 55
            for x in range(10):
                brick_rect = pygame.Rect(x_pos, y_pos, BRICK_WIDTH, BRICK_HEIGHT)
                self.bricks.append(brick_rect)
                x_pos += BRICK_WIDTH + 10
            y_pos += BRICK_HEIGHT + 10
        pygame.display.update()


    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, YELLOW, brick)

    
    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle.x -= 5

        elif keys[pygame.K_RIGHT]:
            self.paddle.x += 5

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [4.5,-4.5]
            self.state = STATE_PLAYING

        if keys[pygame.K_ESCAPE] and self.state == STATE_BALL_IN_PADDLE:
            pygame.quit()   #esc to quit when game hasn't started
            sys.exit()

        if keys[pygame.K_ESCAPE] and self.state == STATE_WON:
            pygame.quit()   #esc pygame when game has been won
            sys.exit()
            
        elif keys[pygame.K_RETURN] and self.state == STATE_WON:
            self.init_game()    #resets game when won and enter is pressed


    def move_ball(self):
        self.ball.x += self.ball_vel[0]
        self.ball.y  += self.ball_vel[1]
    
        if self.ball.x <= 0:
            self.ball.x = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.x >= MAX_BALL_X:
            self.ball.x = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.y < 0:
            self.ball.y = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.y >= MAX_BALL_Y:            
            self.ball.y = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]


    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON  #state changes to STATE_WON when all bricks gone
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            time.sleep(0.5)
            self.init_game() 
            

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            self.check_input()
            self.clock.tick(60)     #locks fps
            self.screen.fill(BLUE)   #refresh screen

            if self.state == STATE_WON:
                self.screen_message("You win! Press Enter to play again", (205,300), WHITE)
                self.screen_message("Press Esc to quit", (280,340), WHITE)
                pygame.event.set_grab(True)

            if self.state == STATE_PLAYING:
                self.move_ball()    
                self.handle_collisions()
                pygame.mouse.set_visible(False)     #makes cursor invisble
                pygame.event.set_grab(True)      #lock cursor in window
                
            if self.state == STATE_BALL_IN_PADDLE:
                self.screen_message("Press Space to launch the ball", (220,300), WHITE)
                self.ball.left = self.paddle.left + self.paddle.width / 2.5
                self.ball.top = self.paddle.top - self.ball.height
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                
            if event.type == pygame.MOUSEMOTION:    #move paddle by mouse
                self.mousePosition = event.pos[0]   
                self.paddle.x = self.mousePosition
        
            #draw bricks
            self.draw_bricks()

            #draw paddle
            pygame.draw.rect(self.screen, PINK, self.paddle)
                  
            #draw ball    
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

            #constantly refresh display
            pygame.display.update()
       

if __name__ == "__main__":
    Breakout().run()
    
