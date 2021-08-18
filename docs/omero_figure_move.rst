Move figures between groups
===========================

Moving figures between groups in OMERO might be necessary for example in cases where a scientist decides to move all their data into another group to enable cooperation and viewing by other colleagues or to a group which is to be made public later. This walkthrough offers two alternatives, with or without duplicating the figures and the images contained in them.

Description
-----------

This guide covers:

- Manual moving of figures using user interface.
- Retrieval of all the images contained in a Figure.
- Duplicating of images contained in a Figure, moving them and re-creating Figure duplicates in the target group. 

Setup
-----

-  Install the scripts :download:`Figure_Images_To_Dataset.py <../scripts/Figure_Images_To_Dataset.py>` and :download:`Dataset_Images_To_New_Figure.py <../scripts/Dataset_Images_To_New_Figure.py>`  on your OMERO.server.
-  We suggest in this workflow the installation under a folder ``Figure scripts`` but you can install the script in any folder.
-  See `server-side script guides <https://omero-guides.readthedocs.io/en/latest/scripts/docs/index.html>`__ for further details.

Resources
---------

-  Any images and Figures created from these images.

Step-by-Step
------------

*Moving of figures using OMERO.web user interface*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow assumes that you have an OMERO.figure already created and want to move this figure into another group.

#.  Log in to OMERO.web.

#.  Click on ``Figure`` link above the central pane to get into OMERO.figure.

#.  Inside OMERO.figure, click ``File > Open`` and open the Figure you wish to move to another group.

#.  Click ``File > Move Figure to Group...``. In the following dialog, select the group you wish to move the Figure to and click OK.

#.  Observe a dialog reporting a success of the move. Verify that when you now again click ``File > Move Figure to Group...`` the Figure is now reported to be in your intended group.

.. note::
      You might want to move the images contained in the Figure to the other group as well. This step is optional, if you want to use your figures by yourself only, but you should consider it in case the users you want to share your figure with do not have permissions to see your images in the original group (for example they are members of the target group only).  

.. _Retrieval:

*Retrieval of images contained in figures using a script*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#.  Go to OMERO.figure and open the Figure. Copy the last part of the url from the address bar of your browser, which contains the Figure ID, e.g.:

    https://your-omero-server.org/web/figure/file/79828

    has the Figure ID ``79828``.

#.  Repeat the step above for all the Figures containing the images you want to move. Retain the Figure IDs (for example saving them as a text document) for later use.

#.  Go back to the tab with OMERO.web, create a new Dataset and select it.

#.  Click on the ``Scripts`` icon |image1| above the central pane of OMERO.web. Select ``Figure scripts > Figure Images to Dataset``. Start the script and paste into the dialog which appears your Figure IDs, separated with commas and no spaces, e.g. ``79828,79830,71228``. Click ``Run``.

#.  When the script finishes, refresh the page and find the images contained in your Figure linked to the Dataset. Note that the images are only doubly-linked to two Datasets now, and no independent copy of the images was done in this step.

#.  The above means that when you execute the Move into another group, the images in your Dataset will no longer be available in the original group.

#.  Move the images into the group you have moved the Figure to. This will enable any user permitted to see your images in the target group to view your Figure.

*Duplication of images, move and re-create Figure(s) in the new group using a script*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case you want to have both Figures and the images contained in them in both groups, the original and the target group, you can use following workflow. Note that this workflow involves usage of Command Line.

#.  Retrieve the images contained in the Figures using the workflow above. For this, you can find out the Figure IDs either manually as described in the chapter :ref:`Retrieval<Retrieval>` or by running hql queries on the command line, such as::

    $ omero hql --all --limit 1000 --style plain --ids-only  "select f.id from FileAnnotation f where (f.details.group.name = 'Lab1' and f.details.owner.id = 454)" | sed -e 's/^.*,//g' | paste -s -d, -

    which will retrieve all the Figure IDs of user with ID 454 in a group ``Lab1`` in a format which you can immediately copy and paste into the ``Figure Images to Dataset`` script.

#.  Start your command line terminal and duplicate the Dataset with the images contained in the Figures as described in `the Duplicate workflow <https://omero-guides.readthedocs.io/en/latest/introduction/docs/data-management.html#command-line-duplicating-objects>`__.

#.  Go to OMERO.web, select the duplicate Dataset and Move it to the target group. For that, follow `the Move workflow <https://omero-guides.readthedocs.io/en/latest/introduction/docs/data-management.html#move-data-between-groups>`__.

#.  Find the Dataset which you have just moved and select it.

#.  Click on the ``Scripts`` icon |image1| above the central pane of OMERO.web. Select ``Figure scripts > Dataset Images To New Figure``. 

#.  Into the dialog which appears paste your Figure IDs, separated with commas and no spaces, e.g. ``79828,79830,71228``. Click ``Run``.

#.  Click on ``Figure`` link above the central pane to get into OMERO.figure.

#.  Inside OMERO.figure, click ``File > Open``. In the top-right corner of the new dialog, click on the ``Group`` dropdown and select your target group name. Verify that the list contains the newly created figures. 


.. |image1| image:: images/scripts_icon.png
   :width: 0.36621in
   :height: 0.27231in
