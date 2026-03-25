# methods/__init__.py

from . import strings
from . import nulls
from . import dateandtime
from . import logic
from . import structural

METHODS = {
    'strings': {
        'case_scrambler': strings.case_scrambler,
        'typo_generator': strings.typo_generator,
        'whitespace_padder': strings.whitespace_padder,
        'special_char_injector': strings.special_char_injector,
    },
    'nulls': {
        'null_injector': nulls.null_injector,
        'placeholder_filler': nulls.placeholder_filler,
    },
    'dateandtime': {
        'format_shifter': dateandtime.format_shifter,
        'epoch_resetter': dateandtime.epoch_resetter,
        'future_traveler': dateandtime.future_traveler,
        'logic_breaker': dateandtime.logic_breaker,
    },
    'logic': {
        'category_shifter': logic.category_shifter,
        'synonym_swapper': logic.synonym_swapper,
    },
    'structural': {
        'row_duplicator': structural.row_duplicator,
        'column_shuffler': structural.column_shuffler,
    }
}