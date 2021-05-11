from .db import Db

def unit(*word_list):
    from .Unit import Unit, UnitWord
    res = []
    for elem in word_list:
        res.append(UnitWord(*elem))
    return Unit(*res)