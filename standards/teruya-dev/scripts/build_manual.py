"""Render the teruya.dev visual manual using local San Francisco / SF Pro optical instances."""
from pathlib import Path
import json
import math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/teruya-dev-manual-visual.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
TOK=json.loads((ROOT/'tokens.json').read_text())
COL=TOK['color']; W,H=595.276,841.89; M=44; CW=W-2*M
from sf_pro_fonts import register_sf_pro, font_name
FONT_BUILD=register_sf_pro()
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1,initialFontName='SFText400')
c.setTitle('teruya.dev | Manual visual de vídeo 3.0')
c.setAuthor('teruya.dev')
c.setSubject('Identidade, kinetic typography, liquid motion e receitas ShotCraft para TikToks narrados')
page=0
DARK=False

def color(v):return HexColor(COL.get(v,v))
def ink(v):
    if DARK:v={'ink':'white','muted':'mutedOnDark','blue':'blueOnDark','line':'#48484A'}.get(v,v)
    return color(v)
def surface(v):
    if DARK:v={'white':'dark2','canvas':'dark3','surface':'dark2','line':'#48484A'}.get(v,v)
    return color(v)
def rect(x,y,w,h,fill='white',stroke=None,r=0,lw=1):
    c.setFillColor(surface(fill));c.setStrokeColor(surface(stroke or fill));c.setLineWidth(lw)
    if r:c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=int(stroke is not None))
    else:c.rect(x,H-y-h,w,h,fill=1,stroke=int(stroke is not None))
def line(x1,y1,x2,y2,col='line',lw=1):
    c.setStrokeColor(ink(col));c.setLineWidth(lw);c.line(x1,H-y1,x2,H-y2)
def text(s,x,y,size=11,weight=400,col='ink',align='left'):
    s=s.replace('–','-').replace('—','-')
    weight=600 if weight>=500 else 400
    tracking=-.01*size if size>=19 else 0
    width=pdfmetrics.stringWidth(s,font_name(size,weight),size)+max(0,len(s)-1)*tracking
    xx=x-width if align=='right' else x-width/2 if align=='center' else x
    obj=c.beginText(xx,H-y-size*.82);obj.setFont(font_name(size,weight),size);obj.setFillColor(ink(col));obj.setCharSpace(tracking);obj.textOut(s);c.drawText(obj)
def outlined_text(s,x,y,size=36,fg='blue',stroke=None,align='left'):
    """Two concentric glyph rings, then original fill. No offset or text backing."""
    width=pdfmetrics.stringWidth(s,font_name(size,600),size)
    xx=x-width/2 if align=='center' else x-width if align=='right' else x
    inner=stroke or ('white' if DARK else 'black')
    outer='black' if inner=='white' else 'white'
    # Editorial PDF sizes use a quarter-scale equivalent of the video ring bounds.
    a=max(.5,min(size*.035,1.5));b=max(.25,min(size*.0175,.75))
    c.saveState();c.setLineJoin(1)
    for col,lw in [(outer,2*(a+b)),(inner,2*a)]:
        c.setStrokeColor(color(col));c.setLineWidth(lw)
        obj=c.beginText(xx,H-y-size*.82);obj.setFont(font_name(size,600),size)
        obj.setTextRenderMode(1);obj.textOut(s);obj.setTextRenderMode(0)
        c.drawText(obj)
    obj=c.beginText(xx,H-y-size*.82);obj.setFont(font_name(size,600),size)
    obj.setFillColor(ink(fg));obj.setTextRenderMode(0);obj.textOut(s);c.drawText(obj)
    c.restoreState()
def para(s,x,y,w,size=11,leading=None,col='ink',weight=400):
    s=s.replace('–','-').replace('—','-')
    weight=600 if weight>=500 else 400
    st=ParagraphStyle('p',fontName=font_name(size,weight),fontSize=size,leading=leading or size*1.44,textColor=ink(col),spaceAfter=0)
    p=Paragraph(s,st);aw,ah=p.wrap(w,1000)
    if y+ah>778:raise ValueError(f'Overflow page {page}: {y+ah}: {s[:80]}')
    p.drawOn(c,x,H-y-ah);return ah
def label(s,x,y,col='muted'):text(s.upper(),x,y,8.5,600,col)
def rule(y):line(M,y,W-M,y)
def pill(s,x,y,w,h=28,fill='blue',fg='white',size=11):
    rect(x,y,w,h,fill,r=h/2);text(s,x+w/2,y+(h-size)/2-.5,size,600,fg,'center')
def arrow(x1,y1,x2,y2,col='blue',lw=1.5):
    line(x1,y1,x2,y2,col,lw);a=math.atan2(y2-y1,x2-x1)
    for offset in [-.55,.55]:line(x2,y2,x2-6*math.cos(a+offset),y2-6*math.sin(a+offset),col,lw)
