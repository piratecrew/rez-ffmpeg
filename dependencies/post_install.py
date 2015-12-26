#!/bin/env python
import sys
import os
import shutil

def main(args):
    if not len(args)==3:
        print "Not enough arguments."
        return
    source_path = args[1]
    install_path = args[2]
    lib_path = os.path.join(install_path, "lib")
    print "SOURCE:", source_path
    print "INSTALL:", install_path
    pkgconfig_root = os.path.join(install_path, "lib", "pkgconfig")
    for pc in os.listdir(pkgconfig_root):
        pkgconfig_file = os.path.join(pkgconfig_root, pc)
        if not pkgconfig_file.endswith('.pc'):
            continue
        pkgconfig_tmp_file = os.path.join(pkgconfig_root, '%s.tmp' % (pc))
        print "Processing:", pkgconfig_file
        with open(pkgconfig_file, 'r') as pkg_file:
            with open(pkgconfig_tmp_file, 'w') as tmp_file:
                for line in pkg_file.readlines():
                    if line.startswith('Libs:'):
                        new_libs = []
                        libs = line.split(' ')
                        for lib in libs:
                            if source_path in lib:
                                new_lib = "-L%s" % (lib_path)
                                new_libs.append(new_lib)
                            else:
                                new_libs.append(lib)
                        line = ' '.join(new_libs)
                    tmp_file.write(line)
        shutil.move(pkgconfig_tmp_file, pkgconfig_file)

if __name__ == '__main__':
    main(sys.argv)
