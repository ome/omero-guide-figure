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

-  Install the scripts ``Figure Images to Dataset`` and 

Resources
---------

-  Sample images from the Image Data Resource (IDR) `idr0021 <https://idr.openmicroscopy.org/search/?query=Name:idr0021>`__.
   See `idr0021-data-prep.md <https://github.com/ome/training-scripts/blob/master/maintenance/preparation/idr0021-data-prep.md>`__
   for download and import instructions.

-  DV images from `siRNAi-HeLa <https://downloads.openmicroscopy.org/images/DV/siRNAi-HeLa/>`__.

-  SVS ‘big’ pathology images from `SVS <https://downloads.openmicroscopy.org/images/SVS/>`__.

Step-by-Step
------------

*Moving of figures using OMERO.web user interface*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#.  Log in to OMERO.web.

#.  We assume that you have an OMERO.figure already created and want to move this figure into another group.

#.  Click on ``Figure`` link above the central pane to get into OMERO.figure.

#.  Inside OMERO.figure, click ``File > Open`` and open the Figure you wish to move to another group.

#.  Click ``File > Move Figure to Group...``. In the following dialog, select the group you wish to move the Figure to and click OK.

#.  Observe a dialog reporting a success of the move. Verify that when you now again click ``File > Move Figure to Group...`` the Figure is now reported to be in your intended group.

.. note::
      You might want to move the images contained in the Figure to the other group as well. This step is optional, if you want to use your figures by yourself only, but you should consider it in case the users you want to share your figure with do not have permissions to see your images in the original group (for example they are members of the target group only).  

*Retrieval of images contained in figures using a script*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#.  Go to OMERO.figure and open the Figure. Copy the last part of the url from the address bar of your browser, which contains the Figure ID, e.g.:

    https://your-omero-server.org/web/figure/file/79828

    has the Figure ID ``79828``.

#.  Repeat the step above for all the Figures containing the images you want to move.

#.  Go back to the tab with OMERO.web, create a new Dataset and select it.

#.  Go to ``Scripts > Figure scripts`` and select the ``Figure Images to Dataset`` script |image1|. Start the script and paste into the dialog which appears your Figure IDs, separated with commas and no spaces, e.g. ``79828,79830,71228``. Click ``Run``.

#.  When the script finishes, refresh the page and find the images contained in your Figure linked to the Dataset. Note that the images are only doubly-linked to two Datasets now, and no independent copy of the images was done in this step.

#.  The above means that when you execute the Move into another group, the images in your Dataset will no longer be available in the original group.

#.  Move the images into the group you have moved the Figure to. This will enable any user permitted to see your images in the target group to view your Figure.

*Duplication of images, move and reconstitution of Figure duplicates using a script*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#.  In case you want to have both Figures and the images contained in them in both groups, the original and the target group, you can use a following workflow.

#.  Retrieve the images contained in the Figures using the workflow above. For this, you can find out the Figure IDs either manually or by running hql queries on the command line, such as::

    $ omero hql --all --limit 1000 --style plain --ids-only  "select f.id from FileAnnotation f where (f.details.group.name = 'Lab1' and f.details.owner.id = 454)" | sed -e 's/^.*,//g' | paste -s -d, -

    which will retrieve all the Figure IDs of user with ID 454 in a group ``Lab1`` in a format which you can immediately copy and paste into the ``Figure Images to Dataset`` script.


Then, select the new dataset and start Will's script. Into the dialog which appears paste the ids of the figures and the script will copy the links to your images into the Dataset. You can then choose to either duplicate the Dataset and move the duplicate into the other group (this would need an exchange of IDs later in the new group or the follow-up script) or move the images as they are. 





.. |image1| image:: images/move_fig_to_dataset.png
   :width: 0.20833in
   :height: 0.20833in
.. |image4| image:: images/image4.png
   :width: 0.36458in
   :height: 0.25in
