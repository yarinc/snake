import pygame,snake,food,scoreboard
from operator import itemgetter
import os,json

class gameManager:
    playerColor = (0,0,0)
    textColor = (0,0,0)
    baseCoordinate = (0,0)
    gameOver = False
    clock = pygame.time.Clock()
    configFileLocation = "configs/configurations.json"
    replayGame = True

    #gameManager constructor
    def __init__(self):
        #load parameter file and assign value to variable
        print("Loading paramteres...")
        if os.path.exists(self.configFileLocation) and os.stat(self.configFileLocation).st_size > 0:
            file = open(self.configFileLocation, "r")
            try:
                configs = json.load(file)
                print("Configuration file loaded successfully.")
            except:
                raise Exception("Failed to load configuration file. Try to check for json formatting")
        else:
            raise Exception("Configuration file is empty or not found")
        try:
            self.screenHeight = configs["screenHeight"]
            self.screenWidth = configs["screenWidth"]
            self.snakeSpeed = configs["snakeSpeed"]
            self.itemsSize = configs["itemsSize"]
            self.showEvents = configs["showEvents"]
            self.foodPlayerImage = configs["foodPlayerImage"]
            self.foodSound =  configs["foodSound"]
            self.bgImage = configs["bgImage"]
            self.gameOverImage = configs["gameOverImage"]
            self.topScoresLocation = configs["topScoresLocation"]
            self.startGameImage = configs["startGameImage"]
            self.gameLeaderboardImage =  configs["gameLeaderboardImage"]
            self.goBackImage = configs["goBackImage"]
        except: 
            raise Exception("Failed to assign values.")
        #make sure screen size is a multiplication of itemSize to avoid strange locations in screen
        if self.screenHeight % self.itemsSize == 0 and self.screenWidth % self.itemsSize == 0:
            print("Sizes are ok.")
        else:
            raise Exception("screen sizes are not a muiltiplication of itemsSize")
        print("Paramters loaded succesfully. Initiating gameManager...")
        
        #Initiate game
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.dis = pygame.display.set_mode((self.screenWidth,self.screenHeight))
        pygame.display.update()
        pygame.display.set_caption("La Snake")

        #draw background
        self.bg = pygame.image.load(self.bgImage)
        self.bg = pygame.transform.scale(self.bg, (self.screenWidth, self.screenHeight))
        print("GameManager Loaded.") 
    #Method to control the game flow
    def play(self):
        while self.replayGame:
            self.preGame()
            self.gameLoop()
            self.endGame()
        pygame.quit()
        quit()
    #Method that handle the preGame phase
    def preGame(self):
        #initilize the begging of the game
        self.dis.blit(self.bg, self.baseCoordinate)
        self.playerName = ""
        playerNameLength = 8
        nameEntered = False
        
        #While loop to allow user input his name so we can save it for scoreboard feature
        while not nameEntered:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    print("Exiting program.")
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                            if(len(self.playerName) < playerNameLength):
                                self.playerName += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        self.playerName = self.playerName[:-1]
                    elif event.key == pygame.K_RETURN:
                        nameEntered = True
                elif event.type == pygame.QUIT:
                    exit()
            self.dis.blit(self.bg, self.baseCoordinate)

            #Draw the name on screen
            localFont = pygame.font.SysFont('Comic Sans MS', 26)
            nameTitle = localFont.render("Player name: ", True, self.textColor)
            self.dis.blit(nameTitle, (self.screenWidth / 7, self.screenHeight / 3 - nameTitle.get_height() / 2))
            nameBlock = localFont.render(self.playerName, True, self.textColor)
            self.dis.blit(nameBlock,(self.screenWidth / 7 + nameTitle.get_width(), self.screenHeight / 3 - nameTitle.get_height() / 2))
            pygame.display.flip()
        
        #At this point the user entered his name so we need to move to the startScreen
        self.drawStartScreen()
        gameStarted = False

        #Display a start game and leaderboard image so the user can select.
        #We leave this loop only when the user clicked start game to allow moving between start and leaderboard screens
        while not gameStarted:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    print("Exiting program.")
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.imageRect.collidepoint(event.pos):
                    gameStarted = True
                    self.imageRect = None
                elif event.type == pygame.MOUSEBUTTONDOWN and self.leaderboardRect.collidepoint(event.pos):
                    print("Showing leaderboard.")
                    self.imageRect = None
                    self.leaderboardRect = None
                    scoreFont = pygame.font.SysFont('Comic Sans MS', 22)
                    self.dis.blit(self.bg, self.baseCoordinate)
                    #Retrieve the top score and show only the top showEvent scores
                    scores = self.getTopScores()
                    if scores is not None:
                        sortedScores = sorted(scores, key=itemgetter('score'), reverse=True)[:self.showEvents]
                        index = 0
                        #Draw the scores accoring to the amount of lines so it's always in the middle of the screen
                        for score in sortedScores:
                            scoreText = scoreFont.render(f'{score["name"]}: {score["score"]}', True, self.textColor)
                            self.dis.blit(scoreText,(self.screenWidth / 2 - (scoreText.get_width() / 2) ,((self.screenHeight - (len(sortedScores) * scoreText.get_height())) / 2) + (index * scoreText.get_height())))
                            index += 1
                    #draw the back image
                    backImage = pygame.image.load(self.goBackImage).convert_alpha()
                    backImage = pygame.transform.scale(backImage, (50, 50))
                    self.dis.blit(backImage, ((self.screenWidth / 2 - (backImage.get_width() / 2) ,(self.screenHeight / 3) * 2.7 - (backImage.get_height() / 2))))
                    backRect = backImage.get_rect().move((self.screenWidth / 2 - (backImage.get_width() / 2) ,(self.screenHeight / 3) * 2.7 - (backImage.get_height() / 2)))
                    inMainScreen = False
                    #while loop to wait for the click to go back to main screen
                    while not inMainScreen:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN and backRect.collidepoint(event.pos):  
                                inMainScreen = True  
                                backRect = None         
                                self.drawStartScreen()
                            pygame.display.update()
                pygame.display.update()
    #Method to handle the game itself
    def gameLoop(self):
        #Load snake  and food position - Snake to the middle of the screen (considering itemSize) and food in a random location on screen
        self.mySnake = snake.Snake(self.playerColor, self.itemsSize * round((self.screenWidth / 2) / self.itemsSize), self.itemsSize * round((self.screenHeight / 2) / self.itemsSize), self.itemsSize,self.itemsSize)
        self.myFood = food.Food(self.foodPlayerImage,self.foodSound, self.itemsSize, self.itemsSize, self.screenWidth, self.screenHeight)
        self.validateFoodCooredinate()

        self.gameOver = False
        self.dis.blit(self.bg, self.baseCoordinate)
        self.clock = pygame.time.Clock()
        pause = False

        #While loop to wait for game to finish ()
        while not self.gameOver:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    print("Exiting program.")
                    exit()
                
                #Set new direction when the arrow keys pressed after validating the the snake can change direction
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:
                            if self.mySnake.canChangeDirection("left"):
                                self.mySnake.changeDirection("left")
                        case pygame.K_RIGHT:
                            if self.mySnake.canChangeDirection("right"):
                                self.mySnake.changeDirection("right")
                        case pygame.K_UP:
                            if self.mySnake.canChangeDirection("up"):
                                self.mySnake.changeDirection("up")
                        case pygame.K_DOWN:
                            if self.mySnake.canChangeDirection("down"):
                                self.mySnake.changeDirection("down")
                        #Set the pause flag to true/false when P is pressed
                        case pygame.K_p:
                            pause = not pause
            
            #Pause game feature - stop the snake till P is pressed again
            if(not pause):
                match self.mySnake.direction:
                    case "left":
                        self.mySnake.moveSnakeLeft()
                    case "right":
                        self.mySnake.moveSnakeRight()
                    case "up":
                        self.mySnake.moveSnakeUp()
                    case "down":
                        self.mySnake.moveSnakeDown()
                
                #Check if snake hitting his body and fail the game
                if self.mySnake.headInBody():
                    self.gameOver = True
                
                #Check if snake is out of game boundry and fail the game
                if self.mySnake.coordinates[0].x < 0 or self.mySnake.coordinates[0].x  == self.screenWidth or self.mySnake.coordinates[0].y < 0 or self.mySnake.coordinates[0].y == self.screenHeight:
                    print("Snake is out of bound.")
                    self.gameOver = True
                
                #Check if snake is hitting the food coordinate - generate a new food object, and expand the snake size.
                if self.mySnake.compareHeadCoordinate(self.myFood.coordinate):
                    sound = pygame.mixer.Sound(self.myFood.sound)
                    sound.set_volume(0.2)
                    sound.play()
                    self.myFood = food.Food(self.foodPlayerImage,self.foodSound,self.itemsSize,self.itemsSize,self.screenWidth,self.screenHeight)
                    self.validateFoodCooredinate()
                    self.mySnake.expandSnake()
                self.dis.blit(self.bg, self.baseCoordinate)
                
                #Draw the snake
                for coordinate in self.mySnake.coordinates:
                    pygame.draw.rect(self.dis, self.mySnake.color, [coordinate.x, coordinate.y, self.mySnake.xSize, self.mySnake.ySize])
                
                #Draw the food image to screen
                foodPlayer = pygame.image.load(self.myFood.image)
                foodPlayer = pygame.transform.scale(foodPlayer, (self.myFood.xSize, self.myFood.ySize))
                self.dis.blit(foodPlayer, (self.myFood.coordinate.x, self.myFood.coordinate.y))
                pygame.display.update()
                
                #Control snake speed
                self.clock.tick(self.snakeSpeed)
    #Method to handle the end game phase
    def endGame(self):
        #Draw the end game image
        gameOver = pygame.image.load(self.gameOverImage).convert_alpha()
        gameOver = pygame.transform.scale(gameOver, (self.screenWidth / 2, self.screenHeight / 2))
        self.dis.blit(gameOver, (self.screenWidth / 2 - (gameOver.get_width() / 2) ,self.screenHeight / 3 - (gameOver.get_height() / 2)))
        
        #Draw the score on screen
        scoreText = self.font.render(f'Score: {len(self.mySnake.coordinates) - 1}', True, self.textColor)
        self.dis.blit(scoreText,(self.screenWidth / 2 - (scoreText.get_width() / 2) ,(self.screenHeight / 3) * 2 - (scoreText.get_height() / 2)))
        
        #Draw the replay instructions on screen
        replayText = pygame.font.SysFont('Comic Sans MS', 16)
        replayText = replayText.render("Press R to replay or E to exit", True, self.textColor)
        self.dis.blit(replayText,(self.screenWidth / 2 - (replayText.get_width() / 2) ,(self.screenHeight * 0.9)))
        
        pygame.display.update()

        #Write the score in the configured location
        scores = scoreboard.scoreboard(self.topScoresLocation)
        scores.writeScore(self.playerName, len(self.mySnake.coordinates) - 1)
        
        #Wait for a key to be pressed before exiting
        keyPressed = False
        while not keyPressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print("Replaying game.")
                        keyPressed = True
                    elif event.key == pygame.K_e:
                        print("Exiting game")
                        keyPressed = True
                        self.replayGame = False
    #Method to load the top scores
    def getTopScores(self) -> dict:
        self.topScores = scoreboard.scoreboard(self.topScoresLocation)
        return self.topScores.loadScores()
    #Method to draw the start screen
    def drawStartScreen(self): 

        self.dis.blit(self.bg, self.baseCoordinate)

        #Drawing the start icon in a 100x100 resolution
        startImage = pygame.image.load(self.startGameImage).convert_alpha()
        startImage = pygame.transform.scale(startImage, (100, 100))
        self.dis.blit(startImage, ((self.screenWidth / 2 - (startImage.get_width() / 2) ,self.screenHeight / 2 - (startImage.get_height() / 2))))
        self.imageRect = startImage.get_rect().move((self.screenWidth / 2 - (startImage.get_width() / 2) ,self.screenHeight / 2 - (startImage.get_height() / 2)))

        #Drawing the leaderboard icon in a 100x100 resolution
        leaderboardImage = pygame.image.load(self.gameLeaderboardImage).convert_alpha()
        leaderboardImage = pygame.transform.scale(leaderboardImage, (100, 100))
        self.dis.blit(leaderboardImage, ((self.screenWidth / 2 - (leaderboardImage.get_width() / 2) ,(self.screenHeight / 3) * 2.25- (leaderboardImage.get_height() / 2))))
        self.leaderboardRect = leaderboardImage.get_rect().move((self.screenWidth / 2 - (leaderboardImage.get_width() / 2) ,(self.screenHeight / 3) * 2.25  - (leaderboardImage.get_height() / 2)))

        pygame.display.update()
    #Method to validate the food isn't spawn over the snake itself.
    #This will generate a new food object till it's fixed
    def validateFoodCooredinate(self):
        foodIsValid = False
        while not foodIsValid:
            for item in self.mySnake.coordinates:
                if self.myFood.coordinate.compare(item):
                    print("Food spwand on snake. generating new one.")
                    self.myFood = food.Food(self.foodPlayerImage,self.foodSound,self.itemsSize,self.itemsSize,self.screenWidth,self.screenHeight)
                    break
            foodIsValid = True