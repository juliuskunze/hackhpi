import subprocess


def generate_conll_file() -> str:
    result = subprocess.call(['./run.sh'])

    if result != 0:
        raise Exception('return code ' + str(result))

    return '/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll'
