import os
import shutil
import logging
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
    mapserv = os.path.join(
        options['compile-directory'], 'mapserv')
    c = options['compile-directory']
    dmapserv = os.path.join( location, 'mapserv')
    shutil.copy(mapserv, dmapserv)
    message =  'Successfully installed mapserv into %s'
    logging.getLogger('mapserver hook').info(
        message % location)

    [shutil.copy(
        os.path.join(c,f), include
    )
        for f in os.listdir(c)
        if f.endswith('.h')]


