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
    location = os.path.join(
        options['location'], 'bin')
    if not os.path.isdir(location):
        os.makedirs(location)
    mapserv = os.path.join(
        options['compile-directory'], 'mapserv')
    dmapserv = os.path.join( location, 'mapserv')
    shutil.copy(mapserv, dmapserv)
    message =  'Successfully installed mapserv into %s'
    logging.getLogger('mapserver hook').info(
        message % location)



