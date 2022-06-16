Move Figures between Groups
===========================

Moving Figures between Groups in OMERO might be necessary for example in cases where a scientist decides to move their data into another Group to enable cooperation and viewing by other colleagues or to make the data public.

As with all data in OMERO, Figures belong to a particular Group and are visible only to members of that Group. Figures can contain Images from the same Group as the Figure or from any other Group. Figures and the Images they contain can be independently moved from one Group to another but should ideally be kept in the same Group. This avoids the situation when a user can view a Figure, but not the Images within it.

This walkthrough offers two alternatives for getting Figures into another Group, either with or without duplicating the Figures and the Images contained in them.

Description
-----------

This guide covers:

- Moving of Figures and Images between Groups.
- Duplicating of Figures and Images into a new Group.

Setup
-----

-  Install the scripts :download:`Figure_Images_To_Dataset.py <../scripts/Figure_Images_To_Dataset.py>` and :download:`Dataset_Images_To_New_Figure.py <../scripts/Dataset_Images_To_New_Figure.py>`  on your OMERO.server.
-  We suggest in this workflow the installation under a folder ``Figure scripts`` but you can install the script in any folder.
-  See `server-side script guides <https://omero-guides.readthedocs.io/en/latest/scripts/docs/index.html>`__ for further details.

Resources
---------

-  Any Images and Figures created from these Images.

Step-by-Step
------------

.. _Movefigure:

*Moving of Figures and Images between Groups*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This workflow assumes that you have an OMERO.figure already created and want to move this Figure into another Group.

#.  Log in to OMERO.web.

#.  Click on ``Figure`` link above the central pane to get into OMERO.figure.

#.  Inside OMERO.figure, click ``File > Open`` and open the Figure you wish to move to another Group. Copy the last part of the url from the address bar of your browser, which contains the Figure ID, e.g.:

    https://your-omero-server.org/web/figure/file/79828

    has the Figure ID ``79828``. The Figure ID will be needed later in case you also want to collect and move the Images contained in the Figure as described below.

#.  Click ``File > Move Figure to Group...``. In the following dialog, select the Group you wish to move the Figure to and click OK.

#.  Observe a dialog reporting a success of the move. Verify that when you now again click ``File > Move Figure to Group...`` the Figure is now reported to be in your intended Group.

.. note::
      You might want to move the Images contained in the Figure to the other Group as well. This step is optional, if you want to use your Figures by yourself only, but you should consider it in case the users you want to share your Figure with do not have permissions to see your Images in the original Group (for example they are members of the target Group only).

#.  In the following steps, we first collect all the Images in the Figure into a single Dataset to enable moving them to the target Group in a single step.

#.  Go back to the tab with OMERO.web, create a new Dataset and select it.

#.  Click on the ``Scripts`` icon |image1| above the central pane of OMERO.web. Select ``Figure scripts > Figure Images to Dataset``. Start the script and in the dialog, enter the Figure ID into the Figure IDs field. If you wish to work with multiple Figures, IDs can be separated with commas, e.g. ``79828, 79830, 71228``. Click ``Run``.

#.  When the script finishes, refresh the page and find the Images contained in your Figure linked to the Dataset. Note that the Images are linked to the chosen Dataset without removing them from any existing Dataset. They will be doubly-linked but not duplicated.

#.  The above means that when you execute the Move into another Group, the Images in your Dataset will no longer be available in the original Group.

#.  Move the Images into the Group you have moved the Figure to. Be sure to select the Images in OMERO.web when moving, not the Dataset. If the Dataset is selected, the Images are left in the original Group, and only the empty Dataset is moved. This is because the Images are linked to the original Dataset which is left in the original Group. Follow `the Move workflow <https://omero-guides.readthedocs.io/en/latest/introduction/docs/data-management.html#move-data-between-groups>`__ to execute the Move. The Move will enable any member of the target Group to view both the Figure and the Images within it.

*Duplicating of Figures and Images into a new Group*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you wish to keep your Figures and the contained Images in their original Group, while also making them available to users in another Group, you can duplicate them as described below.

In this workflow, we first duplicate the Images within one or more Figures. Then move these Images to the target Group.

Finally, using a script, we copy the Figure into the target Group, replacing the Images within it with the duplicated Images.

Note that this workflow involves usage of Command Line.

#.  Collect the Images contained in the Figures into a single Dataset using the workflow :ref:`Moving of Figures...<Movefigure>`. For this, you can find out the Figure IDs either manually as described in the  :ref:`Moving of Figures...<Movefigure>` or by running hql queries on the command line, such as::

    $ omero hql --all --limit 1000 --style plain --ids-only  "select f.id from FileAnnotation f where (f.details.group.name = 'Lab1' and f.details.owner.id = 454)" | sed -e 's/^.*,//g' | paste -s -d, -

    which will retrieve all the Figure IDs of user with ID 454 in a Group ``Lab1`` in a format which you can immediately copy and paste into the ``Figure Images to Dataset`` script.

#.  Start your command line terminal and duplicate the Dataset with the Images contained in the Figures as described in `the Duplicate workflow <https://omero-guides.readthedocs.io/en/latest/introduction/docs/data-management.html#command-line-duplicating-objects>`__.

#.  Go to OMERO.web, select the duplicate Dataset and Move it to the target Group. For that, follow `the Move workflow <https://omero-guides.readthedocs.io/en/latest/introduction/docs/data-management.html#move-data-between-groups>`__.

#.  Find the Dataset which you have just moved and select it.

#.  Click on the ``Scripts`` icon |image1| above the central pane of OMERO.web. Select ``Figure scripts > Dataset Images To New Figure``. 

#.  Start the script and in the dialog, enter the Figure ID into the Figure IDs field. If you wish to work with multiple Figures, IDs can be separated with commas, e.g. ``79828, 79830, 71228``. Click ``Run``. This will copy each specified Figure, update the Images within it to those in the duplicate Dataset (using the Image name to match the replacement Images) and save the Figure to the new Group.

#.  Click on ``Figure`` link above the central pane to get into OMERO.figure.

#.  Inside OMERO.figure, click ``File > Open``. In the top-right corner of the new dialog, click on the ``Group`` dropdown and select your target Group name. Verify that the list contains the newly created Figures.


.. |image1| image:: images/scripts_icon.png
   :width: 0.36621in
   :height: 0.27231in
