# entities.py — Módulos, barcos e NPCs

import math
import random
from constants import C, MODULE_DEFS, UPGRADE_TREE, HULL_UPGRADES, FOG_RADIUS_BASE, GRID_SIZE


def lerp_color(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


class Module:
    def __init__(self, mod_type, rx=None, ry=None):
        d = MODULE_DEFS[mod_type]
        self.type      = mod_type
        self.name      = d['name']
        self.w         = d['w']
        self.h         = d['h']
        self.hp        = d['hp']
        self.max_hp    = d['hp']
        self.color_key = d['color']
        self.rx        = d['rx'] if rx is None else rx
        self.ry        = d['ry'] if ry is None else ry

    def local_tiles(self):
        return [(self.rx + dx, self.ry + dy)
                for dx in range(self.w)
                for dy in range(self.h)]

    @property
    def destroyed(self):
        return self.hp <= 0

    @property
    def color(self):
        if self.destroyed:
            return C['destroyed']
        return lerp_color(C['damaged'], C[self.color_key], self.hp / self.max_hp)

    def damage(self, amount=1):
        self.hp = max(0, self.hp - amount)


class Ship:
    def __init__(self, gx, gy, angle, pid):
        self.gx      = float(gx)
        self.gy      = float(gy)
        self.angle   = float(angle)
        self.pid     = pid
        self.modules : list[Module] = []
        self.money   = 200
        self.hull_level = 0

    # ── Atalhos de módulo ────────────────────────────────────────────────────

    def _mod(self, t):
        return next((m for m in self.modules if m.type == t and not m.destroyed), None)

    @property
    def hull(self):
        return next((m for m in self.modules if m.type == 'hull'), None)

    @property
    def alive(self):
        h = self.hull
        return h is not None and not h.destroyed

    @property
    def player_color(self):
        return C['p1'] if self.pid == 0 else C['p2']

    def has_engine(self):
        for t in ('engine_thermo', 'engine_nuclear', 'engine'):
            m = self._mod(t)
            if m:
                return m
        return None

    @property
    def max_speed(self):
        e = self.has_engine()
        if e is None:            return 2
        if e.type == 'engine_thermo':   return 8
        if e.type == 'engine_nuclear':  return 6
        return 4

    @property
    def noise_level(self):
        e = self.has_engine()
        if e is None:                   return 0.3
        if e.type == 'engine_thermo':   return 0.0
        if e.type == 'engine_nuclear':  return 0.4
        return 0.7

    @property
    def is_silent(self):
        e = self.has_engine()
        return e is not None and e.type == 'engine_thermo'

    def fog_radius(self):
        return FOG_RADIUS_BASE + (2 if self._mod('radar') else 0)

    def has_mortar(self):
        for t in ('mortar_heavy', 'mortar'):
            m = self._mod(t)
            if m:
                return m
        return None

    def mortar_range(self):
        m = self.has_mortar()
        if m is None:              return 0
        if m.type == 'mortar_heavy': return 20
        return 14

    def mortar_damage(self):
        m = self.has_mortar()
        return 2 if m and m.type == 'mortar_heavy' else 1

    def has_research(self):
        return self._mod('research') is not None

    def has_armor(self):
        return self._mod('armor') is not None

    # ── Geometria ────────────────────────────────────────────────────────────

    def center(self):
        h = self.hull
        if h:
            return self.gx + h.w / 2, self.gy + h.h / 2
        return self.gx + 1.5, self.gy + 1.0

    def world_tiles(self):
        ox, oy = int(self.gx), int(self.gy)
        tiles = set()
        for m in self.modules:
            if not m.destroyed:
                for rx, ry in m.local_tiles():
                    tiles.add((ox + rx, oy + ry))
        return list(tiles)

    def take_damage_at(self, wx, wy, amount=1):
        ox, oy = int(self.gx), int(self.gy)
        # Procura módulo não-casco primeiro
        for m in self.modules:
            if m.destroyed or m.type == 'hull':
                continue
            if any(ox + rx == wx and oy + ry == wy for rx, ry in m.local_tiles()):
                m.damage(amount)
                return True
        # Fallback: casco
        h = self.hull
        if h and any(ox + rx == wx and oy + ry == wy for rx, ry in h.local_tiles()):
            h.damage(amount)
            return True
        return False

    # ── Movimento ────────────────────────────────────────────────────────────

    def preview_move(self, steering, speed):
        from constants import GRID_SIZE as GS
        path = []
        x, y = self.gx, self.gy
        steering = max(-45, min(45, steering))
        for step in range(speed):
            t = step / max(speed - 1, 1) if speed > 1 else 1.0
            rad = math.radians(self.angle + steering * t)
            x += math.cos(rad)
            y += math.sin(rad)
            path.append((x, y))
        h = self.hull
        bw, bh = (h.w, h.h) if h else (3, 2)
        nx = max(0.0, min(float(GS - bw), x))
        ny = max(0.0, min(float(GS - bh), y))
        return nx, ny, (self.angle + steering) % 360, path

    def apply_move(self, steering, speed):
        self.gx, self.gy, self.angle, _ = self.preview_move(steering, speed)

    # ── Loja ─────────────────────────────────────────────────────────────────

    def available_purchases(self):
        owned = {m.type for m in self.modules}
        items = []

        # Expansão de casco
        if self.hull_level < len(HULL_UPGRADES):
            nw, nh, cost = HULL_UPGRADES[self.hull_level]
            items.append(('hull_expand', 'hull', f'Expandir Casco {nw}×{nh}', cost,
                          self.money >= cost, f'Cresce o casco para {nw}×{nh}'))

        # Upgrades de módulos existentes
        for base_type, up_type in UPGRADE_TREE.items():
            if base_type in owned and up_type not in owned:
                ud = MODULE_DEFS[up_type]
                items.append(('upgrade', base_type, ud['name'], ud['cost'],
                              self.money >= ud['cost'], ud['desc']))

        # Reparos
        for m in self.modules:
            if 0 < m.hp < m.max_hp:
                items.append(('repair', m.type, f'Reparar {m.name}', 30,
                              self.money >= 30, 'Restaura 1HP'))

        return items

    def can_afford(self, action, mod_type):
        if action == 'upgrade':
            return self.money >= MODULE_DEFS[UPGRADE_TREE[mod_type]]['cost']
        if action == 'repair':
            return self.money >= 30
        if action == 'hull_expand':
            return self.hull_level < len(HULL_UPGRADES) and \
                   self.money >= HULL_UPGRADES[self.hull_level][2]
        return False

    def apply_purchase(self, action, mod_type):
        if action == 'upgrade':
            up = UPGRADE_TREE.get(mod_type)
            if not up:
                return
            old = next((m for m in self.modules if m.type == mod_type), None)
            if old:
                new_m = Module(up, rx=old.rx, ry=old.ry)
                self.money -= MODULE_DEFS[up]['cost']
                self.modules.remove(old)
                self.modules.append(new_m)

        elif action == 'repair':
            m = next((m for m in self.modules if m.type == mod_type), None)
            if m:
                self.money -= 30
                m.hp = min(m.max_hp, m.hp + 1)

        elif action == 'hull_expand':
            if not self.can_afford('hull_expand', 'hull'):
                return
            nw, nh, cost = HULL_UPGRADES[self.hull_level]
            self.money -= cost
            h = self.hull
            if h:
                old_max = h.max_hp
                h.w, h.h = nw, nh
                h.max_hp = nw * nh
                h.hp = min(h.max_hp, h.hp + (h.max_hp - old_max))
            self.hull_level += 1

    # ── Tooltip de upgrade ────────────────────────────────────────────────────

    def upgrade_tooltip(self, mod_type):
        """Retorna (nome_upgrade, custo, desc) se houver upgrade disponível, ou None."""
        up = UPGRADE_TREE.get(mod_type)
        if up and not any(m.type == up for m in self.modules):
            d = MODULE_DEFS[up]
            return d['name'], d['cost'], d['desc']
        return None


# ═════════════════════════════════════════════════════════════════════════════
# NPCs
# ═════════════════════════════════════════════════════════════════════════════

class NPC:
    def __init__(self, gx, gy):
        self.gx    = float(gx)
        self.gy    = float(gy)
        self.alive = True
        self.hp    = 1
        self.angle = random.uniform(0, 360)

    def center(self):
        return self.gx, self.gy

    def world_tiles(self):
        return [(int(self.gx), int(self.gy))]

    def take_damage_at(self, wx, wy, amount=1):
        if int(self.gx) == wx and int(self.gy) == wy:
            self.hp -= amount
            if self.hp <= 0:
                self.alive = False
            return True
        return False

    def money_reward(self):
        return 50

    def update(self):
        pass


class Fish(NPC):
    SWIM_SPEED   = 0.04
    PAUSE_FRAMES = (60, 180)

    def __init__(self, gx, gy):
        super().__init__(int(gx) + 0.5, int(gy) + 0.5)
        self.target_x = self.gx
        self.target_y = self.gy
        self.pause_t  = random.randint(*self.PAUSE_FRAMES)
        self.timer    = 0
        self.moving   = False
        self._pick_target()

    def _pick_target(self):
        from constants import GRID_SIZE as GS
        radius = random.randint(2, 5)
        for _ in range(10):
            nx = self.gx + random.randint(-radius, radius)
            ny = self.gy + random.randint(-radius, radius)
            if 0.5 <= nx <= GS - 1.5 and 0.5 <= ny <= GS - 1.5:
                dist = math.hypot(nx - self.gx, ny - self.gy)
                if dist > 0.5:
                    self.target_x = float(int(nx)) + 0.5
                    self.target_y = float(int(ny)) + 0.5
                    self.angle = math.degrees(math.atan2(ny - self.gy, nx - self.gx))
                    self.moving = True
                    return
        self.moving  = False
        self.timer   = 0
        self.pause_t = random.randint(*self.PAUSE_FRAMES)

    def update(self):
        if not self.alive:
            return
        if self.moving:
            dx = self.target_x - self.gx
            dy = self.target_y - self.gy
            dist = math.hypot(dx, dy)
            if dist < self.SWIM_SPEED + 0.01:
                self.gx, self.gy = self.target_x, self.target_y
                self.moving  = False
                self.timer   = 0
                self.pause_t = random.randint(*self.PAUSE_FRAMES)
            else:
                self.gx += (dx / dist) * self.SWIM_SPEED
                self.gy += (dy / dist) * self.SWIM_SPEED
        else:
            self.timer += 1
            if self.timer >= self.pause_t:
                self._pick_target()

    def money_reward(self):
        return 50

    def world_tiles(self):
        return [(round(self.gx - 0.5), round(self.gy - 0.5))]

    def take_damage_at(self, wx, wy, amount=1):
        tx, ty = round(self.gx - 0.5), round(self.gy - 0.5)
        if tx == wx and ty == wy:
            self.hp -= amount
            if self.hp <= 0:
                self.alive = False
            return True
        return False


class NPCShip(NPC):
    def __init__(self, gx, gy):
        super().__init__(gx, gy)
        self.max_hp = 1
        self.speed  = random.uniform(0.03, 0.10)
        self.timer  = 0

    def update(self, map_grid):
        if not self.alive:
            return
        GS = len(map_grid)
        self.timer += 1
        if self.timer % 90 == 0:
            self.angle += random.uniform(-45, 45)

        rad = math.radians(self.angle)
        for d in range(1, 5):
            fx = int(self.gx + math.cos(rad) * d)
            fy = int(self.gy + math.sin(rad) * d)
            if 0 <= fx < GS and 0 <= fy < GS:
                if map_grid[fy][fx] != 'water':
                    self.angle += random.choice([25, -25, 40, -40])
                    break
            else:
                self.angle += random.choice([30, -30])
                break

        rad = math.radians(self.angle)
        self.gx = max(1.0, min(GS - 2.0, self.gx + math.cos(rad) * self.speed))
        self.gy = max(1.0, min(GS - 2.0, self.gy + math.sin(rad) * self.speed))

    def money_reward(self):
        return 150


class Particle:
    def __init__(self, sx, sy):
        a   = random.uniform(0, math.tau)
        spd = random.uniform(1.5, 5.0)
        self.x, self.y   = float(sx), float(sy)
        self.vx, self.vy = math.cos(a) * spd, math.sin(a) * spd
        self.life = random.randint(18, 40)
        self.col  = random.choice([C['exp_a'], C['exp_b'], C['exp_c']])

    def update(self):
        self.x  += self.vx;  self.y  += self.vy
        self.vx *= 0.90;     self.vy *= 0.90
        self.life -= 1

    def draw(self, surf):
        import pygame
        pygame.draw.circle(surf, self.col, (int(self.x), int(self.y)), max(1, self.life // 9))
