from PIL import Image
'293*190'
def pic_con(path):
        img = Image.open(path+'/code.png')
        
        #目标名称部分
        croping = img.crop((0,0,293,30))
        croping.save(path+'/0.png')

        #上半部图片
        croping = img.crop((0,38,293,110))
        croping.save(path+'/1.png')

        #下半部图片
        croping = img.crop((0,110,293,182))
        croping.save(path+'/2.png')

        #合并为新图片
        imagefile = []
        imagefile.append(Image.open(path+'/1.png'))
        imagefile.append(Image.open(path+'/2.png'))
        target = Image.new('RGB', (293 * 2, 72))
        target.paste(imagefile[0], (0, 0, 293, 72))
        target.paste(imagefile[1], (293, 0, 293*2, 72))
        target.save(path+'/new.jpg')

        img = Image.open(path+'/0.png') #293*30
        #剪裁拿到目标图片名称
        croping = img.crop((120,0,220,30))
        croping.save(path+'/3.png')
