
from .sources.lenta import (
    META as LENTA_META,
    load as load_lenta
)
from .sources.factru import (
    META as FACTRU_META,
    load as load_factru
)
from .sources.gareev import (
    META as GAREEV_META,
    load as load_gareev
)
from .sources.ne5 import (
    META as NE5_META,
    load as load_ne5
)
from .sources.wikiner import (
    META as WIKINER_META,
    load as load_wikiner
)
from .sources.librusec import (
    META as LIBRUSEC_META,
    load as load_librusec
)


REGISTRY = [
    (LENTA_META, load_lenta),
    (FACTRU_META, load_factru),
    (GAREEV_META, load_gareev),
    (NE5_META, load_ne5),
    (WIKINER_META, load_wikiner),
    (LIBRUSEC_META, load_librusec),
]
