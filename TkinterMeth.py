from math import sqrt

class draw:
    def __init__(self, can1, dimensions = [], positions = [], pion = []):
        self.can1 = can1
        self.positions = positions
        self.dimensions = dimensions
        self.pion = pion

    def circle(self,x, y, radius, col1 = '', col2 = ''):
        return self.can1.create_oval(x -radius, y - radius, x + radius, y + radius, outline = col1, fill = col2)

    def rectangle(self,x, y, longeur, largeur, col1 = '', col2 = ''):
        self.can1.create_rectangle(x + longeur, y + largeur, x, y, outline = col1, fill = col2)

    def select(self, x, y, radius):
        closest = []
        for i in self.positions:
            closest.append([abs(x - i[0]), abs(y - i[1])])
        try:
            target = closest.index(min(closest))
        except:
            print("There's nothing at this position.")
        else:
            if sqrt((x - self.positions[target][0])**2 + (y - self.positions[target][1])**2) > radius * 2:
                target = len(self.positions)
        return target

    def movecircle(self, lr, ud, radius, target):
        try:
            self.positions[target] = [self.positions[target][0] + lr, self.positions[target][1] + ud]
        except:
            print("There's nothing at this position")
        else:
            self.can1.coords(self.pion[target], self.positions[target][0] - radius, self.positions[target][1] - radius, self.positions[target][0] + radius, self.positions[target][1] + radius)
        
    def moverectangle(self, lr, ud, longueur, largeur, target, pion = []):
        try:
            self.positions[target] = [self.positions[target][0] + lr, self.positions[target][1] + ud]
        except:
            print("There's nothing at this position")
        else:
            self.can1.coords(self.pion[target], self.positions[target][0] + longueur, self.positions[target][1] + largeur, self.positions[target][0], self.positions[target][1])

class move:
    def __init__(self, canvas, coordone = [], objet = []):
        self.objet = objet
        self.canvas = canvas
        self.coordone = coordone

    def up(self, cible):
        self.coordone[cible][1] -= 1
        self.coordone[cible][3] -= 1
        self.canvas.coords(self.objet[cible], self.coordone[cible])

    def down(self, cible):
        self.coordone[cible][1] += 1
        self.coordone[cible][3] += 1
        self.canvas.coords(self.objet[cible], self.coordone[cible])

    def left(self, cible):
        self.coordone[cible][0] -= 1
        self.coordone[cible][2] -= 1
        self.canvas.coords(self.objet[cible], self.coordone[cible])

    def right(self, cible):
        self.coordone[cible][0] += 1
        self.coordone[cible][2] += 1
        self.canvas.coords(self.objet[cible], self.coordone[cible])