def header(kicker,title,sub=''):
    global page,DARK
    if page:c.showPage()
    page+=1;DARK=page in TOK['manual']['darkPages'];rect(0,0,W,H,'dark' if DARK else 'canvas' if page in [2,6,11] else 'white')
    label(kicker,M,35);text('teruya.dev',W-M,35,9,600,'ink','right')
    title_size=min(29,29*CW/max(CW,pdfmetrics.stringWidth(title,font_name(29,600),29)))
    text(title,M,68,title_size,700)
    if sub:para(sub,M,112,CW,11,col='muted')
def footer():
    text('PADRÃO DE VÍDEO  /  3.0  /  30.10.2026',M,808,7.5,400,'muted')
    text(f'{page:02d} / {TOK["manual"]["pageCount"]:02d}',W-M,808,8,600,'muted','right')
def note(s,y,fill='surface'):
    rect(M,y,CW,55,fill,r=13.5);para(s,M+16,y+12,CW-32,10.2,14.7)
def sketch_grid(x,y,w,h,dark=None,scale=None):
    spec=TOK['explanationBackground'];dark=DARK if dark is None else dark
    theme=spec['dark' if dark else 'light'];scale=w/1080 if scale is None else scale
    step=spec['spacingPx']*scale
    c.saveState()
    clip=c.beginPath();clip.rect(x,H-y-h,w,h);c.clipPath(clip,stroke=0,fill=0)
    c.setStrokeColor(color(theme['stroke']));c.setStrokeAlpha(theme['opacity']);c.setLineWidth(spec['lineWidthPx']*scale)
    xx=x+step
    while xx<x+w:
        c.line(xx,H-y,xx,H-y-h);xx+=step
    yy=y+step
    while yy<y+h:
        c.line(x,H-yy,x+w,H-yy);yy+=step
    c.restoreState()
def mini_phone(x,y,w=147,h=261,bg='canvas',grid=True,grid_scale=1):
    rect(x,y,w,h,bg,r=0)
    if grid:sketch_grid(x,y,w,h,scale=w/1080*grid_scale)
    return x,y,w,h
def chip(s,x,y,w,h=35,active=False,size=11):
    rect(x,y,w,h,'blue' if active else 'canvas',r=6)
    text(s,x+w/2,y+(h-size)/2,size,600,'white' if active else 'ink','center')
def graph(x,y,w,focus='model',scale=1):
    # Normalized vector keyframe, deliberately simplified for documentation.
    rect(x,y,w,w*.88,'white','line',13.5,lw=.75)
    text('HARNESS',x+12,y+12,9,700,'blue' if focus=='harness' else 'muted')
    chip('MODELO',x+w*.18,y+w*.26,w*.64,w*.25,focus=='model',max(8,w*.085))
    yy=y+w*.65
    line(x+w*.5,y+w*.51,x+w*.5,yy-5,'blue',1.5)
    for xp,lab in [(x+w*.08,'tools'),(x+w*.54,'contexto')]:
        chip(lab,xp,yy,w*.38,w*.16,focus==lab,max(6,w*.055))
def row_title(n,title,y,body,height=103):
    text(n,M,y,22,700,'blue');text(title,M+42,y+2,16,700)
    para(body,M+42,y+31,CW-42,10.6,15)
    if height:rule(y+height)
def link(s,url,x,y,size=9):
    text(s,x,y,size,600,'blue')
    ww=pdfmetrics.stringWidth(s,font_name(size,600),size)
    c.linkURL(url,(x,H-y-size*1.35,x+ww,H-y+2),relative=0,thickness=0)

# 01 Cover: a visual identity built from words becoming components.
header('MANUAL VISUAL','')
text('teruya.dev',W/2,128,26,600,'ink','center')
text('A fala',W/2,207,48,600,'ink','center')
text('vira imagem.',W/2,258,48,600,'ink','center')
text('Voz, tipografia e movimento.',W/2,335,16,400,'muted','center')
rect(0,399,W,285,'canvas')
sketch_grid(0,399,W,285)
outlined_text('modelo',M+27,510,35)
arrow(M+178,533,M+237,533)
graph(M+270,454,174)
text('A palavra ganha forma. A ideia continua.',W/2,723,13,400,'muted','center')
text('Design editorial  /  versão 3.0',W/2,753,9,400,'muted','center')
footer()

# 02 Palette and typography.
header('01  /  DESIGN SYSTEM','Uma família de azul.','Branco, cinzas neutros e blocos escuros. A cor conduz o olhar com discrição.')
sw=[('blue','Foco'),('ink','Texto'),('white','Base')]
for i,(key,role) in enumerate(sw):
    x=M+i*174
    rect(x,171,159,116,key,'line' if key=='white' else None,13.5,lw=.75)
    text(role,x+13,187,11,600,'white' if key in ['blue','ink'] else 'ink')
    text(COL[key],x+13,259,12,700,'white' if key in ['blue','ink'] else 'ink')
for i,(key,role) in enumerate([('canvas','Fundo suave'),('dark','Bloco escuro'),('blueOnDark','Azul no escuro'),('line','Hairline')]):
    x=M+i*130
    rect(x,307,117,38,key,'line' if key=='canvas' else None,r=6,lw=.75)
    text(role,x,354,9,600);text(COL[key],x,370,8,400,'muted')
