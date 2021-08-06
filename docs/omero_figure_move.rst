Move figures between groups
===========================

Moving figures between groups in OMERO might be necessary for example in cases where a scientist decides to move all their data into another group to enable cooperation and viewing by other colleagues or to a group which is to be made public later. This walkthrough offers two alternatives, with or without duplicating the figures and the images contained in them.

Description
-----------

This guide covers:

- Manual moving of figures using user interface.
- Duplicating and moving of figures using a script. 

Setup
-----

-  Install the script...

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

#.  (optional) You might want to move the images contained in the Figure to the other group as well. For that, crate a new Dataset. Then, find out the figure ids by running

omero hql --all --limit 1000 --style plain --ids-only  "select f.id from FileAnnotation f where (f.details.group.name = 'read-only-1' and f.details.owner.id = 454)" | sed -e 's/^.*,//g' | paste -s -d, -

Then, select the new dataset and start Will's script. Into the dialog which appears paste the ids of the figures and the script will copy the links to your images into the Dataset. You can then choose to either duplicate the Dataset and move the duplicate into the other group (this would need an exchange of IDs later in the new group or the follow-up script) or move the images as they are. 





.. |image2| image:: images/image2.png
   :width: 0.20833in
   :height: 0.20833in
.. |image4| image:: images/image4.png
   :width: 0.36458in
   :height: 0.25in
