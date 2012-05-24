overlay4u - Tools for dealing with overlayfs in ubuntu (Work in Progress)
=========================================================================

Super simple way to create an overlayfs in ubuntu.

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
