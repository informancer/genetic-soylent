from paver.easy import *
import paver.doctools

def run_script(input_file, run_dir, script_name, interpreter='python'):
    """Run a script in the context of rundir relative to the
    input_file's directory, return the text output formatted to be
    included as an rst literal text block.
    """
    from paver.runtime import sh
    from paver.path import path
    docdir = path(input_file).dirname()
    output_text = sh('cd %(docdir)s/%(run_dir)s;%(interpreter)s %(script_name)s 2>&1' % vars(),
                    capture=True)
    response = '\n::\n\n\t$ %(interpreter)s %(script_name)s\n\t' % vars()
    response += '\n\t'.join(output_text.splitlines())
    while not response.endswith('\n\n'):
        response += '\n'
    return response
# Stuff run_script() into the builtins so we don't have to
# import it in all of the cog blocks where we want to use it.
__builtins__['run_script'] = run_script

options(
    setup=dict(
        name="Soylent",
        version="0.0",
        author="Adrien Beaucreux",
        author_email="informancer@web.de"
        ),
    cog=Bunch(
        beginspec='{{{cog',
        endspec='}}}',
        endoutput='{{{end}}}',
        ),
    sphinx = Bunch(
        docroot = 'doc',
        builder = 'html',
        builddir = '_build',
     ),
)

@task
@needs(['cog'])
def html():
    paver.doctools.html() 
