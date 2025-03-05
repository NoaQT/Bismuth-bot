import socket
import struct
import asyncio


class MCQuery:
    id = 0

    challenge = None

    def __init__(self, host="localhost", port=25565, timeout=1, max_retries=1, event_loop=None):
        self.addr = (host, port)
        self.timeout = timeout
        self.max_retries = max_retries
        self.event_loop = event_loop or asyncio.get_running_loop()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.settimeout(self.timeout)

    async def send_packet(self, type, payload):
        data = struct.pack(">HBl", 0xFEFD, type, self.id) + payload
        await self.event_loop.sock_sendto(self.sock, data, self.addr)

    async def read_packet(self):
        retry = self.max_retries
        while retry > 0:
            try:
                buf = await self.event_loop.sock_recv(self.sock, 4096)
                return buf[5:]
            except TimeoutError:
                retry -= 1
                continue

        raise TimeoutError

    async def handshake(self):
        await self.send_packet(9, bytes())
        buf = await self.read_packet()
        self.challenge = int(buf[:-1])

    async def basic_stat(self):
        if self.challenge is None:
            await self.handshake()

        await self.send_packet(0, struct.pack(">l", self.challenge))
        buf = await self.read_packet()
        res = {}
        res["motd"], buf = buf.split(b"\x00", 1)
        res["gametype"], buf = buf.split(b"\x00", 1)
        res["map"], buf = buf.split(b"\x00", 1)
        num_players, buf = buf.split(b"\x00", 1)
        res["num_players"] = int(num_players)
        max_players, buf = buf.split(b"\x00", 1)
        res["max_players"] = int(max_players)
        res["hostport"] = struct.unpack("<h", buf[:2])[0]
        res["hostname"], _ = buf[2:].split(b"\x00", 1)

        for key in res:
            res[key] = res[key].decode()

        for key in "maxplayers", "numplayers", "hostport":
            res[key] = int(res[key])

        return res

    async def full_stat(self):
        if self.challenge is None:
            await self.handshake()

        await self.send_packet(0, struct.pack(">lxxxx", self.challenge))
        buf = await self.read_packet()

        buf = buf[11:]
        kv, players = buf.split(b"\x00\x01player_\x00\x00")

        kv = kv.split(b"\x00")
        res = {k.decode(): v.decode() for k, v in zip(kv[::2], kv[1::2])}
        for key in "maxplayers", "numplayers", "hostport":
            res[key] = int(res[key])

        players = players[:-2]
        res["players"] = [p.decode() for p in players.split(b"\x00")]

        return res
