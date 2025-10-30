import math
from enum import Enum
import random

# 28 13
world_map = [
    "###################################################################",
    "#######....##############..##########.###########.##..##############",
    "##..................###............#.....#...#.....................#",
    "##..........e........#...................##........................#",
    "##...e...........##............#....................##......e......#",
    "###....#...e...............e.....#...........t......................#",
    "####............#.....+..........##....t........+.......+..#.........#",
    "#####.#......t...#..........#............e.......#.......#.........#",
    "#####..+.......##....#.............#..................#..#.....+..##",
    "####.....................+................#....t................###",
    "####...##....e......##.........e.....+..................e......#...#",
    "###......................t...................t...............###...#",
    "##..............#...............+...##.........#.....#.......#....#",
    "#......e....t...##....e...###........................#......##....#",
    "#.........................#.........+......#...+.................##",
    "#.........##..............#.....#........#.#........#.............##",
    "#...#...........#...+......###.............#.....+...#..t..........#",
    "#..#............#.........................................#........#",
    "##.....+.......##.............#.....t....#.......e.................#",
    "##....................t..............................#...........###",
    "###.......##............................#............#.............##",
    "#..#.............e...#.................##........##....#...e......#",
    "#......e..................##......t....................#..........#",
    "#...e...............................................t.......t.....#",
    "####......###############.....e....############..............######",
    "##### .##############################################....##########",
    "######################################################+############",
    "###################################################################",


]

# INTRO SCENE
TEXT_SPEED = .01
SKIP_INTRO = False

app.background = "black"
app.stepsPerSecond = 10


def label_writer(label, text: str) -> None:
    for character in text:
        sleep(TEXT_SPEED)
        label.value += character

    sleep(.2)
    
def label_remover(label) -> None:
    existing_text = label.value
    
    for i in range(len(existing_text), 0, -3):
        label.value = existing_text[:i]
        sleep(TEXT_SPEED)

    label.value = ""

def run_intro() -> None:
    INTRO_LABEL = Label("", 200, 200, size=15, bold=True, fill="white")
    label_writer(INTRO_LABEL, "There was once a world of beauty and peace")
    label_remover(INTRO_LABEL)
    label_writer(INTRO_LABEL, "At least until a hellish experiment took place")
    label_remover(INTRO_LABEL)
    label_writer(INTRO_LABEL, "Today all that exists is decaying death")
    label_remover(INTRO_LABEL)


if not SKIP_INTRO:
    run_intro()
    
    

SCREEN_SIZE = 400
PRECISION = 10 # raycaster precision
MAX_DEPTH = 6 # render distance
FOV = math.radians(80)
ENEMY_SPEED = .05
LINE_SKIP = 10 # optimization in which every 6th line is rendered, set it to 1 for every line to be rendered



# renders the ground
MAX_GROUND_SIZE = SCREEN_SIZE//2 - (SCREEN_SIZE/MAX_DEPTH/2)
GROUND_COLOR = rgb(139-50, 69-20, 19)
Rect(0, SCREEN_SIZE-MAX_GROUND_SIZE, SCREEN_SIZE, MAX_GROUND_SIZE, fill=gradient(GROUND_COLOR, GROUND_COLOR, GROUND_COLOR, GROUND_COLOR, GROUND_COLOR, GROUND_COLOR, GROUND_COLOR, GROUND_COLOR, "black", start="bottom"))



class Entity:
    __slots__ = [
        "x",
        "y",
        "graphics",
        "canPathfind",
        ]
        
        
    def __init__(self, x: int, y: int, graphics: Group, canPathfind: bool) -> None:
        
        self.x = x
        self.y = y
        self.graphics = graphics
        self.canPathfind = canPathfind
        
        
    


