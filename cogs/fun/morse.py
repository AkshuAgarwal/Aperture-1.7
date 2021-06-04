from discord.ext import commands

from bot.main import NewCommand, Emoji, StringPaginator, Errors

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
        usage="`morse` `<string:str>`",
        cooldown="`1/5 sec` - [`User`]",
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
            '@': '.--.-.', '$': '...-..-', '&': '.-...', ';': '-.-.-.'
        }

        MORSE_TO_TEXT = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
            '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q',
            '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z',
            '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
            '-----': '0', '--..--': ',', '.-.-.-': '.', '..--..': '?', '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')',
            '---...': ':', '.----.': "'", '.-..-.': '"', '.......': ' ', '-.-.--': '!', '.--.-.': '@', '...-..-': '$', '.-...': '&', '-.-.-.': ';'
        }

        _tempset = set(string)
        check = True
        for char in _tempset:
            if char not in ['.', '-', ' ']:
                check = False
        
        if check is True:
            _templist = str(string).split(' ')
            converted = "".join(MORSE_TO_TEXT[str(i)] for i in _templist)
            await ctx.reply(f"`{converted}`")
        else:
            #texttomorse
            _templist = []
            for char in str(string):
                _templist.append(char)
            try:
                converted = " ".join(TEXT_TO_MORSE[str(i).upper()] for i in _templist)
                if len(converted) <= 1998:
                    await ctx.reply(f"`{converted}`")
                else:
                    entries = [f"`{converted[i:i+1998]}`" for i in range(0, len(converted), 1998)]
                    pager = StringPaginator(
                        pages=entries,
                        timeout=60
                    )
                    await pager.start(ctx)
            except KeyError as e:
                return await ctx.reply(f"{Emoji.redcross} The String contains some characters which cannot be converted into Morse!")

    @_morse.error
    async def _morse_error(self, ctx, error):
        _error = getattr(error, "original", error)
        error = Errors(ctx, _error)
        await error.response()

def setup(client):
    client.add_cog(Morse(client))