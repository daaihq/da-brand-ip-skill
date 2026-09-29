#!/usr/bin/env python3
"""Portable three-image brand/character packages. Python standard library only."""
import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ASSETS={'main':('01-main.png',1.0),'turnaround':('02-turnaround.png',1.5),'overview':('03-overview.png',4/3)}
FIELDS=('brand_id','brand_name','entity_type','character_id','character_name','style_id','identity','palette','allowed_changes','forbidden_changes','actions','expressions')
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.write-',dir=p.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def ident(s):
    if not isinstance(s,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',s):raise ValueError('IDs must be lowercase ASCII letters/numbers with - or _, up to 64 chars')
    return s
def validate_spec(s):
    for key in FIELDS:
        if key not in s:raise ValueError('Missing specification field: '+key)
    ident(s['brand_id']);ident(s['character_id'])
    if s['entity_type'] not in ['personal','company','brand','product','school','community','nonprofit','organization','event']:raise ValueError('Unsupported entity_type')
    for key in ['brand_name','character_name','style_id','identity']:
        if not isinstance(s[key],str) or not s[key].strip():raise ValueError('Nonempty string required: '+key)
    for key in ['palette','allowed_changes','forbidden_changes','actions','expressions']:
        if not isinstance(s[key],list) or any(not isinstance(v,str) or not v.strip() for v in s[key]):raise ValueError('Expected list of strings: '+key)
    if not s['palette'] or not s['forbidden_changes']:raise ValueError('Palette and forbidden_changes cannot be empty')
    if len(s['actions'])!=5 or len(s['expressions'])!=6:raise ValueError('Exactly 5 actions and 6 expressions required')
    version=int(s.get('layout_version',1))
    if version not in (1,2):raise ValueError('Unsupported layout version')
    if version==2:
        details=s.get('signature_details',[]);colors=s.get('color_palette',[])
        if not isinstance(details,list) or not 1<=len(details)<=6:raise ValueError('v2 requires 1-6 signature_details')
        if not isinstance(colors,list) or not 5<=len(colors)<=7:raise ValueError('v2 requires 5-7 color_palette entries')
        for items,field,limit in [(details,'label',6),(colors,'role',7)]:
            slots=[]
            for i,item in enumerate(items):
                value=item.get(field,'');slot=item.get('slot',i)
                if not isinstance(value,str) or not value.strip() or not value.isascii():raise ValueError('English display labels required')
                if not isinstance(slot,int) or isinstance(slot,bool) or not 0<=slot<limit or slot in slots:raise ValueError('Invalid or duplicate fixed slot')
                slots.append(slot)
        for color in colors:
            if not re.fullmatch(r'#[0-9A-Fa-f]{6}',color.get('hex','')):raise ValueError('Invalid palette HEX value')
def img_info(p,ratio):
    data=Path(p).read_bytes()
    if len(data)<33 or data[:8]!=b'\x89PNG\r\n\x1a\n' or data[12:16]!=b'IHDR':raise ValueError('Expected a real PNG: '+str(p))
    w,h=struct.unpack('>II',data[16:24])
    if min(w,h)<256 or abs(w/h-ratio)>0.015:raise ValueError('Wrong image dimensions/aspect ratio: '+str(p))
    return {'sha256':hashlib.sha256(data).hexdigest(),'width':w,'height':h,'bytes':len(data)}
def validate_package(folder):
    folder=Path(folder);m=read(folder/'manifest.json');s=read(folder/'character.json');validate_spec(s)
    if m.get('schema_version')!=1 or m.get('status') not in ['draft','confirmed']:raise ValueError('Invalid manifest schema/status')
    if int(m.get('layout_version',1))!=int(s.get('layout_version',1)):raise ValueError('Manifest/spec layout version mismatch')
    for k in ['brand_id','character_id','style_id']:
        if m.get(k)!=s[k]:raise ValueError('Manifest/spec mismatch: '+k)
    if not re.fullmatch(r'v[0-9]{3,}',m.get('version','')):raise ValueError('Invalid version')
    if m.get('spec_sha256')!=hashlib.sha256((folder/'character.json').read_bytes()).hexdigest():raise ValueError('Character specification checksum mismatch')
    if set(m.get('assets',{}))!=set(ASSETS):raise ValueError('Exactly three registered assets required')
    for key,(name,ratio) in ASSETS.items():
        rec=m['assets'][key]
        if rec.get('file')!=name:raise ValueError('Noncanonical asset path')
        if (folder/name).is_symlink():raise ValueError('Asset symlinks not allowed')
        info=img_info(folder/name,ratio)
        if any(rec.get(k)!=v for k,v in info.items()):raise ValueError('Asset metadata/hash mismatch: '+name)
    return m,s
def save_draft(root,s,images):
    s=dict(s)
    s.setdefault('layout_version',2)
    validate_spec(s);root=Path(root).resolve()
    skill=Path(__file__).resolve().parents[1]
    if root==skill or skill in root.parents:raise ValueError('Runtime assets must be outside the installed skill')
    base=root/'brands'/s['brand_id']/'characters'/s['character_id']
    base.mkdir(parents=True,exist_ok=True)
    nums=[int(p.name[1:]) for p in base.glob('v*') if p.is_dir() and re.fullmatch(r'v[0-9]{3,}',p.name)]
    version='v'+str(max(nums,default=0)+1).zfill(3);dest=base/version
    with tempfile.TemporaryDirectory(prefix='.draft-',dir=base) as temp:
        t=Path(temp);records={}
        for key,(name,ratio) in ASSETS.items():
            info=img_info(images[key],ratio);shutil.copyfile(images[key],t/name);records[key]={'file':name,**info}
        write(t/'character.json',s)
        m={'schema_version':1,'brand_id':s['brand_id'],'character_id':s['character_id'],'style_id':s['style_id'],'version':version,'status':'draft','created_at':datetime.now(timezone.utc).isoformat(),'layout_version':str(s.get('layout_version',2)),'spec_sha256':hashlib.sha256((t/'character.json').read_bytes()).hexdigest(),'assets':records,'visual_review':'required'}
        write(t/'manifest.json',m)
        if dest.exists():raise ValueError('Version collision; retry')
        # Atomic rename of a complete directory; no partial published version.
        os.rename(t,dest)
    return dest
def resolve(root,brand=None,character=None,version=None):
    root=Path(root).resolve()
    if bool(brand)!=bool(character):raise ValueError('Supply both --brand and --character')
    if not brand:
        a=read(root/'current.json');brand=a['brand_id'];character=a['character_id'];version=version or a['version']
    base=root/'brands'/ident(brand)/'characters'/ident(character)
    if not version:version=read(base/'active.json')['version']
    if not re.fullmatch(r'v[0-9]{3,}',version):raise ValueError('Invalid version')
    p=base/version;m,s=validate_package(p)
    if m['status']!='confirmed':raise ValueError('Draft cannot be used for content or activated')
    return p,m,s
def activate(root,p,m):
    a={k:m[k] for k in ['brand_id','character_id','version']}
    write(p.parent/'active.json',a);write(Path(root)/'current.json',a)
def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='cmd',required=True)
    for cmd in ['register','confirm','list','resolve','activate','export','import']:
        q=sub.add_parser(cmd);q.add_argument('--root',required=True)
        if cmd=='register':
            q.add_argument('--spec',required=True)
            for key in ASSETS:q.add_argument('--'+key,required=True)
        elif cmd=='confirm':
            for key in ['brand','character','version','confirmation']:q.add_argument('--'+key,required=True)
            q.add_argument('--visual-reviewed',action='store_true',required=True)
        elif cmd in ['resolve','activate','export']:
            for key in ['brand','character','version']:q.add_argument('--'+key)
            if cmd=='export':q.add_argument('--out',required=True)
        elif cmd=='import':q.add_argument('--archive',required=True)
    a=ap.parse_args();root=Path(a.root).resolve()
    if a.cmd=='register':print(save_draft(root,read(a.spec),{k:getattr(a,k) for k in ASSETS}))
    elif a.cmd=='list':
        result=[]
        for p in sorted(root.glob('brands/*/characters/*/v*/manifest.json')):
            m=read(p);result.append({k:m[k] for k in ['brand_id','character_id','version','status','style_id']})
        print(json.dumps(result,ensure_ascii=False,indent=2))
    elif a.cmd=='confirm':
        if not a.confirmation.strip():raise ValueError('Record actual user confirmation or prior authorization')
        if not re.fullmatch(r'v[0-9]{3,}',a.version):raise ValueError('Invalid version')
        p=root/'brands'/ident(a.brand)/'characters'/ident(a.character)/a.version;m,s=validate_package(p)
        m.update(status='confirmed',visual_review='passed',confirmation=a.confirmation,confirmed_at=datetime.now(timezone.utc).isoformat())
        write(p/'manifest.json',m);activate(root,p,m);print(p)
    elif a.cmd in ['resolve','activate','export']:
        p,m,s=resolve(root,a.brand,a.character,a.version)
        if a.cmd=='activate':activate(root,p,m)
        if a.cmd=='export':
            out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED) as z:
                for name in ['manifest.json','character.json']+[v[0] for v in ASSETS.values()]:z.write(p/name,name)
            print(out.resolve())
        else:print(json.dumps({'path':str(p),'manifest':m,'character':s},ensure_ascii=False,indent=2))
    elif a.cmd=='import':
        expected={'manifest.json','character.json'}|{v[0] for v in ASSETS.values()}
        with tempfile.TemporaryDirectory(prefix='da-ip-import-') as t,zipfile.ZipFile(a.archive) as z:
            infos=z.infolist()
            if len(infos)!=5 or {i.filename for i in infos}!=expected:raise ValueError('Archive must contain exactly the five canonical files')
            if sum(i.file_size for i in infos)>128*1024*1024:raise ValueError('Archive exceeds 128 MiB expanded')
            for i in infos:
                if (i.external_attr>>16)&0o170000==0o120000:raise ValueError('Symlinks not allowed')
                (Path(t)/i.filename).write_bytes(z.read(i))
            m,s=validate_package(t)
            s.setdefault('layout_version',int(m.get('layout_version',1)))
            dest=save_draft(root,s,{k:Path(t)/v[0] for k,v in ASSETS.items()})
            # Imports always remain draft until user selects/confirms the imported identity.
            print(json.dumps({'path':str(dest),'status':'draft','source_status':m['status'],'message':'Review and confirm imported package before activation'},ensure_ascii=False))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,zipfile.BadZipFile,json.JSONDecodeError) as e:raise SystemExit(str(e))
