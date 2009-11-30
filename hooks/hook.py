import os
import sys
import shutil
import logging
import re

def hook(options,buildout):
    """"""
    os.system("""
              cd %s;
              sed -e "s|SUP_LIBS =|SUP_LIBS = %s |g" -i Makefile.in
              """%(
                  options['compile-directory'] ,
                  os.environ['LDFLAGS']
              )
             )

def install(options, buildout):
    location = os.path.join( options['location'], 'bin')
    include = os.path.join( options['location'], 'include')
    lib = os.path.join( options['location'], 'lib')
    for p in location, include, lib:
        if not os.path.isdir(p):
            os.makedirs(p)
    #mapserv = os.path.join(
    #    options['compile-directory'], 'mapserv')
    c = options['compile-directory']
    #dmapserv = os.path.join( location, 'mapserv')
    #shutil.copy(mapserv, dmapserv)
    message =  'Successfully installed mapserv into %s'
    logging.getLogger('mapserver hook').info(
        message % location)

    [shutil.copy(
        os.path.join(c,f), include
    )
        for f in os.listdir(c)
        if f.endswith('.h')]
    #[shutil.copy(
    #    os.path.join(c,f), lib
    #)
    #    for f in os.listdir(c)
    #    if f.startswith('.libmap')] 


def p(o, b):
    lib_re = re.compile('^((lib)(?P<dll>.+))$')
    if 'win' in sys.platform:
        dest = o['location']
        bin = os.path.join(dest, 'bin')
        lib = os.path.join(dest, 'lib')
        if not os.path.exists(bin): os.makedirs(bin)
        for dll in [libdll 
                    for libdll in os.listdir(lib) 
                    if( libdll.endswith('dll') 
                    and libdll.startswith('lib'))]:
            ldests = [os.path.join(bin, dll)]
            orig = os.path.join(lib, dll)
            m = lib_re.match(dll)
            if m:
                dg = m.groupdict()
                ldests.append(os.path.join(bin, 'cyg%s' % dg['dll']))
            for ldest in ldests:
                if os.path.exists(ldest):
                    os.remove(ldest)
                
                shutil.copy2(orig, ldest)
    
    
    
    