rule(401)
label('SAN FRANCISCO · SF PRO DISPLAY / TEXT',M,424)
text('Mesmo modelo.',M,450,38,800)
outlined_text('Outro contexto.',M,497,38)
para('SF Pro Display em títulos e ênfases; SF Pro Text em legendas, rótulos e corpo. Semibold 600 e Regular 400. Tracking inicial de -0,01 em nos títulos. Fonte local do macOS incorporada neste PDF.',M,559,CW,11,16)
rows=[('Hero','144–176 px','1–3 palavras'),('Título','96–120 px','até 6 palavras'),('Rótulo','48–64 px','conceito curto'),('Legenda','60–68 px','até 2 linhas')]
for i,(a,b,d) in enumerate(rows):
    yy=626+i*29
    text(a,M,yy,10.5,600);text(b,M+135,yy,10.5);text(d,M+302,yy,10.5,400,'muted')
text('Tamanhos na tela 1080 × 1920. Texto essencial: mínimo inicial de 40 px.',M,757,9,400,'muted')
footer()

# 03 Composition and safe regions.
header('02  /  COMPOSIÇÃO VERTICAL','O espaço também explica.','Um foco principal. Poucos componentes. Tempo para o olhar encontrar cada relação.')
px,py,pw,ph=mini_phone(M,166,245,436,grid=False)
s=pw/1080
rect(px+96*s,py+200*s,804*s,1320*s,'white','blue',5)
rect(px+96*s,py+240*s,804*s,1020*s,'canvas',r=4)
sketch_grid(px+96*s,py+240*s,804*s,1020*s,scale=s)
rect(px+96*s,py+1340*s,804*s,180*s,'surface',r=4)
text('PALCO',px+115*s,py+275*s,8,700,'muted')
graph(px+200*s,py+540*s,600*s)
text('A voz guia a explicação.',px+498*s,py+1400*s,9,600,'ink','center')
for yy in [750,930,1110]:
    c.setFillColor(color('line'));c.circle(px+990*s,H-(py+yy*s),9,fill=1,stroke=0)
text('Interface',px+920*s,py+1280*s,6,400,'muted')
text('1080 × 1920  /  30 fps',px+pw/2,py+ph+13,10,600,'ink','center')
rx=M+277;rw=CW-277
label('ÁREA INTERNA',rx,173)
para('x 96…900<br/>y 200…1520',rx,196,rw,14,21,weight=600)
label('PALCO DE EXPLICAÇÃO',rx,266)
para('y 240…1260<br/>Componentes, títulos e imagens.',rx,289,rw,11,16)
label('LEGENDA',rx,362)
para('y 1340…1520<br/>Sempre em coordenadas da tela, fora do zoom.',rx,385,rw,11,16)
label('GEOMETRIA',rx,472)
para('Base web: 8 px → vídeo: 24 px.<br/>Raios web: 8 / 11 / 18 px.<br/>Vídeo: 24 / 33 / 54 px.<br/>Blocos de ponta a ponta: 0.<br/>Pílulas: metade da altura.',rx,495,rw,10.4,17)
note('Guias conservadoras do projeto. Conferir a interface atual do TikTok e o arquivo final no celular antes de publicar.',646)
para('No primeiro olhar: uma ideia. Na sequência: uma relação. Se tudo pede atenção ao mesmo tempo, reduzir elementos ou revelar o grupo em etapas.',M,726,CW,12,18,weight=600)
footer()

# Explanation canvas: visibly spacious, translucent and subordinate to the diagram.
header('03  /  SKETCHBOOK','Um espaço para explicar.','Uma malha larga e translúcida cria o clima de raciocínio visual.')
for i,is_dark in enumerate([False,True]):
    x=M+i*280
    text('ESCURO / 6%' if is_dark else 'CLARO / 7%',x,168,9,600,'muted')
    DARK=is_dark
    mini_phone(x,193,207,368,'dark' if is_dark else 'canvas')
    text('O mesmo',x+19,225,14,600)
    outlined_text('modelo.',x+19,245,23)
    graph(x+35,313,137,'harness')
    text('A estrutura organiza.',x+103.5,510,9,600,'ink','center')
    DARK=False
label('GRID QUADRADO',M,594)
text('216 px entre linhas',M,619,16,600)
text('Traço de 1,5 px',W-M,619,16,600,'ink','right')
para('Aplicar nas explicações, comparações e diagramas. Fundo, grid e apoios ficam discretos; a atenção vai para palavras, componentes e suas relações.',M,655,CW,11,16)
note('O grid não pulsa nem deriva. Quando a câmera se move, ele acompanha o plano do diagrama. Rostos, imagens e cartelas podem usar fundo liso.',716)
footer()