class World:
    __slots__ = ["map", "entities", "enemy_spawns"]
    def __init__(self, world_map: list[str]) -> None:
        self.map = world_map
        
        self.entities = []
        self.enemy_spawns = []
        
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == "t":
                    tombstone = Entity(x, y, Group(Image("cmu://1067374/42468870/tombstone.png", 0, 0, visible=False)), False)
                    self.entities.append(tombstone)
                elif self.map[y][x] == "e":
                    enemyParts = Group(
                        Line(250, 400, 200, 280, lineWidth=10, visible=False, fill="green"),
                        Line(150, 400, 200, 280, lineWidth=10, visible=False, fill="green"),
                        Line(200, 280, 200, 100, lineWidth=10, visible=False, fill="green"),
                        Line(100, 220, 300, 220, lineWidth=10, visible=False, fill="green"),
                        Image("cmu://1067374/42531568/ramones.png", 85, 00, width=230, height=200, opacity=100)
                    )

                    enemy = Entity(x, y, enemyParts, True)
                    self.entities.append(enemy)
                    
                    self.enemy_spawns.append((x, y))
                    
                elif self.map[y][x] == "+":
                    tree = Entity(x, y, Group(Image("cmu://1067374/42532975/tree.png", 0, 0, visible=False)), False)
                    self.entities.append(tree)

    
    def _cord_exists(self, x:int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
            
        if y >= len(self.map):
            return False
            
            
        if x >= len(self.map[y]):
            return False
            
        return True
        
    def is_collision(self, x: int, y: int) -> bool:
        
        if not self._cord_exists(x, y):
            return True

        if self.map[y][x] == "#":
            return True
            
        return False
        

    def is_wall(self, x: int, y: int) -> bool:
        if not self._cord_exists(x, y):
            return False

        return self.map[y][x] == "#"

    
    def enemy_exists(self, x: float, y: float) -> bool:
        for i, entity in enumerate(self.entities):
            if abs(entity.x - x) < .25 and abs(entity.y - y) < .25 and entity.canPathfind:
                return True
        return False
    
    
    def delete_enemy(self, x: float, y: float):
        for i, entity in enumerate(self.entities):
            if abs(entity.x - x) < .25 and abs(entity.y - y) < .25 and entity.canPathfind:
                self.entities[i].graphics.visible=False
                self.entities.pop(i)


    def respawn_enemy(self):
        if len(self.enemy_spawns) == 0:
            return
            
        x, y = random.choice(self.enemy_spawns)
        
        enemyParts = Group(
            Line(250, 400, 200, 280, lineWidth=10, visible=False, fill="green"),
            Line(150, 400, 200, 280, lineWidth=10, visible=False, fill="green"),
            Line(200, 280, 200, 100, lineWidth=10, visible=False, fill="green"),
            Line(100, 220, 300, 220, lineWidth=10, visible=False, fill="green"),
            Image("cmu://1067374/42531568/ramones.png", 85, 00, width=230, height=200, opacity=100)
        )

        enemy = Entity(x, y, enemyParts, True)
        self.entities.append(enemy)

    
    def pathfind_entities(self, player) -> None:
        for entity in self.entities:
            if entity.canPathfind:
                    
                new_x = entity.x
                new_y = entity.y
                    
                if abs(entity.x - player.x) > .5:
                    if entity.x > player.x:
                        new_x -= ENEMY_SPEED
                    if entity.x < player.x:
                        new_x += ENEMY_SPEED
                    
                if abs(entity.y - player.y) > .5:
                    if entity.y > player.y:
                        new_y -= ENEMY_SPEED
                    if entity.y < player.y:
                        new_y += ENEMY_SPEED                
                
                if not self.is_collision(int(new_x), int(new_y)):
                    entity.x = new_x
                    entity.y = new_y
                    
                




class Renderer:
    __slots__ = [
        "lines",
        "distanceBuffer",
    ]

    def __init__(self) -> None:
        self.lines = [Line(x, 0, x, SCREEN_SIZE, fill="darkGray", visible=False, lineWidth=LINE_SKIP) for x in range(SCREEN_SIZE)]
        self.distanceBuffer = [MAX_DEPTH for _ in range(SCREEN_SIZE)]


    def render_scene(self, player, world: World) -> None:
        for ray in range(0, SCREEN_SIZE, LINE_SKIP):
            angle = player.angle - FOV/2 + FOV * (ray / SCREEN_SIZE)
    
            for depth in range(1, MAX_DEPTH*PRECISION):
                x = player.x + depth/PRECISION * math.cos(angle)
                y = player.y + depth/PRECISION * math.sin(angle)
    

                if world.is_wall(int(x), int(y)):
                    self.set_line(ray, depth/PRECISION)
                    break
                
        self.draw_entitys(player, world)

    def refresh_frame(self) -> None:
        for i, line in enumerate(self.lines):
            line.visible = False
            line.fill = "black"

            line.x1 = i
            line.y1 = 0
            line.x2 = i
            line.y2 = SCREEN_SIZE
            
            self.distanceBuffer[i] = MAX_DEPTH
  


    def draw_entitys(self, player, world: World) -> None:
        
        for entity in world.entities:
            dx = entity.x - player.x
            dy = entity.y - player.y
            
            entity_distance = abs(distance(entity.x, entity.y, player.x, player.y))
            if entity_distance > MAX_DEPTH:
                entity.graphics.visible = False
                continue
            
            angle_difference = math.atan2(dy, dx) - player.angle

            # makes it between [-pi, pi]           
            if angle_difference > math.pi:
                angle_difference -= 2*math.pi
            
            elif angle_difference < -math.pi:
                angle_difference += 2*math.pi
            
            
            # idk why i have to do a /1.65, i think im just doing this wrong but it works enough
            xCord = (angle_difference / (FOV/1.65)) * SCREEN_SIZE/2 + SCREEN_SIZE/2
            
            # try:
            if xCord >= 400 or xCord < 0:
                entity.graphics.visible = False
                continue
            bufferDistance = self.distanceBuffer[int(xCord)]
            
            if entity_distance > bufferDistance:
                entity.graphics.visible = False
                continue

            
            entity.graphics.visible=True
            entity.graphics.centerX = xCord
            entity.graphics.centerY = SCREEN_SIZE/2
            entity.graphics.height = (SCREEN_SIZE/2) / (entity_distance+.001)
            entity.graphics.width = entity.graphics.height
            
     
    
    

    def set_line(self, i: int, depth: float) -> None:
        line = self.lines[i]
        
        if i < SCREEN_SIZE-LINE_SKIP:
            for j in range(LINE_SKIP):
                self.distanceBuffer[j + i] = depth



        # color = int(((MAX_DEPTH - depth) / MAX_DEPTH) * 255)
        color = 170 // (1 + depth**2 * .1)
        line.fill = rgb(color, color, color)

        height = SCREEN_SIZE / (depth+.001)
        line.y1 = int((SCREEN_SIZE - height) // 2)
        line.y2 = int(SCREEN_SIZE - ((SCREEN_SIZE - height) // 2))
        
        line.dashes = (12, 2)

        line.visible = True





class Player:
    __slots__ = [
        "x",
        "y",
        "angle",
        "move_speed",
        "rotate_speed",
        "wand",
        "wand_lightning",
        "info_screen"
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.move_speed = .25
        self.rotate_speed = math.pi/30
        self.wand = Image("cmu://1067374/42545290/wand.png", 10, 270, width=140, height=140)
        self.wand_lightning = Image("cmu://1067374/42545545/wand_lightning.png", 130, 190, width=100, height=100, visible = False)
    
        self.info_screen = Group(
            Rect(65, 65, 400-65*2, 100, border="white"),
            Label("", 200, 65+50, fill="white", size=15, bold=True)
        )


    def write_info_text(self, text: str):
        info_label = self.info_screen.children[1]
        if info_label.value == "":
            label_writer(info_label, text)
        elif info_label.value != text:
            label_remover(info_label)
            label_writer(info_label, text)
            
    def hide_info_text(self):
        self.info_screen.visible = False

    def fire_wand(self, world: World) -> None:
        self.wand_lightning.visible = True
        

        angle = self.angle
        
        for depth in range(1, MAX_DEPTH*100):
            x = self.x + depth/PRECISION * math.cos(angle)
            y = self.y + depth/PRECISION * math.sin(angle)   
            
            if world.enemy_exists(x, y):
                world.delete_enemy(x, y)
                break
        
        
        sleep(.0000000001)
        self.wand_lightning.visible = False


    def move_forward(self, world: World) -> None:
        new_x = self.x + math.cos(self.angle) * self.move_speed
        new_y = self.y + math.sin(self.angle) * self.move_speed
        
        if not world.is_collision(int(new_x), int(new_y)):
            self.x = new_x
            self.y = new_y
    
    def move_backwards(self, world: World) -> None:
        new_x = self.x - math.cos(self.angle) * self.move_speed
        new_y = self.y - math.sin(self.angle) * self.move_speed

        if not world.is_collision(int(new_x), int(new_y)):
            self.x = new_x
            self.y = new_y

    def rotate_left(self) -> None:
        self.angle -= self.rotate_speed
        if self.angle < -2*math.pi:
            self.angle += 2*math.pi

    def rotate_right(self) -> None:
        self.angle += self.rotate_speed
            
        if self.angle > 2*math.pi:
            self.angle -= 2*math.pi

    def is_dead(self, world: World) -> bool:
        return world.enemy_exists(self.x, self.y)

    




class TutorialStage(Enum):
    NOT_STARTED = 0
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    SHOOT = 5
    FINISHED = 6
    



RENDERER = Renderer()
PLAYER = Player(3, 1.5)
WORLD = World([
            "##########",
            "#........#",
            "##########",
        ])

RENDERER.draw_entitys(PLAYER, WORLD)
POSITION_LABEL = Label("", 20, 10, fill="red")

TUTORIAL_STAGE = TutorialStage.NOT_STARTED
TIME = 0


def play_death_screen():
    Rect(0, 0, 400, 400)
    death_label = Label("", 200, 200, size=15, bold=True, fill="white")
    label_writer(death_label, "You have been attacked")
    label_remover(death_label)
    label_writer(death_label, "You have died")
    label_remover(death_label)
    label_writer(death_label, f"You survived for {TIME//app.stepsPerSecond} seconds")
    label_remover(death_label)
    label_writer(death_label, "Happy Halloween")
    app.stop()

def onStep():
    global TIME
    global TUTORIAL_STAGE
    global WORLD
    
    if PLAYER.is_dead(WORLD):
        play_death_screen()
    
    
    if TIME % app.stepsPerSecond == 0:
        WORLD.respawn_enemy()
    
    TIME += 1
    
    WORLD.pathfind_entities(PLAYER)
    RENDERER.refresh_frame()
    RENDERER.render_scene(PLAYER, WORLD)
    POSITION_LABEL.value = f"{rounded(PLAYER.x)} {rounded(PLAYER.y)}"

    if TUTORIAL_STAGE == TutorialStage.NOT_STARTED:
        PLAYER.write_info_text("Press W or UP to Move Forward")
        TUTORIAL_STAGE = TutorialStage.FORWARD
        
    if TUTORIAL_STAGE == TutorialStage.FORWARD and TIME >= app.stepsPerSecond*2:
        PLAYER.write_info_text("Press S or Down to Move Backwards")
        TUTORIAL_STAGE = TutorialStage.BACKWARD
        TIME = 0
        
    if TUTORIAL_STAGE == TutorialStage.BACKWARD and TIME >= app.stepsPerSecond*2:
        WORLD = World([
            "##########",
            "#........#",
            "#...##...#",
            "#........#",
            "##########",]
        )
        PLAYER.x = 3
        PLAYER.y = 3
        PLAYER.write_info_text("Press A or Left to Turn Left")
        TUTORIAL_STAGE = TutorialStage.LEFT
        TIME = 0
       
    if TUTORIAL_STAGE == TutorialStage.LEFT and TIME >= app.stepsPerSecond*2:
        PLAYER.write_info_text("Press D or Right to Turn Right")
        TUTORIAL_STAGE = TutorialStage.RIGHT
        TIME = 0 
        
    
    if TUTORIAL_STAGE == TutorialStage.RIGHT and TIME >= app.stepsPerSecond*2:
        PLAYER.write_info_text("Click or Press Space to Shoot")
        TUTORIAL_STAGE = TutorialStage.SHOOT
        TIME = 0
        
    
    if TUTORIAL_STAGE == TutorialStage.SHOOT and TIME >= app.stepsPerSecond*2:
        TUTORIAL_STAGE = TutorialStage.FINISHED
        PLAYER.hide_info_text()
        WORLD = World(world_map)
        PLAYER.x =27
        PLAYER.y=15
        PLAYER.angle = -2*math.pi + .1
        TIME = 0



def onMousePress(mouseX, mouseY):
    PLAYER.fire_wand(WORLD)



def onKeyHold(keys):
    
    if PLAYER.is_dead(WORLD):
        return
    
    if "up" in keys or "w" in keys:
        PLAYER.move_forward(WORLD)
        
    if "left" in keys or "a" in keys:
        PLAYER.rotate_left()

    if "right" in keys or "d" in keys:
        PLAYER.rotate_right()


    if "down" in keys or "s" in keys:
        PLAYER.move_backwards(WORLD)
        
    if "space" in keys:
        PLAYER.fire_wand(WORLD)
        
