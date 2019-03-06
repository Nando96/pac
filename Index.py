import spritesheet


class Index:

    def __init__(self):
        ss = spritesheet.spritesheet('img/Pac.png')

        self.pacR = []
        self.pacR.append(ss.image_at((0, 0, 32, 32)))
        self.pacR.append(ss.image_at((0, 32, 32, 32)))
        self.pacR.append(ss.image_at((0, 32 * 2, 32, 32)))
        self.pacR.append(ss.image_at((0, 32 * 3, 32, 32)))
        self.pacU = []
        self.pacU.append(ss.image_at((0, 32 * 4, 32, 32)))
        self.pacU.append(ss.image_at((0, 32 * 5, 32, 32)))
        self.pacU.append(ss.image_at((0, 32 * 6, 32, 32)))
        self.pacU.append(ss.image_at((0, 32 * 7, 32, 32)))
        self.pacL = []
        self.pacL.append(ss.image_at((0, 32 * 19, 32, 32)))
        self.pacL.append(ss.image_at((0, 32 * 20, 32, 32)))
        self.pacL.append(ss.image_at((0, 32 * 14, 32, 32)))
        self.pacL.append(ss.image_at((0, 32 * 15, 32, 32)))
        self.pacD = []
        self.pacD.append(ss.image_at((0, 32 * 16, 32, 32)))
        self.pacD.append(ss.image_at((0, 32 * 17, 32, 32)))
        self.pacD.append(ss.image_at((0, 32 * 18, 32, 32)))
        self.pacD.append(ss.image_at((0, 32 * 19, 32, 32)))
        self.dead = []
        self.dead.append(ss.image_at((0, 32 * 20, 32, 32)))
        self.dead.append(ss.image_at((0, 32 * 21, 32, 32)))
        self.dead.append(ss.image_at((0, 32 * 22, 32, 32)))
        self.dead.append(ss.image_at((0, 32 * 23, 32, 32)))
        self.dead.append(ss.image_at((0, 32 * 24, 32, 32)))
        self.dead.append(ss.image_at((0, 32 * 25, 32, 32)))


