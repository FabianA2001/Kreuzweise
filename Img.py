from PIL import Image, ImageDraw, ImageFont
import random

class Img:
    def __init__(self, words:list[str]) -> None:
        print("init img")
        def createCartsDic() -> dict[str,bool]:
            carts = {}
            for nummer in "1234":
                for letter in "abcd":
                    carts[f"{letter}{nummer}"] = False
            return carts
        def createCarts(carts_draw:dict[str,bool]) -> list[str]:
            carts = []
            for letter,var in carts_draw.items():
                carts.append(letter)
            random.shuffle(carts)            
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
        self.drawCorner()
        self.carts_draw = createCartsDic()
        self.carts_iter = iter(createCarts(self.carts_draw))

        

    # def show(self):
    #     self.update()
    #     self.img.show()

    # def save(self,str:str):
    #     self.update()
    #     self.img.save(str)

    # def save(self,bit, str:str):
    #     self.update()
    #     self.img.save(bit, str)

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
        START = 500
        STEPS = 300
        it = iter(self.words) 
        for i in range(START,self.img.size[1],STEPS):
            self.draw_text_big((100,i,500,i + STEPS),next(it),35)
        for i in range(START,self.img.size[1],STEPS):
            self.draw_text_big((i,100,i+ STEPS,500),next(it),35)
    

    def drawCarts(self):
        ROWS = 4
        COLUMS = 4
        START = 590
        STEPS = 300
        
        it = iter(self.carts_draw.items())
        for x in range(0,COLUMS):
            for y in range(0,ROWS):
                letter, var = next(it)
                if var:
                    self.draw.text((START + x * STEPS,START + y * STEPS),letter,fill=self.fontColor, font=self.font,align="center")
    
    def drawCorner(self):
        self.draw.rectangle((0,0,500,500),fill="white")
        self.draw.multiline_text((30,20),f"Karten:\n{self.numCarts}\nVerkackt:\n{self.discard}",fill=self.fontColor, font=self.font,align="left")

    def update(self):
        self.drawCarts()
        self.drawCorner()

    def addCart(self, cart:str) -> bool:
        if cart not  in self.carts_draw.keys():
            return False
        self.carts_draw[cart] = True
        return True
    
    def reduceCarts(self) -> str:
        self.numCarts += -1
        return next(self.carts_iter)
        

    def addDiscard(self):
        self.discard += 1
    
    def draw_point_debugg(self,x,y):
        self.draw.line((0,y,self.img.width,y),fill="red")
        self.draw.line((x,0,x,self.img.height),fill="red") 

    def draw_text_big(self,box:tuple[int,int,int,int],text:str, padding:int = 0):
        font = self.font
        font_size = 10 
        font_path = font.path
        box_mid_with = (box[2] - box[0]) // 2 + box[0]
        box_mid_hight = (box[3] - box[1]) // 2 + box[1]

        font = ImageFont.truetype(font_path, font_size)
        while True:
            # Measure the text size
            textBox= self.draw.textbbox((box_mid_with,box_mid_hight),text,font,"mm")

            # If the text fits within the box, break
            if textBox[0] - padding < box[0]:
                break

            if textBox[1] - padding < box[1]:
                break

            if textBox[2] +padding > box[2]:
                break

            if textBox[3] +padding > box[3]:
                break

            # Reduce the font size and try again
            font_size += 1
            font = ImageFont.truetype(font_path, font_size)
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        self.draw.text((box_mid_with, box_mid_hight), text, font=font, fill=(0, 0, 0),anchor="mm")



if __name__ == "__main__":
    img = Img(["Haus","Pflanze","Ritter","See","Frau","Liebe","Essen","Apfelkuchen"])
    img.addCart("c4")
    img.addCart("b2")
    print(img.reduceCarts())
    img.addDiscard()
    # img.show()
    img.update()
    img.img.save("test.png")
