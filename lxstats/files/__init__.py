'''Read and write files under :file:`/proc` and :file:`/sys` Linux filesystems.

This module and its submoduels contain specialized classes to read, parse and
write content to different types of files under :file:`/proc` and :file:`/sys`
Linux filesystems.

Submodules are structured as follows:

 - :mod:`lxstats.files.text`: base classes for reading and writing text files.

 - :mod:`lxstats.files.types`: classes for reading and writing different types
   of files, mostly used in the :file:`/sys` filesystem.

 - :mod:`lxstats.files.proc`: classes for accessing system-wide and per-process
   statistics.

 - :mod:`lxstats.files.sys`: classes for accessing files under :file:`/sys`,
   such as debug tracing.

'''
