from PIL import Image, ImageDraw, ImageFont

class Img:
    def __init__(self) -> None:
        def createCarts() -> dict[str,bool]:
            carts = {}
            for nummer in "1234":
                for letter in "abcd":
                    carts[f"{letter}{nummer}"] = False
            return carts
        self.img = Image.new("RGB", (1700,1700), color="white")
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype("Voice of Truth.ttf", 100)
        self.drawBackregister("black", 5)
        self.drawLetters("black", ["1","2","3","4","A","B","C","D"])
        self.carts = createCarts()

    def show(self):
        self.update()
        self.img.show()

    def drawBackregister(self, color, width):
        STEPS = 300
        START = 500
        MID = 100
        self.draw.line([(MID,START),(MID,self.img.size[1])], fill=color, width=width)
        self.draw.line([(START,MID),(self.img.size[0],MID)], fill=color, width=width)

        self.draw.line([(START,0),(START,self.img.size[1])], fill=color, width=width)
        for i in range(START,self.img.size[0],STEPS):
            self.draw.line([(i,0),(i,self.img.size[1])], fill=color, width=width)

        self.draw.line([(0,START),(self.img.size[0],START)], fill=color, width=width)
        for i in range(START,self.img.size[1],STEPS):
            self.draw.line([(0,i),(self.img.size[0],i)], fill=color, width=width)

    def drawLetters(self, color, letters:list[str]):
        assert(len(letters) == 8)
        START_H = 630
        START_V = 600
        STEPS = 300
        OFFSET_H =-12 
        OFFSET_V =25
        count = 0
        for i in range(START_H,self.img.size[1],STEPS):
            self.draw.text((i,OFFSET_H),letters[count],fill=color, font=self.font,align="center")
            count += 1
        for i in range(START_V,self.img.size[0],STEPS):
            self.draw.text((OFFSET_V,i),letters[count],fill=color, font=self.font,align="center")
            count += 1
    
    def drawCarts(self, color):
        ROWS = 4
        COLUMS = 4
        START = 590
        STEPS = 300
        
        it = iter(self.carts.items())
        for x in range(0,COLUMS):
            for y in range(0,ROWS):
                letter, var = next(it)
                if var:
                    self.draw.text((START + x * STEPS,START + y * STEPS),letter,fill=color, font=self.font,align="center")

    def update(self):
        self.drawCarts("black")

    def addCart(self, cart:str):
        assert(cart in self.carts.keys())
        self.carts[cart] = True




if __name__ == "__main__":
    img = Img()
    img.addCart("c4")
    img.addCart("b2")
    img.show()