# 04 Text roles and synchronization.
header('04  /  KINETIC TYPOGRAPHY','Três funções para o texto.','A legenda informa. A palavra enfatiza. O termo se transforma em objeto.')
for i,(title,body) in enumerate([
    ('01  Legenda de apoio','Toda a fala, em blocos de sentido. Sobre o apresentador: texto flutuante, sem fundo. Contorno duplo: branco interno/preto externo no escuro; ordem inversa no claro.'),
    ('02  Palavra em destaque','Cada letra da palavra de ênfase tem Elastic Pop-In e Pop-Out próprios. Contorno acompanha o glifo; a palavra assenta para leitura.'),
    ('03  Texto vira componente','O termo diminui, muda de posição e passa a identificar o elemento que seguirá na cena.')]):
    y=166+i*164
    rect(M,y,180,140,'canvas',r=13.5)
    text(title,M+201,y+4,14,700)
    para(body,M+201,y+34,CW-201,11,16)
    if i==0:
        text('O mesmo',M+18,y+47,14,600)
        outlined_text('modelo',M+92,y+47,14)
        text('pode mudar.',M+18,y+87,14,600)
    elif i==1:
        text('mesmo',M+18,y+27,17,600,'muted')
        outlined_text('modelo',M+17,y+62,35)
        line(M+20,y+108,M+152,y+108,'blue',3)
    else:
        text('MODELO',M+20,y+17,23,700,'blue')
        arrow(M+90,y+51,M+90,y+75)
        chip('MODELO',M+40,y+88,100,32,True,12)
label('A PALAVRA É O MARCADOR',M,684)
para('Entrada de 0–2 frames antes da palavra. Revisar sincronia em até 3 frames. Usar os tempos reais do áudio; nunca espaçar todas as palavras igualmente.',M,709,CW,11,16)
text('Sobre o rosto: títulos, legendas e CTA sem placas, faixas, chips ou blur de fundo.',M,761,8.5,400,'muted')
footer()

# 05 Liquid and timing.
header('05  /  MOTION SYSTEM','Design clean. Movimento vivo.','A energia vem da coreografia: texto, componentes e câmera conduzem a explicação.')
rect(0,168,W,145,'white')
chip_bounds=[]
for center,lab in [(M+84,'modelo'),(M+254,'contexto'),(M+424,'ferramentas')]:
    width=pdfmetrics.stringWidth(lab,font_name(13,600),13)+30
    pill(lab,center-width/2,212,width,42,size=13)
    chip_bounds.append((center-width/2,center+width/2))
for i in range(2):arrow(chip_bounds[i][1]+12,233,chip_bounds[i+1][0]-12,233)
text('A largura acompanha a palavra. As letras não esticam.',M+22,279,10.5,600,'muted')
label('CICLO DO COMPONENTE',M,338)
segments=[('ENTRA','16–24 f',.21),('AGE','pela fala',.27),('PERMITE LER','≥18–30 f',.34),('TRANSFORMA','20–28 f',.18)]
xx=M
for i,(a,b,frac) in enumerate(segments):
    wid=CW*frac
    rect(xx,365,wid-3,58,'blue' if i==1 else 'surface',r=6)
    text(a,xx+9,378,8,700,'white' if i==1 else 'ink')
    text(b,xx+9,397,9,600,'white' if i==1 else 'muted');xx+=wid

# Parametric cubic curves drawn as editorial figures, matching the spec.
def curve_plot(x,y,w,h,points,title,detail):
    label(title,x,y)
    gy=y+29
    line(x,gy+h,x+w,gy+h);line(x,gy,x,gy+h)
    a,b,d,e=points
    path=c.beginPath();path.moveTo(x,H-(gy+h))
    for i in range(1,61):
        t=i/60;xx=3*(1-t)**2*t*a+3*(1-t)*t*t*d+t**3;yy=3*(1-t)**2*t*b+3*(1-t)*t*t*e+t**3
        path.lineTo(x+xx*w,H-(gy+h-yy*h))
    c.setStrokeColor(color('blue'));c.setLineWidth(2.2);c.drawPath(path)
    text(detail,x,y+h+42,8.5,400,'muted')
curve_plot(M,457,218,85,[.22,1,.36,1],'OPACIDADE / APOIO','.22, 1, .36, 1')
curve_plot(M+289,457,218,85,[.6,0,.18,1],'REORGANIZAÇÃO','.6, 0, .18, 1')
para('A cada ideia, uma ação perceptível: a palavra entra, a peça se conecta, o diagrama muda ou a câmera revela uma relação. Variar a coreografia e assentar para leitura. Apoios mantêm pop discreto: 1,5% em texto e 3% em objetos. Ênfase por letra usa elastic com picos de 8% na entrada e 6% na saída.',M,621,CW,11,16)
note('Os tempos acima são presets próprios teruya.dev. Receitas ShotCraft mantêm seus parâmetros essenciais ou registram claramente a adaptação.',710)
footer()

