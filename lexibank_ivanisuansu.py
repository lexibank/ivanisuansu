import attr
import lingpy
from pathlib import Path
from clldutils.misc import slug
from pylexibank import Language
from pylexibank import progressbar
from pylexibank.dataset import Dataset as BaseDataset


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
    writer_options = dict(keep_languages=False, keep_parameters=False)

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(self.raw_dir.joinpath("suansu.tsv").as_posix())

        converter = {
            "ll": "lː",
            "ddʑ": "dʑː",
            "ddʒ": "dʒː",
            "mm": "mː",
            "nn": "nː",
            "ss": "sː",
            "sʰ": "sʰ",
            "tts": "tsː",
            "ttʰ": "tʰː",
            "ddʰ": "dʰː",
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
            "kʰ": "kʰ",
            "kh": "kʰ",
            "ttɕ": "tɕː",
            "ttʃ": "tʃː",
            "ma": "m a",
            "ē": "e",
            "ê": "e",
            "ʈʈʂ": "ʈʂː",
            "I": "ɪ",
            "ʷ": "w",
        }

        args.writer.add_sources()
        concepts = {}
        args.writer.add_languages()

        for k in progressbar(wl, desc="wl-to-cldf", total=len(wl)):
            if wl[k, "concepticon_id"] not in concepts:
                cid = "{0}_{1}".format(wl[k, "concepticon_id"], slug(wl[k, "concept"]))
                concepts[wl[k, "concept"]] = cid
                args.writer.add_concept(
                    ID=cid,
                    Name=wl[k, "concept"],
                    Concepticon_ID=wl[k, "concepticon_id"],
                    Concepticon_Gloss=wl[k, "concepticon_gloss"],
                )
            args.writer.add_form_with_segments(
                Language_ID="Suansu",
                Parameter_ID=concepts[wl[k, "concept"]],
                Value="".join(wl[k, "tokens"]),
                Form="".join(wl[k, "tokens"]),
                Segments=" ".join(
                    [converter.get(x, x) for x in wl[k, "tokens"]]
                ).split(),
                Source=["Ivani2019"],
            )
