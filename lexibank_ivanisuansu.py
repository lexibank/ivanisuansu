import attr
import lingpy
from clldutils.path import Path
from clldutils.text import strip_chars, split_text_with_context
from clldutils.misc import lazyproperty
from lingpy.sequence.sound_classes import syllabify
from pylexibank.dataset import Concept, Language
from pylexibank.dataset import NonSplittingDataset as BaseDataset
from pylexibank.util import pb, getEvoBibAsBibtex

@attr.s
class HLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default="Unclassified")
    DialectGroup = attr.ib(default=None)
    Location = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "ivanisuansu"
    language_class = HLanguage

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):
        wl = lingpy.Wordlist(self.raw.posix("suansu.tsv"))

        converter = {
                'll': 'lː',
                "ddʑ": "dʑː",
                "mm": "mː",
                "nn": "nː",
                "ss": "sː",
                "tts": "tsː",
                "tʂ": "ʈʂː",
                "bb": "bː",
                "dd": "dː",
                "pp": "pː",
                "tt": "tː",
                "ttʰ": "tʰː",
                "ɹɹ": "ɹː",
                "ff": "fː",
                "je": "j e",
                "oj": "oi",
                "ph": "pʰ",
                "th": "tʰ",
                "ttɕ": "tɕː",
                "ttʃ": "tʃː",
                "ma": "m a",
                "ē": "e",
                "ê": "e",
                "ʈʈʂ": "ʈʂː",
                "I": "ɪ",
                "ʷ": "w",
                }

        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            ds.add_concepts(id_factory=lambda c: c.concepticon_id)
            ds.add_languages()

            for k in pb(wl, desc="wl-to-cldf", total=len(wl)):
                ds.add_form_with_segments(
                    Language_ID='Suansu',
                    Parameter_ID=wl[k, 'concepticon_id'],
                    Value=''.join(wl[k, "tokens"]),
                    Form=''.join(wl[k, 'tokens']),
                    Segments=' '.join(
                        [converter.get(x, x) for x in wl[k, 'tokens']]).split(),
                    Source=["Ivani2019"],
                )
