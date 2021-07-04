from discord.ext import commands

from bot.main import NewCommand, Emoji, StringPaginator, reply

class Morse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="morse",
        cls=NewCommand,
        brief="Morse Code??!!!",
        description="Convert the Morse Code to Text and Text to Morse Code",
        help="""This command is used to convert the Morse Code into Ascii Text and Text to Morse Code.""",
        explained_usage=["**String:** The Text or Morse to Convert."],
        usage="<string:str>",
        examples=[
            'morse Hello, how are you!',
            'morse -- --- .-. ... . ....... . -..- .- -- .--. .-.. .'
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _morse(self, ctx, *, string:str):
        TEXT_TO_MORSE = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....',
            'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-',
            'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..',
            '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..',
            '9':'----.', '0':'-----', ',':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.',
            ')':'-.--.-', ':': '---...', "'": '.----.', "’": ".----.", '"': '.-..-.', ' ': '.......', '!': '-.-.--',
            '@': '.--.-.', '$': '...-..-', '&': '.-...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '_': '..--.-'
        }

        MORSE_TO_TEXT = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
            '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q',
            '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z',
            '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
            '-----': '0', '--..--': ',', '.-.-.-': '.', '..--..': '?', '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')',
            '---...': ':', '.----.': "'", '.-..-.': '"', '.......': ' ', '-.-.--': '!', '.--.-.': '@', '...-..-': '$', '.-...': '&',
            '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '..--.-': '_'
        }

        _tempset = set(string)
        check = True
        for char in _tempset:
            if char not in ['.', '-', ' ']:
                check = False
        
        if check is True:
            _templist = str(string).split(' ')
            converted = "".join(MORSE_TO_TEXT[str(i)] for i in _templist)
            await reply(self.client, ctx, f"`{converted}`")
        else:
            _templist = []
            for char in str(string):
                _templist.append(char)
            try:
                converted = " ".join(TEXT_TO_MORSE[str(i).upper()] for i in _templist)
                if len(converted) <= 1998:
                    await reply(self.client, ctx, f"`{converted}`")
                else:
                    entries = [f"`{converted[i:i+1998]}`" for i in range(0, len(converted), 1998)]
                    pager = StringPaginator(
                        pages=entries,
                        timeout=60
                    )
                    await pager.start(ctx)
            except KeyError as e:
                return await reply(self.client, ctx, f"{Emoji.redcross} The String contains some characters which cannot be converted into Morse!\n> If you think that's a Mistake, please report it to my Developers, they'll Review and fix it :)")


def setup(client):
    client.add_cog(Morse(client))