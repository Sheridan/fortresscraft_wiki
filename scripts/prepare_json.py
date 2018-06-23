from gamedata_parser.parsers.fceitemsparser import FCEItemsParser
from gamedata_parser.parsers.fcereceiptsparser import FCEReceiptsParser
from gamedata_parser.parsers.fcegenericsreceiptsparser import FCEGenericReceiptsParser
from gamedata_parser.parsers.fceterrainparser import FCETerrainParser
from gamedata_parser.parsers.fceresearchparser import FCEResearchParser
from gamedata_parser.tools.jsonrecompiler import JsonRecompiler
from gamedata_parser.tools.listscompiler import ListsCompiler
from gamedata_parser.tools.graphscompiler import GraphsCompiler
from gamedata_parser.tools.spriteparser import SpriteParser
from gamedata_parser.tools.jsonmixer import JsonMixer


gamedata_dir = "/home/sheridan/software/fortresscraft/app/Default/Data"
media_dir = "/data/home/sheridan/development/fortresscraft/fortresscraft.info/media"


if __name__ == '__main__':
        # FCEItemsParser(gamedata_dir, media_dir).parse()
        # FCEReceiptsParser(gamedata_dir, media_dir).parse()
        # FCEGenericReceiptsParser(gamedata_dir, media_dir).parse()
        # FCETerrainParser(gamedata_dir, media_dir).parse()
        # FCEResearchParser(gamedata_dir, media_dir).parse()


        # JsonRecompiler(media_dir).recompile()
        # ListsCompiler(media_dir).compile()
        ## GraphsCompiler(media_dir).compile()
        SpriteParser(media_dir, 'BlockPreview_P20_64.png').parse()
        JsonMixer(media_dir).mix()