# 06 Bubble-pop lifecycle.
header('06  /  BOLHA POP','Aparecer também é explicar.','Todo elemento que chama atenção tem entrada, leitura e saída fluidas.')
rect(0,172,W,248,'canvas')
states=[('01  EXPANDE','0,88×',.88),('02  ASSENTA','1,025× → 1×',1.025),('03  PERMITE LER','1×',1),('04  RECOLHE','1× → 0,92×',.92)]
for i,(name,sc,ratio) in enumerate(states):
    cx=M+58+i*130
    sz=84*ratio
    alpha=[.72,1,1,.35][i]
    def matte(fg):
        a=color(fg);b=color('canvas')
        return '#'+''.join(f'{round((u*alpha+v*(1-alpha))*255):02x}' for u,v in zip((a.red,a.green,a.blue),(b.red,b.green,b.blue)))
    rect(cx-sz/2,240+(84-sz)/2,sz,sz,matte('blue'),r=13.5*ratio)
    text('Aa',cx,282-25*ratio/2,25*ratio,600,matte('white'),'center')
    text(name,cx,194,7.7,600,'muted','center')
    text(sc,cx,350,10.3,600,'ink','center')
    if i<3:arrow(cx+49,283,cx+78,283)
text('Quadros-chave de referência. Escala uniforme; a forma e as letras não deformam.',M,439,9,400,'muted')
rows=[('Entrada','18 frames','Escala 0,88 → 1,025 → 1. Opacidade chega em 4 frames.'),('Leitura','pela fala','O objeto assenta e permanece nítido; não fica pulsando.'),('Saída','10 frames','Escala 1 → 0,92. Opacidade sai nos últimos 5 frames.')]
for i,(a,b,d) in enumerate(rows):
    yy=491+i*66
    text(a,M,yy,13,600);text(b,W-M,yy,11,600,'blue','right')
    text(d,M,yy+25,10.5);rule(yy+50)
note('Fundos e apoios podem permanecer estáticos. O elemento focal assenta para leitura e sai ou se transforma; a base não precisa desaparecer.',716)
footer()

# 07 Origins and variants, not a universal vertical reveal.
header('07  /  ORIGEM E DIREÇÃO','O pop nasce da relação.','Centro, lateral, diagonal ou conexão: escolher a origem pelo significado da cena.')
for i,(a,b) in enumerate([('Centro','O conceito aparece no lugar.'),('Conexão','A peça emerge do seu pai.'),('Substituição','Uma forma continua na outra.')]):
    x=M+i*174
    rect(x,174,159,178,'canvas',r=13.5)
    text(a,x+16,191,12,600)
    if i==0:
        rect(x+55,247,49,49,'blue',r=6)
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:arrow(x+79.5+dx*29,271.5+dy*29,x+79.5+dx*40,271.5+dy*40)
    elif i==1:
        rect(x+22,245,32,32,'white','line',6)
        arrow(x+59,265,x+100,282)
        rect(x+108,270,30,30,'blue',r=6)
    else:
        pill('A',x+16,257,44,30,size=12)
        arrow(x+67,272,x+88,272)
        pill('AB',x+96,252,48,40,size=12)
    para(b,x+12,366,153,9.8,14)
presets=[('Centro','0,88 → 1,025 → 1','18 f / saída 10 f'),('Da conexão','0,86 → 1,03 → 1','20 f / saída 12–20 f'),('Texto de apoio','0,94 → 1,015 → 1','10 f / saída 8 f'),('Substituir','Largura + troca de termo','20–28 f / morph'),('No enquadramento','0,96 → 1,01 → 1','18 f / saída 10–14 f')]
for i,(name,sc,timing) in enumerate(presets):
    yy=428+i*38
    text(name,M,yy,10.5,600);text(sc,M+135,yy,10);text(timing,W-M,yy,10,400,'muted','right')
    if i<4:rule(yy+26)
para('Objeto já visível: animar a camada de foco. Encerrar o destaque pode manter o objeto base estático no diagrama.',M,618,CW,9.5,13)
rect(M,647,CW,124,'canvas',r=13.5)
text('Referência de sensação, não de trajetória fixa.',M+16,664,13,600)
para('O componente enviado usa spring 190 / 22 e reveal vertical. Aproveitar o assentamento; acrescentar escala, saída e origem. Trocar o stagger fixo de 0,2 s pelos tempos da fala. Evitar aleatoriedade a cada render.',M+16,695,CW-32,10.5,15)
footer()

# 08 Camera.
header('08  /  CÂMERA','Aproximar. Explicar. Relacionar.','O zoom tem um alvo. O zoom out devolve o contexto.')
xs=[M,M+178,M+356]
for i,x in enumerate(xs):
    mini_phone(x,174,151,269,grid_scale=1.25 if i==1 else 1)
    label(['01  CONJUNTO','02  DETALHE','03  RELAÇÃO'][i],x+12,192)
    if i!=1:graph(x+20,237,111,'harness' if i==2 else 'model')
    else:
        text('CONTEXTO',x+15,252,16,700,'blue')
        for j,lab in enumerate(['instruções','arquivos','histórico']):chip(lab,x+15,291+j*32,121,26,j==0,10)
    text(['O mesmo modelo','O ambiente organiza','O conjunto influencia'][i],x+75.5,402,8.2,600,'ink','center')
    text(['1,00×','1,25×','1,00×'][i],x+75.5,461,14,700,'blue','center')
