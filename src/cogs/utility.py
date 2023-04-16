import discord
import requests
from discord.ext import commands
from datetime import datetime
import random  # Add this import
import tracery

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and message.author.name + '#' + message.author.discriminator == "Beckyy#4370" and message.author != self.client.user:
            rules = {
                "subject": [
                    "I", "You", "Bob", "Sue", "We", "They", "Aliens", "Giraffes", "Unicorns", "Robots", "Ghosts",
                    "Pirates", "Ninjas", "Astronauts", "Wizards", "Elves", "Zombies", "Mermaids", "Vikings", "Dragons",
                    "Detectives", "Samurais", "Cats", "Dogs", "Mice", "Bats", "Lions", "Frogs", "Spiders", "Squirrels",
                    "Sharks", "Ladybugs", "Camels", "Snakes", "Dolphins", "Gorillas", "Penguins", "Seagulls", "Elephants",
                    "Hedgehogs", "Beavers", "Monkeys", "Owls", "Rats", "Raccoons", "Turtles", "Bees", "Butterflies"
                ],
                "verb": [
                    "love", "hate", "like", "dislike", "prefer", "admire", "despise", "enjoy", "appreciate", "fear",
                    "adore", "cherish", "dread", "savor", "relish", "avoid", "embrace", "envy", "fantasize about",
                    "laugh at", "crave", "detest", "loathe", "anticipate", "distrust", "believe in", "dance with",
                    "sing to", "argue with", "whisper to", "celebrate", "mock", "swoon over", "welcome", "disregard",
                    "forgive", "blame", "kiss", "hug", "fight", "remember", "acknowledge", "trust", "ignore", "defend"
                ],
                "object": [
                    "apples", "bananas", "cherries", "dogs", "cats", "pineapples", "elephants", "unicorns", "spaceships",
                    "mountains", "rainbows", "lasers", "pumpkins", "lollipops", "robots", "vampires", "pirates", "ninjas",
                    "zombies", "wizards", "computers", "pizzas", "hamburgers", "tacos", "donuts", "ice cream", "potatoes",
                    "sunsets", "fireworks", "guitars", "dinosaurs", "jellyfish", "octopuses", "dragons", "ghosts", "aliens",
                    "roller coasters", "beaches", "volcanoes", "forests", "deserts", "skyscrapers", "castles", "moon",
                    "stars", "statues", "paintings", "monsters", "witches", "time machines", "frozen yoghurt", "bagels"
                ],
                "time": [
                    "in the morning", "before lunch", "at night", "during a thunderstorm", "after a nap", "at midnight",
                    "under the rain", "on a full moon", "on a sunny day", "while snowing", "on a foggy night", "in a dream",
                    "in a parallel universe", "in the future", "in the past", "on vacation", "during a hurricane",
                    "in a desert", "on a cruise", "at a party", "on a train", "in a spacecraft", "in the clouds",
                    "in the middle of the ocean", "on an ice rink", "on a tightrope", "during a tornado", "on the moon",
                    "in a cave", "on top of a mountain", "at a concert", "at the circus", "on a roller coaster",
                    "in a haunted house", "on a deserted island", "in a library", "in a maze", "on a stage", "in a jungle"
                ],
                "origin": [
                    "#subject# #verb# #object# #time#."
                ]
            }
            
            grammar = tracery.Grammar(rules)
            response = grammar.flatten("#origin#")
            await message.channel.send(response)
    
    @commands.command(brief="Deletes a specific amount of messages in the current channel, or upto the message that you reply til")
    async def purge(self, ctx, amount=None):
        if amount is None:
            if ctx.message.reference:
                async for msg in ctx.channel.history(limit=None):
                    if msg.author == self.client.user:
                        await msg.delete()
                    if (
                        msg.id == ctx.message.reference.message_id
                    ):  # once initial message is reached
                        return
        else:
            amount = int(amount)
            counter = -1
            async for msg in ctx.channel.history(limit=None):
                if counter >= amount:
                    return

                if msg.author == self.client.user:
                    await msg.delete()
                    counter += 1
                    
    @commands.command(brief="Same as ,purge but for every user (needs manage messages)")
    async def purgeall(self, ctx, amount=None):
        if amount is None:
            if ctx.message.reference:
                async for msg in ctx.channel.history(limit=None):
                    try:
                        await msg.delete()
                    except:
                        pass
                    
                    if (
                        msg.id == ctx.message.reference.message_id
                    ):  # once initial message is reached
                        return
        else:
            amount = int(amount)
            counter = -1
            async for msg in ctx.channel.history(limit=None):
                if counter >= amount:
                    return

                try:
                    await msg.delete()
                    counter += 1
                except:
                    pass

    @commands.command(brief="Fetches and joins a voice channel by ID")
    async def joinvc(self, ctx, id):
        await self.client.get_channel(int(id)).connect()

    @commands.command(brief="Lookup information about a Discord user")
    async def fetch(self, ctx, id):
        if "<@" in id:
            id = id.strip("<@").strip(">")

        user = await self.client.fetch_user(int(id))
        msg = f"{user} - {user.id}\nAvatar URL: {user.avatar_url}\nJoin date: <t:{int(user.created_at.timestamp())}>"
        banner_request = await self.client.http.request(
            discord.http.Route("GET", f"/users/{id}")
        )
        if banner_request["banner"]:
            banner_url = f"https://cdn.discordapp.com/banners/{id}/{banner_request['banner']}?size=1024"
            msg += f"\nBanner URL: {banner_url}"

        await ctx.message.edit(content=msg)

    @commands.command(brief="Fetches wikipedia for a short summary of your query")
    async def whatis(self, ctx, query):
        r = requests.get(
            f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={query}"
        )
        result = r.json()

        page = list(result["query"]["pages"].values())[0]

        ellipses = ""

        if "may refer to" not in page["extract"]:
            page["extract"] = page["extract"].replace("\n", "\n\n")
            ellipses = "..."

        await ctx.message.edit(
            content=f"""**{page["title"]}:**

{page["extract"][:1990 - len(page["title"])]}{ellipses}
"""
        )

    @commands.command(aliases=["wiki"], brief="Lists out wikipedia articles that are relevant to your query")
    async def wikipedia(self, ctx, query):
        response = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&namespace=0&format=json"
        ).json()
        results = "\n".join(
            [
                f"**{name}:** <{response[3][index]}>"
                for index, name in enumerate(response[1])
            ]
        )

        await ctx.message.edit(
            content=f"""Search results for \"{query}\"

{results}
"""
        )

    @commands.command(brief="Useful little fake identity command for placeholder data")
    async def fakeuser(self, ctx, nationality=None):
        url = "https://randomuser.me/api/1.4"
        if nationality:
            url += f"?nat={nationality}"

        identity = requests.get(url).json()["results"][0]
        date_of_birth = int(
            datetime.fromisoformat(identity["dob"]["date"].rstrip("Z")).timestamp()
        )

        return await ctx.message.edit(
            content=f"""
{identity["name"]["title"]}. {identity["name"]["first"]} {identity["name"]["last"]}
{identity["location"]["city"]}, {identity["location"]["state"]}, {identity["location"]["country"]}
{identity["location"]["street"]["number"]} {identity["location"]["street"]["name"]}, {identity["location"]["postcode"]}

Born <t:{date_of_birth}:R> on <t:{date_of_birth}>

Email: {identity["email"]}
Username: {identity["login"]["username"]}
Password: {identity["login"]["password"]}

{identity["picture"]["large"]}
"""
        )


def setup(client):
    client.add_cog(Utility(client))
    
    
    # JohnWick was here 3-14-23 <3
