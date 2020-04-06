import re

with open("c://users//hunglnm//documents//template_re", "r") as f:
        print(f.read().splitlines())
        tmpl = "\n".join(f.read().splitlines())
f.close()
with open("c://users//hunglnm//documents//DBN01BPU", "r") as f1:
        cnt = f1.read()
print(tmpl)
txt_cmp1= re.match(tmpl, cnt)
if txt_cmp1:
    print(txt_cmp1.groups())
else:
    print("Khong tim thay cmp1")