arrow(M+154,310,M+174,310);arrow(M+332,310,M+352,310)
rows=[('Entrar no detalhe','18–30 f','Centro e escala usam a mesma curva.'),('Ler o detalhe','pela fala','A câmera repousa enquanto se explica.'),('Voltar ao conjunto','24–36 f','Recuperar a relação entre os elementos.')]
for i,(a,b,d) in enumerate(rows):
    yy=512+i*64
    text(a,M,yy,12,600);text(b,W-M,yy,12,700,'blue','right')
    text(d,M,yy+24,10.5,400,'muted');rule(yy+48)
para('Legendas ficam fixas na tela. Câmera preenche o painel por recorte proporcional, priorizando o rosto. Nunca completar laterais com blur; ajustar recorte ou painel.',M,725,CW,11,16)
footer()

# 07 Typographic ShotCraft recipe cards.
header('09  /  SHOTCRAFT · TEXTO','Receitas com identidade.','O look muda para teruya.dev. A lógica do movimento continua reconhecível.')
entries=[
 ('karaoke-fill-sync','A voz preenche a palavra.','Duas camadas + máscara linear por palavra. Fonte de tempo: áudio real. Elevar o contraste da base não lida.'),
 ('blur-slide','A frase chega e entra em foco.','Opacidade, y e blur ligados. Referência: 22 f por palavra, gap 4 f. Recalcular com a fala e a composição vertical.'),
 ('lead-word-zoom-assemble','Uma palavra puxa o gancho.','Âncora medida, zoom inicial 2,3×, montagem da frase. Variante teruya sem o crash final; registrar essa diferença.'),
 ('title-demote-to-label','O título passa a explicar o objeto.','O mesmo texto se move e reduz pela mesma curva em 26 f. Adaptar o rótulo final para manter pelo menos 40 px.'),
 ('pill-chip-slot-cycle-handled','O chip acompanha o termo.','Largura medida + deslocamento vertical. Preservar recorte e acompanhamento dos vizinhos; não esticar letras.')]
for i,(name,use,desc) in enumerate(entries):
    yy=165+i*112
    rect(M,yy,2,92,'line')
    text(name,M+16,yy+2,12 if len(name)<28 else 10.8,700,'blue')
    text(use,M+16,yy+26,12,600)
    para(desc,M+16,yy+49,CW-22,10.4,14.7)
text('Referências a 30 fps. Cadastro com caminhos, revisão e hashes no JSON de receitas.',M,750,9,400,'muted')
footer()

# 08 Diagram/interface recipes and proof.
header('10  /  SHOTCRAFT · COMPONENTES','Movimento que demonstra.','Escolher pela função da cena. Usar duas a quatro famílias é um ponto de partida.')
ent=[
 ('list-reveal','Itens chegam nas menções.','24 f por item, escala .82→1, y 44→0, blur 8→0. Ícone +2 f; detalhe +4 f. Drift do pai separado da entrada local.'),
 ('draw-svg-trace','O harness se constrói ao redor.','Traço de 40 f; cabeça no mesmo caminho. Fechamento: 2 f de pico + 6 f de retorno. Conteúdo aparece ao fechar.'),
 ('cursor-flyover','Uma ação real conduz a câmera.','Câmera 20 f; cursor sai 2 f antes e chega 6 f antes. Clique responde na interface. Usar apenas quando há ação de UI.'),
 ('line-carry-transition','A conexão vira a próxima cena.','Linha contínua e câmera acopladas. Cena original: 190 f; viagem de 56 f. Opcional, normalmente uma vez por vídeo.')]
for i,(name,use,desc) in enumerate(ent):
    yy=169+i*116
    text(f'0{i+1}',M,yy,18,600,'muted')
    text(name,M+49,yy+1,13,700,'blue')
    text(use,M+49,yy+28,12,600)
    para(desc,M+49,yy+52,CW-49,10.3,14.8)
rect(M,657,CW,112,'white',r=13.5)
text('Como comprovar o uso',M+17,673,14,700)
para('Cartão + TSX + parâmetros + render comparado. Registrar a adaptação pop e sua saída. Preservar o movimento que define a receita; não empilhar springs em pais e filhos.',M+17,703,CW-34,11,16)
footer()

# 09 Pilot storyboard, documentation only.
header('11  /  EPISÓDIO DE REFERÊNCIA','Mesmo modelo. Outra edição.','Aplicação proposta ao vídeo existente. Esta etapa não altera nem renderiza o vídeo.')
events=[
 ('00–05,87','Gancho','Rosto abre a fala. “Mesmo modelo” entra e conduz a montagem do título.','Lead word zoom'),
 ('05,87–09,87','Conceitos','MODELO e HARNESS aparecem nas menções. O título vira rótulo.','Title demote'),
 ('09,87–18,67','Estrutura','Chip permanece; contorno se desenha e a câmera destaca a relação.','Draw SVG + foco'),
 ('18,67–23,67','Ferramentas e contexto','Retorno breve do rosto; palavras entram e ocupam compartimentos.','Blur slide + layout'),
 ('23,67–38,07','Aplicativos e saídas','Entradas nas menções. Aproximar exemplos e recuar para comparar.','List reveal + retorno'),
 ('38,07–48,77','Conclusão','Recompor o diagrama. Foco acompanha a escolha de modelo e harness.','Reuso + karaoke'),
 ('48,77–50,27','Pergunta','“Qual harness você usa?” permanece para leitura e sai com pop discreto.','Hold + saída')]
