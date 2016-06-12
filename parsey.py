import subprocess

#TODO replace ' (tick) symbol
def generate_conll_file(text: str = '''Flies are flying behind flies.
    This is a test, please succeed.
    One more sentence.
    Will it work?''') -> str:
    command = 'echo \'{0}\' | /home/julius/prj/tensorflow-models/syntaxnet/syntaxnet/demo.sh'.format(text)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode != 0:
        raise Exception('return code ' + str(process.returncode))

    conll_file = '/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll'