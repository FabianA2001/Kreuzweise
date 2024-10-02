# from Img import Img

# if __name__ == "__main__":
#     img = Img(["Haus","Pflanze","Ritter","See","Frau","Liebe","Essen","Apfelkuchen"])
#     img.show()


from PIL import Image, ImageDraw, ImageFont

# Erstellen eines neuen Bildes
img_width, img_height = 800, 600
image = Image.new('RGB', (img_width, img_height), color='white')
draw = ImageDraw.Draw(image)

# Bereich, in dem der Text eingefügt werden soll
box = (50, 50, 700, 350)
draw.rectangle(box,outline="black",width=10)
# Text und initiale Schriftgröße
text = "test"
font_path = "Original Fish.otf"  # Pfad zur Schriftartdatei
font_size = 10  # Start mit kleiner Schriftgröße

# Schriftgröße dynamisch anpassen
while True:
    font = ImageFont.truetype(font_path, font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    if text_width > (box[2] - box[0]) or text_height > (box[3] - box[1]):
        break
    font_size += 1

# Den Text mittig im Bereich platzieren
font_size -= 1  # Eine Größe zurückgehen, damit es passt
font = ImageFont.truetype(font_path, font_size)
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
text_x = box[0] + (box[2] - box[0] - text_width) // 2
text_y = box[1] + (box[3] - box[1] - text_height) // 2

# Text zeichnen
draw.text((text_x, text_y), text, font=font, fill="black")

# Bild speichern oder anzeigen
image.show()  # Zeigt das Bild an
# image.save("output.png")  # Speichert das Bild

