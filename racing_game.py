import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)

# Physics constants
GRAVITY = 0.3
FRICTION = 0.98
AIR_RESISTANCE = 0.99
MAX_SPEED = 15
ACCELERATION = 0.3
BRAKE_FORCE = 0.5
BOOST_POWER = 1.5
TURN_SPEED = 0.05

class Vector3:
    """Simple 3D vector class"""
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def copy(self):
        return Vector3(self.x, self.y, self.z)
    
    def add(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def scale(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

class Camera:
    """3D camera for perspective projection"""
    def __init__(self):
        self.position = Vector3(0, -5, -20)
        self.rotation = 0
        self.fov = 400
        self.horizon = SCREEN_HEIGHT // 2
    
    def project(self, point):
        """Project 3D point to 2D screen coordinates"""
        # Apply camera rotation
        cos_angle = math.cos(self.rotation)
        sin_angle = math.sin(self.rotation)
        
        dx = point.x - self.position.x
        dz = point.z - self.position.z
        
        rotated_x = dx * cos_angle - dz * sin_angle
        rotated_z = dx * sin_angle + dz * cos_angle
        
        dy = point.y - self.position.y
        
        # Perspective projection
        if rotated_z > 0.1:
            scale = self.fov / rotated_z
            screen_x = SCREEN_WIDTH // 2 + rotated_x * scale
            screen_y = self.horizon - dy * scale
            return (int(screen_x), int(screen_y), rotated_z)
        return None

class TrackSegment:
    """Represents a segment of the racing track"""
    def __init__(self, start_pos, end_pos, width=8):
        self.start = start_pos
        self.end = end_pos
        self.width = width
        
    def get_corners(self):
        """Get the four corners of the track segment"""
        # Calculate perpendicular offset for track width
        dx = self.end.x - self.start.x
        dz = self.end.z - self.start.z
        length = math.sqrt(dx * dx + dz * dz)
        
        if length > 0:
            offset_x = (-dz / length) * self.width
            offset_z = (dx / length) * self.width
        else:
            offset_x = self.width
            offset_z = 0
        
        return [
            Vector3(self.start.x + offset_x, self.start.y, self.start.z + offset_z),
            Vector3(self.start.x - offset_x, self.start.y, self.start.z - offset_z),
            Vector3(self.end.x - offset_x, self.end.y, self.end.z - offset_z),
            Vector3(self.end.x + offset_x, self.end.y, self.end.z + offset_z)
        ]

class Track:
    """Elevated racing track with jumps, ramps, and banked turns"""
    def __init__(self):
        self.segments = []
        self.checkpoints = []
        self.build_track()
    
    def build_track(self):
        """Build an exciting elevated track with various features"""
        points = []
        
        # Start area - flat
        points.append(Vector3(0, 0, 0))
        points.append(Vector3(0, 0, 20))
        
        # Upward ramp
        for i in range(5):
            z = 20 + i * 8
            y = i * 3
            points.append(Vector3(0, y, z))
        
        # High section with slight curve
        base_y = points[-1].y
        for i in range(8):
            angle = i * 0.3
            x = math.sin(angle) * 15
            z = points[-1].z + 6
            points.append(Vector3(x, base_y, z))
        
        # Jump section - gap in track (but car continues)
        jump_start = points[-1]
        jump_end = Vector3(jump_start.x, base_y - 3, jump_start.z + 25)
        points.append(jump_end)
        
        # Downward slope
        for i in range(5):
            z = points[-1].z + 6
            y = points[-1].y - 2
            x = points[-1].x
            points.append(Vector3(x, y, z))
        
        # Banked turn (right)
        turn_center = points[-1]
        for i in range(10):
            angle = math.pi * i / 10
            x = turn_center.x + math.cos(angle) * 20
            z = turn_center.z + math.sin(angle) * 20
            y = turn_center.y + math.sin(i * 0.3) * 3  # Banking effect
            points.append(Vector3(x, y, z))
        
        # Long straight with hill
        for i in range(8):
            z = points[-1].z + 8
            # Create a hill
            hill_factor = math.sin(i * math.pi / 8)
            y = points[-1].y + hill_factor * 4
            points.append(Vector3(points[-1].x, y, z))
        
        # Final turn back to start
        final_turn = points[-1]
        for i in range(10):
            angle = -math.pi * i / 10
            x = final_turn.x + math.cos(angle) * 25
            z = final_turn.z + math.sin(angle) * 15
            y = max(0, points[-1].y - i * 1.5)
            points.append(Vector3(x, y, z))
        
        # Connect back to start
        points.append(Vector3(0, 0, 0))
        
        # Create segments from points
        for i in range(len(points) - 1):
            segment = TrackSegment(points[i], points[i + 1])
            self.segments.append(segment)
        
        # Set up checkpoints (evenly spaced)
        checkpoint_interval = len(self.segments) // 5
        for i in range(0, len(self.segments), checkpoint_interval):
            self.checkpoints.append(i)
    
    def get_position_on_track(self, progress):
        """Get position and normal on track based on progress (0-1)"""
        segment_index = int(progress * len(self.segments)) % len(self.segments)
        segment = self.segments[segment_index]
        
        local_progress = (progress * len(self.segments)) % 1.0
        
        # Interpolate position
        pos = Vector3(
            segment.start.x + (segment.end.x - segment.start.x) * local_progress,
            segment.start.y + (segment.end.y - segment.start.y) * local_progress,
            segment.start.z + (segment.end.z - segment.start.z) * local_progress
        )
        
        # Calculate track direction
        dx = segment.end.x - segment.start.x
        dz = segment.end.z - segment.start.z
        angle = math.atan2(dx, dz)
        
        return pos, angle, segment_index

class Car:
    """Player's racing car with physics"""
    def __init__(self, track):
        self.track = track
        self.progress = 0.0  # Position on track (0-1)
        self.position = Vector3(0, 0, 0)
        self.velocity = 0
        self.vertical_velocity = 0
        self.angle = 0
        self.on_ground = True
        self.boost_amount = 100
        self.boost_recharge_rate = 0.1
        self.max_boost = 100
        self.lap_time = 0
        self.current_lap = 0
        self.last_checkpoint = -1
        
    def update(self, dt, controls):
        """Update car physics and position"""
        # Handle acceleration and braking
        if controls['throttle']:
            self.velocity += ACCELERATION
        if controls['brake']:
            self.velocity -= BRAKE_FORCE
        
        # Handle boost
        if controls['boost'] and self.boost_amount > 0 and self.on_ground:
            self.velocity += BOOST_POWER
            self.boost_amount -= 1
        else:
            self.boost_amount = min(self.max_boost, self.boost_amount + self.boost_recharge_rate)
        
        # Apply friction and limits
        if self.on_ground:
            self.velocity *= FRICTION
        else:
            self.velocity *= AIR_RESISTANCE
        
        self.velocity = max(-MAX_SPEED / 2, min(MAX_SPEED, self.velocity))
        
        # Handle steering
        if controls['left'] and abs(self.velocity) > 0.5:
            self.progress -= TURN_SPEED * abs(self.velocity) / MAX_SPEED
        if controls['right'] and abs(self.velocity) > 0.5:
            self.progress += TURN_SPEED * abs(self.velocity) / MAX_SPEED
        
        # Update position on track
        self.progress += self.velocity * 0.001
        self.progress = self.progress % 1.0
        
        # Get track position and angle
        track_pos, track_angle, segment_index = self.track.get_position_on_track(self.progress)
        self.angle = track_angle
        
        # Check if on ground (simple collision detection)
        if self.position.y > track_pos.y + 0.5:
            self.on_ground = False
            self.vertical_velocity -= GRAVITY * dt
        else:
            self.on_ground = True
            self.position.y = track_pos.y
            self.vertical_velocity = 0
        
        # Update vertical position
        self.position.y += self.vertical_velocity
        
        # Update horizontal position
        self.position.x = track_pos.x
        self.position.z = track_pos.z
        
        # Check checkpoint
        if segment_index in self.track.checkpoints:
            if segment_index != self.last_checkpoint:
                self.last_checkpoint = segment_index
                # Check if completed lap
                if segment_index == 0 and self.current_lap > 0:
                    self.current_lap += 1
        
        # Update lap time
        self.lap_time += dt
    
    def get_corners(self):
        """Get car corners for rendering"""
        car_length = 3
        car_width = 1.5
        
        corners = [
            Vector3(-car_width, 0, -car_length),
            Vector3(car_width, 0, -car_length),
            Vector3(car_width, 0, car_length),
            Vector3(-car_width, 0, car_length),
            Vector3(-car_width, 2, -car_length),
            Vector3(car_width, 2, -car_length),
            Vector3(car_width, 2, car_length),
            Vector3(-car_width, 2, car_length)
        ]
        
        # Rotate and translate corners
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        
        rotated = []
        for corner in corners:
            x = corner.x * cos_a - corner.z * sin_a + self.position.x
            y = corner.y + self.position.y
            z = corner.x * sin_a + corner.z * cos_a + self.position.z
            rotated.append(Vector3(x, y, z))
        
        return rotated

class RacingGame:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stunt Car Racer - Wireframe Edition")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.track = Track()
        self.car = Car(self.track)
        self.camera = Camera()
        
        # UI fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Start position
        self.car.current_lap = 1
        self.start_time = time.time()
        
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        controls = {
            'throttle': keys[pygame.K_UP],
            'brake': keys[pygame.K_DOWN],
            'left': keys[pygame.K_LEFT],
            'right': keys[pygame.K_RIGHT],
            'boost': keys[pygame.K_SPACE]
        }
        
        return controls
    
    def update(self, dt):
        """Update game state"""
        controls = self.handle_input()
        self.car.update(dt, controls)
        
        # Update camera to follow car
        self.camera.position.x = self.car.position.x
        self.camera.position.y = self.car.position.y - 5
        self.camera.position.z = self.car.position.z - 20
        self.camera.rotation = self.car.angle
    
    def draw_track(self):
        """Render track with wireframe graphics"""
        # Draw track segments
        for i, segment in enumerate(self.track.segments):
            corners = segment.get_corners()
            projected = [self.camera.project(corner) for corner in corners]
            
            # Only draw if all points are visible
            if all(p is not None for p in projected):
                points_2d = [(p[0], p[1]) for p in projected]
                
                # Color based on distance
                avg_z = sum(p[2] for p in projected) / len(projected)
                brightness = max(50, min(255, int(255 - avg_z * 2)))
                
                # Highlight checkpoints
                if i in self.track.checkpoints:
                    color = (brightness, brightness // 2, brightness // 2)
                else:
                    color = (brightness, brightness, brightness)
                
                # Draw track surface
                if len(points_2d) >= 3:
                    pygame.draw.polygon(self.screen, color, points_2d, 1)
                    
                # Draw track edges
                pygame.draw.line(self.screen, color, points_2d[0], points_2d[1], 2)
                pygame.draw.line(self.screen, color, points_2d[2], points_2d[3], 2)
                
                # Draw support pillars for elevated sections
                if segment.start.y > 2:
                    for corner in [corners[0], corners[1]]:
                        ground_point = Vector3(corner.x, 0, corner.z)
                        proj_top = self.camera.project(corner)
                        proj_bottom = self.camera.project(ground_point)
                        if proj_top and proj_bottom:
                            pygame.draw.line(self.screen, GRAY, 
                                           (proj_top[0], proj_top[1]), 
                                           (proj_bottom[0], proj_bottom[1]), 1)
    
    def draw_car(self):
        """Render car with wireframe graphics"""
        corners = self.car.get_corners()
        projected = [self.camera.project(corner) for corner in corners]
        
        if all(p is not None for p in projected):
            points = [(p[0], p[1]) for p in projected]
            
            # Draw car body edges (wireframe cube)
            edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
                (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
                (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
            ]
            
            for edge in edges:
                pygame.draw.line(self.screen, RED, points[edge[0]], points[edge[1]], 2)
            
            # Draw front indicator
            pygame.draw.line(self.screen, YELLOW, points[1], points[5], 3)
    
    def draw_ui(self):
        """Draw user interface"""
        # Speed display
        speed_text = self.font.render(f"Speed: {abs(self.car.velocity):.1f}", True, GREEN)
        self.screen.blit(speed_text, (10, 10))
        
        # Boost meter
        boost_text = self.small_font.render("Boost:", True, CYAN)
        self.screen.blit(boost_text, (10, 50))
        
        boost_bar_width = 200
        boost_bar_height = 20
        boost_fill = int((self.car.boost_amount / self.car.max_boost) * boost_bar_width)
        
        pygame.draw.rect(self.screen, WHITE, (80, 52, boost_bar_width, boost_bar_height), 1)
        pygame.draw.rect(self.screen, CYAN, (80, 52, boost_fill, boost_bar_height))
        
        # Lap timer
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = elapsed % 60
        timer_text = self.font.render(f"Time: {minutes:02d}:{seconds:05.2f}", True, WHITE)
        self.screen.blit(timer_text, (10, 85))
        
        # Lap counter
        lap_text = self.small_font.render(f"Lap: {self.car.current_lap}", True, WHITE)
        self.screen.blit(lap_text, (10, 125))
        
        # On ground indicator
        status = "ON GROUND" if self.car.on_ground else "AIRBORNE!"
        status_color = GREEN if self.car.on_ground else YELLOW
        status_text = self.small_font.render(status, True, status_color)
        self.screen.blit(status_text, (10, 150))
        
        # Controls help
        controls_lines = [
            "Arrow Keys: Steer/Throttle/Brake",
            "Space: Boost",
            "ESC: Quit"
        ]
        
        for i, line in enumerate(controls_lines):
            text = self.small_font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH - 280, SCREEN_HEIGHT - 80 + i * 25))
        
        # Title
        title = self.font.render("STUNT CAR RACER", True, RED)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 150, 10))
    
    def draw(self):
        """Render everything"""
        self.screen.fill(BLACK)
        
        # Draw horizon line
        pygame.draw.line(self.screen, BLUE, (0, self.camera.horizon), 
                        (SCREEN_WIDTH, self.camera.horizon), 1)
        
        # Draw track and car
        self.draw_track()
        self.draw_car()
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = RacingGame()
    game.run()
