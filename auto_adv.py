from PIL import Image, ImageEnhance
import PIL.ImageOps
import pytesseract
import math
import pyautogui
import time
import sys 

def to_num(s):
    return int(''.join(c for c in s if c.isdigit()))

def has_numeric(arr):
    for i in arr:
        try:
            return to_num(i)
        except ValueError: 
            pass
    return -1

print("5 segundos pra vc botar o foco no jogo...(dê ctrl+C pra cancelar)")
time.sleep(5)

ids_antigos = {}

while True: # o pyautogui tem um failsafe embutido; pra parar o script, só jogar o mouse pra algum dos cantos da tela (monitor primário, se vc tiver mais de um)
    
    pyautogui.write('t/presos', interval=0.1)
    pyautogui.press('enter')
    time.sleep(5) # tempo de espera longo pra compensar possíveis lags por parte do servidor
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.moveTo(100, 150) # tirar o mouse da frente pra ele nao sair no print (mas nao pode por no canto senão ativa o failsafe do pyautogui)
    time.sleep(3)

    im = pyautogui.screenshot()
    w, h = im.size
    im = im.crop((1000, 0, 1458, h)) # vc deve querer mudar essa linha de acordo com o teu monitor (o meu é ultrawide, 2560x1080)
    im = PIL.ImageOps.invert(im.convert('RGB'))
    im = im.convert('LA')
    enhancer = ImageEnhance.Contrast(im)
    im_output = enhancer.enhance(4)
    im_output.save('asdasd.png')

    result = pytesseract.image_to_string(im_output, config='--psm 6')
    print(result)
    lines = result.split('\n')

    ids = {}

    for line in lines:
        fields = line.split(' ')
        has_num = has_numeric(fields)
        if has_num != -1:
            tempo = fields[-1].split(':')
            try:
                if len(tempo) == 2 and to_num(tempo[1]) < 60 and (to_num(tempo[0]) < 25 or (to_num(tempo[0]) == 25 and to_num(tempo[1]) == 0)):
                    price = math.ceil((to_num(tempo[0]) + (to_num(tempo[1]) / 60)) * 555)
                    if price < 500: price = 500
                    if price > 10000: price = 10000
                    ids[has_num] = price
            except ValueError: 
                pass
    if not ids: # failsafe importante em caso de lag
        print("Nenhum preso detectado; possivelmente o servidor lagou, o script bugou ou não tem nenhum preso mesmo; parando o script")
        sys.exit()
    
    ids_diff = {x:ids[x] for x in ids if x not in ids_antigos} # pra não soltar preso repetido (que não tem dinheiro etc)

    pyautogui.press('esc')
    for i, preco in ids_diff.items():
        comando = 't/soltar ' + str(i) + ' ' + str(preco)
        pyautogui.write(comando, interval=0.1)
        pyautogui.press('enter')
        caracteres = len(comando) - 1
        if (len(comando) - 1) < 20: time.sleep((26 - caracteres)/10)

    ids_antigos = ids