for i,(tm,title,body,rec) in enumerate(events):
    yy=164+i*79
    text(tm,M,yy,10.1,700,'blue')
    text(title,M+100,yy,12,700)
    para(body,M+100,yy+23,CW-100,10,14)
    if i<6:line(M+100,yy+69,W-M,yy+69)
note('Referência: 1508 frames / 50,27 s. Medir as palavras antes da aplicação. Conferir nomes e versões citados na fala separadamente da direção visual.',727)
footer()

# 10 Workflow / handoff.
header('12  /  PRODUÇÃO E REVISÃO','O padrão precisa ser repetível.','A estética orienta a edição. A evidência confirma a execução.')
steps=[('01','Voz e marcações','Montagem da fala, transcrição revisada e palavras alinhadas ao áudio.'),('02','Vetores e motion','VectorCraft → EffectCraft. Quando necessário, render da receita em Remotion e importação no FilmCraft.'),('03','Montagem e conferência','FilmCraft: voz, aparições, legendas e efeitos. Ver o render inteiro; ouvir no celular e conferir o overlay.')]
for i,(n,t,b) in enumerate(steps):row_title(n,t,165+i*94,b,79)
label('ANTES DE ENTREGAR',M,460)
checks=['Texto sobre o rosto sem fundo, com os dois contornos visíveis.','Ênfase: Elastic Pop-In e Pop-Out em cada letra.','Coreografia expressiva, apoios estáticos e pausas de leitura.','Receitas têm fonte, adaptações e render conferido.','Recorte no rosto, sem blur lateral; som e SDR revisados.']
for i,s in enumerate(checks):
    yy=487+i*28
    rect(M,yy+1,10,10,'white','blue',2)
    text(s,M+22,yy,10.5)
rule(641)
label('PACOTE REUTILIZÁVEL',M,662)
para('<b>VIDEO_STANDARD.md</b> · regras completas<br/><b>tokens.json</b> + <b>motion-presets.json</b> · design e pop<br/><b>shotcraft-recipes.json</b> · fontes e validação<br/><b>scene-template.json</b> · ciclo de cada elemento',M,684,310,9.5,15)
link('ShotCraft · revisão utilizada','https://github.com/Vincentwei1021/video-shotcraft/tree/5a2e98daade313c4f376120f38427eb19a108e8c',M+318,686,8.5)
link('SF Pro · Apple Developer','https://developer.apple.com/fonts/',M+318,712,8.5)
text('Design: Markdown fornecido',M+318,738,8.3,400,'muted')
text('JSONs são especificações. Implementação e validação dos presets serão feitas na edição.',M,761,8.4,400,'muted')
footer()
# Optional integral presenter format, added 2026-10-30.
header('13  /  VARIANTE OPCIONAL','Apresentador + quadro 60/40.','A explicação ocupa o topo. O apresentador permanece na conversa.')
rect(M,170,216,384,'white','line',0)
sketch_grid(M,170,216,230.4,scale=.2)
text('QUADRO',M+108,205,16,600,'blue','center')
text('60% · 1080 × 1152',M+108,234,10,400,'muted','center')
rect(M+24,280,168,54,'canvas',r=10)
text('Ideia → componente',M+108,300,12,600,'blue','center')
text('Legendas em até duas linhas',M+108,373,9,600,'ink','center')
rect(M,400.4,216,153.6,'dark')
text('APRESENTADOR',M+108,450,13,600,'white','center')
text('40% · 1080 × 768',M+108,478,10,400,'white','center')
para('<b>Uma opção de composição.</b><br/>Usar quando a presença contínua ajuda a explicar. Não torna o split obrigatório nos próximos episódios.',M+240,174,CW-240,11,16)
para('<b>Transformar em 18–24 frames.</b><br/>A câmera reduz e se reposiciona sem parar o take. Recorte proporcional para preencher o painel, com foco no rosto e divisão reta. Nunca usar blur lateral.',M+240,279,CW-240,11,16)
para('<b>Separar os movimentos.</b><br/>O zoom do quadro não arrasta legenda ou apresentador. Texto sobre o rosto flutuante e com contorno duplo. Ênfase tem entrada e saída elásticas por letra.',M+240,390,CW-240,11,16)
rule(584)
text('Integral significa preservar o tempo.',M,610,18,600)
para('Dois takes completos, em ordem, sem retirar pausas, acelerar ou repetir conteúdo. A transformação gráfica muda a composição; a gravação e a voz continuam avançando.',M,649,CW,11,16)
para('Referência aprovada: 1680 + 651 = 2331 frames / 77,7 s. A versão 3.0 orienta os próximos vídeos; a edição entregue e seus projetos permanecem preservados.',M,718,CW,10,15)
footer()
# 15 Per-grapheme emphasis and adaptive glyph outlines.
header('14  /  ÊNFASE POR LETRA','Letras com presença.','Elastic Pop-In e Elastic Pop-Out próprios em cada letra da palavra de ênfase.')
for x,bg,stroke,fg,labeltext in [(M,'muted','white','blueOnDark','ESCURO · BRANCO + PRETO'),(M+264,'line','black','blue','CLARO · PRETO + BRANCO')]:
    rect(x,170,243,128,bg,'line',0)
    outlined_text('ÊNFASE',x+121.5,210,40,fg,stroke,'center')
    text(labeltext,x,313,8,600,'muted')
    text('ORDEM: INTERNO + EXTERNO',x,329,7,400,'muted')
