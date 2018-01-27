# Enquanto não desenvolvo a lógica
# do jogo da velha, esse teste será
# bem dummy
#
# O Compileall no travis.yml fará o syntax checking


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
