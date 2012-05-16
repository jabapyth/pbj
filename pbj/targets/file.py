from target import Target
from reg import register

import os, glob

@register('file', required=1)
class FileTarget(Target):
    '''A build target based around producing a file.

    A FileTarget only builds when the dependant files are
    more recently modified than the target file. (or if
    the --force option is used). The target target file
    name is also registered as an alternate target name.

    Arguments:
        fname: the filename to produce

    example usage::

        @build.file("main.bin", depends=['main.c'])
        def main(outfile):
            """Compile the program"""
            compile_c(infile='main.c', outfile='main.bin')

    '''
    def __init__(self, fname, *args, **kwargs):
        Target.__init__(self, *args, **kwargs)
        self.filename = fname

    def applies_to(self, target):
        return target in ['@' + self.name, self.filename]

    def check_depends(self, builder):
        if Target.check_depends(self, builder):
            return True
        if not os.path.exists(self.filename):
            return True
        last_mod = os.path.getctime(self.filename)
        for dep in self.depends:
            if dep.startswith('@'):continue
            files = glob.glob(os.path.expanduser(dep))
            if not len(files):
                raise Exception, 'file not found %s -- depended on by ' % dep + self.filename
            for fname in files:
                if last_mod < os.path.getctime(fname):
                    return True
        return False

    def run(self, *args):
        self.fn(self.filename, *args)

# vim: et sw=4 sts=4
