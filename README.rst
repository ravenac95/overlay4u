overlay4u - Tools for dealing with overlayfs in ubuntu (Work in Progress)
=========================================================================

Simple way to create an overlayfs in ubuntu within Python.

Warnings!
---------

overlay4u requires root. Be sure you're aware of that. It's still very much a
work in progress so please use with caution and hopefully on VM that you do not
care about.

Caveats
-------

overlay4u is not currently being designed for anything but Ubuntu 12.04. At
this time that's the first priority.

Currently Working
-----------------

- Mounting works! (Not fully tested)
- Creating a table of mounted filesystems

TODO
----

- Unmounting

Possible interface examples
---------------------------

Create an overlay at dest::
    
    import overlay4u

    overlay = overlay4u.mount('dest', 'lower', 'upper')

    overlay.unmount()

If the destination already has something mounted it won't mount again::
    
    import overlay4u

    overlay1 = overlay4u.mount('dest', 'lower', 'upper')
    
    # This will throw an error.
    overlay2 = overlay4u.mount('dest', 'lower', 'upper')

That's all. It's a relatively simple tool.
