import aiohttp
import json
from urllib.parse import quote_plus


class Scroll:
    def __init__(self, json_data: dict) -> None:
        self._id = json_data['id']
        self._name = json_data['name']
        self._description = json_data['description']
        self._kind = json_data['kind']
        self._types = json_data['types']
        self._growth_cost = json_data['costgrowth']
        self._order_cost = json_data['costorder']
        self._energy_cost = json_data['costenergy']
        self._decay_cost = json_data['costdecay']
        self._attack = json_data['ap']
        self._countdown = json_data['ac']
        self._health = json_data['hp']
        self._flavor = json_data['flavor']
        self._rarity = json_data['rarity']
        self._set = json_data['set']
        self._passive_rules = json_data.get('passiverules', [])
        self._abilities = json_data.get('abilities', [])

    @property
    def cost(self) -> str:
        if self._growth_cost:
            return f'<:Growth:320829951534170113> {self._growth_cost}'
        if self._order_cost:
            return f'<:Order:320830133801975808> {self._order_cost}'
        if self._decay_cost:
            return f'<:Decay:320829724085583874> {self._decay_cost}'
        if self._energy_cost:
            return f'<:Energy:320830049039417344> {self._energy_cost}'

    @property
    def attack(self) -> str:
        return '-' if not self._attack else self._attack

    @property
    def countdown(self) -> str:
        return '-' if self._countdown < 1 else self._countdown

    @property
    def rarity(self) -> str:
        rarities = {
            0: 'Common',
            1: 'Uncommon',
            2: 'Rare'
        }
        return rarities[self._rarity]

    @property
    def description(self) -> str:
        return self._description.replace('<', '').replace('>', '').replace('\\n', '\n')

    @property
    def passive_rules(self) -> str:
        return ', '.join([rule['name'] for rule in self._passive_rules])

    @property
    def types(self) -> str:
        return self._types.replace(',', ', ')

    @property
    def image(self) -> str:
        return f'https://a.scrollsguide.com/image/screen?name={quote_plus(self._name)}&size=small'

    @property
    def printable(self) -> str:
        ret = f'**{self._name}** {self.cost}\n' \
              f'{self.rarity} {self._kind.capitalize()}'
        if self.types:
            ret += f' ({self.types})'
        if self.attack != '-' or self.countdown != '-' or self._health:
            ret += f'\n<:attack:462355358229200916> {self.attack} | ' \
                   f'<:countdown:462355358057496577> {self.countdown} | ' \
                   f'<:health:462355358250434570> {self._health}'
        if self.passive_rules:
            ret += f'\n*{self.passive_rules}*'
        if self.description:
            ret += f'\n\n{self.description}'
        if self._flavor:
            ret += f'\n\n*{self._flavor}*'
        return ret


class ScrollNotFound(Exception):
    pass


async def get_scroll(name: str) -> Scroll:
    async with aiohttp.ClientSession() as s:
        async with s.get('http://a.scrollsguide.com/scrolls') as resp:
            text = await resp.text()
            data = json.loads(text)
            for scroll in data.get('data', []):
                if scroll['name'] == name:
                    return Scroll(scroll)

            raise ScrollNotFound
