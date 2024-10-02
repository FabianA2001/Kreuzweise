from PIL import Image, ImageDraw, ImageFont

class Img:
    def __init__(self, words:list[str]) -> None:
        def createCarts() -> dict[str,bool]:
            carts = {}
            for nummer in "1234":
                for letter in "abcd":
                    carts[f"{letter}{nummer}"] = False
            return carts
        assert(len(words) == 8)
        self.words = words
        self.img = Image.new("RGB", (1700,1700), color="white")
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype("Original Fish.otf", 100)
        self.discard = 0
        self.numCarts = 16
        self.fontColor = "black"
        self.drawBackregister("black", 5)
        self.drawLetters(["1","2","3","4","A","B","C","D"])
        self.drawWords()
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

    def drawLetters(self, letters:list[str]):
        assert(len(letters) == 8)
        START_H = 630
        START_V = 600
        STEPS = 300
        OFFSET_H =-12 
        OFFSET_V =25
        it = iter(letters) 
        for i in range(START_H,self.img.size[1],STEPS):
            self.draw.text((i,OFFSET_H),next(it),fill=self.fontColor, font=self.font,align="center")
        for i in range(START_V,self.img.size[0],STEPS):
            self.draw.text((OFFSET_V,i),next(it),fill=self.fontColor, font=self.font,align="center")

    def drawWords(self):
        START_H = 930
        START_V = 600
        STEPS = 300
        OFFSET_H =-12 
        OFFSET_V =25
        # it = iter(self.words) 
        # for i in range(START_H,self.img.size[1],STEPS):
        #     self.draw.text((i,OFFSET_H),next(it),fill=self.fontColor, font=self.font,align="center")
        # for i in range(START_V,self.img.size[0],STEPS):
        #     self.draw.text((OFFSET_V,i),next(it),fill=self.fontColor, font=self.font,align="center")
        self.drawBig(100,500,400,300,"Test")
    
    def drawCarts(self):
        ROWS = 4
        COLUMS = 4
        START = 590
        STEPS = 300
        
        it = iter(self.carts.items())
        for x in range(0,COLUMS):
            for y in range(0,ROWS):
                letter, var = next(it)
                if var:
                    self.draw.text((START + x * STEPS,START + y * STEPS),letter,fill=self.fontColor, font=self.font,align="center")
    
    def drawCorner(self):
        self.draw.multiline_text((30,20),f"Karten:\n{self.numCarts}\nVerkackt:\n{self.discard}",fill=self.fontColor, font=self.font,align="left")

    def update(self):
        self.drawCarts()
        self.drawCorner()

    def addCart(self, cart:str):
        assert(cart in self.carts.keys())
        self.carts[cart] = True
    
    def reduceCarts(self):
        self.numCarts += -1

    def addDiscard(self):
        self.discard += 1

    def drawBig(self,x:int,y:int,height:int,width:int, text:str):
        OFFSET = 20
        font_size = 10
        font = self.font
        box = (x+OFFSET, y + OFFSET, x+height-OFFSET, y+width-OFFSET)
        # self.draw.rectangle(box,fill="Black")
        while True:
            font = ImageFont.truetype(font.path,font_size)
            text_bbox = self.draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1] 
            if text_width > (box[2] - box[0]) or text_height > (box[3] - box[1]):
                break
            font_size += 1 

        font_size -= 1
        font = ImageFont.truetype(font.path,font_size)
        text_bbox = self.draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = box[0] + (box[2] - box[0] - text_width) // 2
        text_y = box[1] + (box[3] - box[1] - text_height) // 2
        self.draw.text((text_x, text_y), text, font=font, fill=self.fontColor) 


if __name__ == "__main__":
    img = Img(["Haus","Pflanze","Ritter","See","Frau","Liebe","Essen","Apfelkuchen"])
    img.addCart("c4")
    img.addCart("b2")
    img.reduceCarts()
    img.addDiscard()
    img.show()
