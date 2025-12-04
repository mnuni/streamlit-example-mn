import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0
    
    def move(self):
        self.rect.y += self.speed
        # Keep paddle within screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1
    
    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x *= -1
        self.speed_y = BALL_SPEED_Y
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        
        # Create paddles and ball
        self.player_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ai_paddle = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        
        # Scores
        self.player_score = 0
        self.ai_score = 0
        
        # Font for score display
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Player controls (W and S keys)
        if keys[pygame.K_w]:
            self.player_paddle.speed = -PADDLE_SPEED
        elif keys[pygame.K_s]:
            self.player_paddle.speed = PADDLE_SPEED
        else:
            self.player_paddle.speed = 0
    
    def update_ai(self):
        # Simple AI: follow the ball
        if self.ai_paddle.rect.centery < self.ball.rect.centery:
            self.ai_paddle.speed = PADDLE_SPEED
        elif self.ai_paddle.rect.centery > self.ball.rect.centery:
            self.ai_paddle.speed = -PADDLE_SPEED
        else:
            self.ai_paddle.speed = 0
    
    def check_collisions(self):
        # Check collision with paddles
        if self.ball.rect.colliderect(self.player_paddle.rect) or self.ball.rect.colliderect(self.ai_paddle.rect):
            self.ball.speed_x *= -1
        
        # Check if ball goes out of bounds (scoring)
        if self.ball.rect.left <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.player_score += 1
            self.ball.reset()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw center line
        pygame.draw.aaline(self.screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        
        # Draw paddles and ball
        self.player_paddle.draw(self.screen)
        self.ai_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        self.screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
        self.screen.blit(ai_text, (3 * SCREEN_WIDTH // 4, 20))
        
        # Draw controls info
        controls_text = self.small_font.render("W/S: Move Paddle  |  ESC: Quit", True, WHITE)
        self.screen.blit(controls_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 40))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.handle_input()
            self.update_ai()
            
            # Move objects
            self.player_paddle.move()
            self.ai_paddle.move()
            self.ball.move()
            
            # Check collisions
            self.check_collisions()
            
            # Draw everything
            self.draw()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PongGame()
    game.run()