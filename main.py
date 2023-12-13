import pygame

pygame.init()
font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 30


class Striker:
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		self.Rect = pygame.Rect(posx, posy, width, height)
		self.rect = pygame.draw.rect(screen, self.color, self.Rect)

	def display(self):
		self.rect = pygame.draw.rect(screen, self.color, self.Rect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		if self.posy <= 0:
			self.posy = 0
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		self.Rect = (self.posx, self.posy, self.width, self.height)

	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	def getRect(self):
		return self.Rect


class Ball:
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.yFac = -1
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.yFac

		if self.posy <= 0 or self.posy >= HEIGHT:
			self.yFac *= -1

		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	def reset(self):
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1

	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.ball


def main():
	running = True

	player1 = Striker(20, 0, 10, 100, 10, WHITE)
	player2 = Striker(WIDTH-30, 0, 10, 100, 10, WHITE)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

	players = [player1, player2]

	p1s, p2s = 0, 0
	p1YF, p2YF = 0, 0

	while running:
		screen.fill(BLACK)

		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					p2YF = -1
				if event.key == pygame.K_DOWN:
					p2YF = 1
				if event.key == pygame.K_w:
					p1YF = -1
				if event.key == pygame.K_s:
					p1YF = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					p2YF = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					p1YF = 0

		for i in players:
			if pygame.Rect.colliderect(ball.getRect(), i.getRect()):
				ball.hit()

		player1.update(p1YF)
		player2.update(p2YF)
		point = ball.update()

		if point == -1:
			p1s += 1
		elif point == 1:
			p2s += 1

		if point:
			ball.reset()

		player1.display()
		player2.display()
		ball.display()

		player1.displayScore("Player1 : ", p1s, 100, 20, WHITE)
		player2.displayScore("Player2 : ", p2s, WIDTH-100, 20, WHITE)

		pygame.display.update()
		clock.tick(FPS)


if __name__ == "__main__":
	main()
	pygame.quit()
