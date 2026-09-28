"""앱 아이콘 PNG 생성 (외부 라이브러리 없이). 초록 바탕 + 노란 깃발."""
import zlib, struct, os

def png(path, W, pixels):
    raw = b''.join(b'\x00' + bytes(pixels[y*W*4:(y+1)*W*4]) for y in range(W))
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', W, W, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))

GREEN, DEEP, FLAG, WHITE = (28, 107, 65), (14, 68, 40), (255, 198, 41), (255, 255, 255)

def color_at(x, y, maskable):
    # 좌표계 0..32 (파비콘 SVG와 같은 모양)
    if not maskable and (x-16)**2 + (y-16)**2 > 15**2: return None
    c = GREEN
    if ((x-16)/8)**2 + ((y-24.5)/2.2)**2 <= 1: c = DEEP
    if 12 <= x <= 14 and 7 <= y <= 24: c = WHITE
    # 깃발: (13,7.5)-(22,7.5)-(19.8,10.7)-(22,14)-(13,14)
    if 13 <= x and 7.5 <= y <= 14:
        edge = 22 - 2.2*(1 - abs(y-10.75)/3.25)
        if x <= edge: c = FLAG
    return c

def make(path, W, maskable=False, ss=4):
    px = []
    scale = 32 / W
    for j in range(W):
        for i in range(W):
            acc = [0, 0, 0, 0]
            for sj in range(ss):
                for si in range(ss):
                    x = (i + (si+.5)/ss) * scale; y = (j + (sj+.5)/ss) * scale
                    if maskable:  # 안전 영역 안에 들어오게 가운데로 축소
                        x = 16 + (x-16)/0.8; y = 16 + (y-16)/0.8
                    c = color_at(x, y, maskable)
                    if c: acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]; acc[3] += 255
            n = ss*ss; a = acc[3]
            px += [round(acc[0]/(a/255)) if a else 0, round(acc[1]/(a/255)) if a else 0, round(acc[2]/(a/255)) if a else 0, round(a/n)]
    png(path, W, px)

os.makedirs('icons', exist_ok=True)
make('icons/icon-192.png', 192)
make('icons/icon-512.png', 512, ss=2)
make('icons/maskable-512.png', 512, maskable=True, ss=2)
print('icons ok')
