import pytest
from models.tatuagens.avaliacao import Avaliacao

def test_avaliacao():
    avaliacao = Avaliacao("Gersinho Gameplay", 5.0)
    assert avaliacao._cliente == "Gersinho Gameplay"
    assert avaliacao._nota == 5.0