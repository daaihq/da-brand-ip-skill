#!/usr/bin/env python3
"""Place supplied independent white-background character art in fixed frames.
Requires Pillow. Does not generate characters, remove backgrounds or change identity.
"""
import argparse,json,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps

def compose(kind,spec_path,out,font_path):
    spec_path=Path(spec_path);s=json.loads(spec_path.read_text(encoding='utf-8'))
    layout=json.loads((Path(__file__).resolve().parents[1]/'assets/layouts/layout.json').read_text())[kind]
    out=Path(out)
    if out.exists():raise ValueError('Refusing to overwrite existing output')
    canvas=Image.new('RGB',tuple(layout['size']),'white');d=ImageDraw.Draw(canvas)
    def text(value,x,baseline,maxwidth,size,minsize=12,align='center'):
        value=str(value)
        if not value:return
        if not value.isascii() or any(ord(ch)<32 or ord(ch)>126 for ch in value):
            raise ValueError('Use English display text with printable ASCII punctuation: '+value)
        if '\n' in value:raise ValueError('Text must be single-line; shorten or supply an approved short label')
        probe=ImageFont.truetype(str(font_path),24)
        missing=bytes(probe.getmask('\uffff'))
        for ch in set(value):
            if not ch.isspace() and ord(ch)>127 and bytes(probe.getmask(ch))==missing:
                raise ValueError('Font lacks required glyph; supply a suitable font: '+ch)
        while size>=minsize:
            f=ImageFont.truetype(str(font_path),size)
            width=d.textlength(value,font=f)
            if width<=maxwidth:break
            size-=1
        else:raise ValueError('Text too long for fixed frame: '+value)
        if align=='center':px=x-width/2
        elif align=='right':px=x-width
        else:px=x
        d.text((px,baseline),value,font=f,fill='#222222',anchor='ls')
    def art(item,box,baseline):
        path=Path(item['file'])
        if not path.is_absolute():path=spec_path.parent/path
        with Image.open(path) as raw:
            im=ImageOps.exif_transpose(raw).convert('RGBA')
            # Keep source art intact; only fit and place, no automatic trimming.
            white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);im=white.convert('RGB')
        x,y,w,h=box
        available_h=min(h,baseline-y)
        ratio=min(w/im.width,available_h/im.height)
        resample=Image.Resampling.NEAREST if s.get('pixel_art',False) else Image.Resampling.LANCZOS
        im=im.resize((max(1,round(im.width*ratio)),max(1,round(im.height*ratio))),resample)
        canvas.paste(im,(x+(w-im.width)//2,baseline-im.height))
    def need(key,count):
        items=s.get(key,[])
        if not isinstance(items,list) or len(items)!=count:raise ValueError(f'{key} needs exactly {count} entries')
        return items
    if kind=='main':
        if not str(s.get('title','')).strip():raise ValueError('Character design card requires an English title')
        text(s['title'],*layout['title'],minsize=28)
        text(s.get('subtitle','CHARACTER DESIGN / v2'),*layout['subtitle'],minsize=16)
        text('MAIN CHARACTER',*layout['main_heading'])
        text('SIGNATURE DETAILS',*layout['details_heading'])
        art(need('images',1)[0],layout['slots'][0],layout['baseline'])
        details=s.get('details',[]);palette=s.get('palette',[])
        if not isinstance(details,list) or not 1<=len(details)<=6:raise ValueError('Provide 1-6 actual signature details')
        if not isinstance(palette,list) or not 5<=len(palette)<=7:raise ValueError('Provide 5-7 palette colors')
        def slots(items,limit):
            used=set()
            for i,item in enumerate(items):
                pos=item.get('slot',i)
                if not isinstance(pos,int) or isinstance(pos,bool) or not 0<=pos<limit or pos in used:
                    raise ValueError('Invalid or duplicate fixed slot')
                used.add(pos);yield pos,item
        for pos,item in slots(details,6):
            b=layout['details'][pos]
            art(item,b,b[1]+b[3])
            text(item['label'],b[0]+b[2]/2,layout['detail_label_baselines'][pos],b[2],15,minsize=11)
        text('COLOR PALETTE',*layout['palette_heading'])
        for pos,item in slots(palette,7):
            color=item.get('hex','')
            if not re.fullmatch(r'#[0-9a-fA-F]{6}',color):raise ValueError('Palette colors require exact six-digit HEX values')
            x,y,w,h=layout['swatches'][pos]
            d.rectangle((x,y,x+w-1,y+h-1),fill=color,outline='#D8D8D8',width=1)
            text(item['role'],x+w/2,layout['palette_label_baseline'],w,14,minsize=10)
            text(color.upper(),x+w/2,layout['palette_hex_baseline'],w,13,minsize=11)
        text(s.get('footer_left',''),48,layout['footer_baseline'],450,11,align='left')
        text(s.get('footer_right',''),976,layout['footer_baseline'],450,11,align='right')
    elif kind=='turnaround':
        text(s.get('title',''),*layout['title']);text(s.get('subtitle',''),*layout['subtitle'])
        for item,b in zip(need('images',3),layout['slots']):
            art(item,b,layout['baseline']);text(item['label'],b[0]+b[2]/2,layout['label_baseline'],b[2],22)
    else:
        # Font fitting never moves the title frame or other regions.
        text(s.get('title',''),*layout['title'],minsize=54)
        text(s.get('subtitle',''),*layout['subtitle'],minsize=18)
        text(s.get('tagline',''),*layout['tagline'],minsize=14)
        for side,key,x,align in [('left','info',40,'left'),('right','keywords',1560,'right')]:
            lines=s.get(key,[])
            if len(lines)>4:raise ValueError(key+' allows at most four lines')
            for i,line in enumerate(lines):text(line,x,58+i*23,240,16,align=align)
        for key,pill,label in [('actions','action_pill',s.get('actions_title','ACTIONS')),('expressions','expression_pill',s.get('expressions_title','EXPRESSIONS'))]:
            x,y,w,h=layout[pill];d.rounded_rectangle((x,y,x+w,y+h),radius=18,fill='#dddddd');text(label,x+w/2,y+25,w-20,18)
        for key,count,base,lab in [('actions',5,'action_baseline','action_label_baseline'),('expressions',6,'expression_baseline','expression_label_baseline')]:
            for item,b in zip(need(key,count),layout[key]):
                art(item,b,layout[base]);text(item['label'],b[0]+b[2]/2,layout[lab],b[2],20)
        d.line((440,157,550,157),fill='#aaaaaa',width=1);d.line((1050,157,1160,157),fill='#aaaaaa',width=1)
        text(s.get('footer_left',''),40,layout['footer_baseline'],700,14,align='left')
        text(s.get('footer_right',''),1560,layout['footer_baseline'],700,14,align='right')
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('xb') as f:canvas.save(f,format='PNG')
    return out.resolve()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kind',choices=['main','turnaround','overview'],required=True)
    p.add_argument('--spec',required=True);p.add_argument('--out',required=True);p.add_argument('--font',required=True)
    a=p.parse_args()
    try:print(compose(a.kind,a.spec,a.out,a.font))
    except (ValueError,OSError,KeyError) as e:raise SystemExit(str(e))
