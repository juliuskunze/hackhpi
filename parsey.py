import subprocess


def execute_multiple_commands(commands: str, cwd: str = '/home/julius/prj/tensorflow-models/syntaxnet/') -> int:
    process = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=True)
    return process.communicate()[0].strip()


# TODO replace ' (tick) symbol
def generate_conll_file(text: str = '''Flies are flying behind flies.
    This is a test, please succeed.
    One more sentence.
    Will it work?''') -> str:
    commands = 'alias python=/home/julius/.local/bin/python; export PATH=/home/julius/.local/bin:$PATH; echo \'{0}\' | /home/julius/prj/tensorflow-models/syntaxnet/syntaxnet/demo.sh'.format(
        text)
    result = execute_multiple_commands(commands)
    # if result != 0:
    #    raise Exception('return code ' + str(result))

    return '/home/julius/prj/tensorflow-models/syntaxnet/tagged.conll'
