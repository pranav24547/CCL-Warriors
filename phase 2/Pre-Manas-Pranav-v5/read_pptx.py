import zipfile
import re
import glob
import os
import shutil

pptx_path = 'CFL Competition Submission – Phase 2 template.pptx'
temp_dir = 'temp_pptx_extract'

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

with zipfile.ZipFile(pptx_path, 'r') as z:
    z.extractall(temp_dir)

slides = glob.glob(f'{temp_dir}/ppt/slides/slide*.xml')
# Sort by slide number
slides.sort(key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1)))

for slide in slides:
    with open(slide, 'r', encoding='utf-8') as f:
        xml = f.read()
    texts = re.findall(r'<a:t>(.*?)</a:t>', xml)
    print(f"\n[{os.path.basename(slide).upper()}]")
    for t in texts:
        t = t.strip()
        if len(t) > 0:
            print(" - " + t)

shutil.rmtree(temp_dir)