para('Dois anéis nos glifos: externo mais fino, interno junto à letra. Desenhar externo, interno e preenchimento. Mesma posição e animação nas três camadas. Obrigatório sobre a câmera e nas ênfases; sem fundo.',M,349,CW,11,16)
rule(410)
for j,(labeltext,scales) in enumerate([('ENTRA',[1.08,.8,.55]),('PERMITE LER',[1,1,1]),('SAI',[.55,.85,1.06])]):
    x=M+j*174
    text(labeltext,x,436,9,600,'muted')
    for i,(letter,scale) in enumerate(zip('POP',scales)):
        size=38*scale
        outlined_text(letter,x+24+i*43,482+(38-size)/2,size,align='center')
    text('Quadro ilustrativo',x,543,8.5,400,'muted')
rows=[('Entrada por letra','12–16 f','0,55 → 1,08 → 0,98 → 1'),('Saída por letra','10–14 f','1 → 1,06 → 0,55 → 0')]
for i,(a,b,sc) in enumerate(rows):
    yy=588+i*47
    text(a,M,yy,11,600);text(b,M+184,yy,11,600,'blue');text(sc,W-M,yy,10,400,'muted','right')
para('Stagger inicial: 1 frame. Limitar a cascata a 8 f na entrada e 6 f na saída. Acentos ficam unidos; reservar posições finais e kerning. Ler por pelo menos 18 f após todas as letras assentarem.',M,694,CW,10,15)
text('Parâmetros de partida para validar na próxima edição; o vídeo aprovado não muda.',M,761,8.5,400,'muted')
footer()

# 16 Spatial cover crop only; no blurred side duplication.
header('15  /  ENQUADRAMENTO DO ROSTO','Preencher com a gravação.','Recortar espacialmente para encaixar no layout, com prioridade no rosto falando.')
# Diagram of a source portrait and the selected face window, not a real shot.
sx,sy,sw,sh=M,174,174,310
rect(sx,sy,sw,sh,'canvas','line')
def schematic_face(x,y,k=1):
    c.setFillColor(color('chipGray'))
    c.ellipse(x+31*k,H-(y+300*k),x+143*k,H-(y+137*k),fill=1,stroke=0)
    c.circle(x+87*k,H-(y+118*k),38*k,fill=1,stroke=0)
schematic_face(sx,sy)
crop_h=148*172/242
c.setStrokeColor(color('blue'));c.setLineWidth(2);c.rect(sx+13,H-(sy+66+crop_h),148,crop_h,fill=0,stroke=1)
text('Janela sobre o rosto',sx+87,500,10,600,'blue','center')
arrow(M+192,304,M+247,304)
dx=M+265;dy=248
rect(dx,dy,242,172,'canvas','blue',0,2)
c.saveState();clip=c.beginPath();clip.rect(dx,H-(dy+172),242,172);c.clipPath(clip,stroke=0,fill=0)
k=242/148;schematic_face(dx-13*k,dy-66*k,k);c.restoreState()
text('Painel preenchido por recorte',dx+121,442,10,600,'blue','center')
text('Esquema de enquadramento, sem simular uma captura real.',M,535,8.5,400,'muted')
rule(565)
para('<b>Escala proporcional em cover.</b> Recortar o excedente; não esticar o rosto. Olhos e boca têm prioridade. Manter testa, queixo e espaço para movimentos sempre que possível.',M,588,CW,11,16)
para('<b>Sem preenchimento lateral.</b> Nunca usar cópia desfocada, espelhada ou alongada da gravação. Se o rosto não couber, ajustar a janela de recorte ou a geometria do painel.',M,659,CW,11,16)
para('<b>Recorte espacial não é corte temporal.</b> Aplicar também no 60/40. As mudanças de composição preservam o tempo da gravação quando o episódio for integral.',M,730,CW,10,15)
footer()
c.save()
(ROOT/'output/pdf/font-build.json').write_text(json.dumps(FONT_BUILD,ensure_ascii=False,indent=2)+'\n')
print(f'{OUT}\n{page} pages')
