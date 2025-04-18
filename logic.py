import aiohttp  # A library for asynchronous HTTP requests
import random
import asyncio

class Pokemon:
    pokemons = {}
    # Object initialisation (constructor)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.type = None
        self.level = 1
        self.hp = random.randint(100, 150)
        self.power = random.randint(20, 50)
        self.experience = 0
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails

    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
        self.type = await self.get_type()
        return f"The name of your Pokémon: {self.name} type: {self.type} level: {self.level}, XP: {self.experience}, "  # Returning the string with the Pokémon's name
    

    async def get_image(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['sprites']['front_default']
                else:
                    return "Img not found"  

    async def get_type(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['types'][0]['type']['name']
                else:
                    return "Type not found"  
        
    async def feed(self):
        # Give XP and potentially level up
        xp_gained = 5
        self.experience += xp_gained

        # Level up logic
        if self.experience >= self.level * 10:
            self.experience = 0
            self.level += 1
            return f"{self.name} leveled up to level {self.level}!"
        return f"{self.name} gained {xp_gained} XP!"
    
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Periksa apakah musuh adalah tipe data Penyihir (instance dari kelas Penyihir)
            kesempatan = random.randint(1,5)
            if kesempatan == 1:
                return "Pokemon penyihir menggunakan perisai dalam pertarungan"
        
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertarungan @{self.pokemon_trainer} dengan @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!"

class Wizard(Pokemon):
    async def attack(self, enemy):
        return await super().attack(enemy)

class Fighter(Pokemon):
    async def attack(self, enemy):
        kekuatan_super = random.randint(5,15)
        self.power += kekuatan_super
        hasil = await super().attack(enemy)
        self.power -= kekuatan_super
        return hasil + f"\nPetarung menggunakan serangan super dengan kekuatan:{kekuatan_super} "


async def main():
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(await wizard.info())
    print()
    print(await fighter.info())
    print()
    print(await fighter.attack(wizard))

if __name__ == '__main__':
    asyncio.run(main())