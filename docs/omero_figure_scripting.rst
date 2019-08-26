OMERO.figure scripting
======================

**Description:**
----------------

We can use JavaScript in the browser console to script changes to a
figure. This is an experimental feature and not documented.

**Setup:**
----------

-  Install the OMERO.figure web app as described at
      https://pypi.org/project/omero-figure/

**Resources:**

-  2 FRAP images from https://downloads.openmicroscopy.org/images/DV/will/FRAP/

**Step-by-Step:**
-----------------

To see the
data model for the current file, go to *File > Export as JSON...*.

The figureModel variable is accessible in the console. We can use AJAX
to load JSON data. In this example we will load the FRAP intensities
from the Map Annotations on these images.

1.  Select 2 FRAP images. If these images have a 

Create a Figure with 2 images from the *FRAP* Dataset.

2.  Make each image into a row of multiple time-points.

3.  Open the browser console by *right-click > Inspect Element (Firefox)* or *right-click > Inspect (Chrome)* and click on the *Console* tab.

4.  Copy the code from
       https://raw.githubusercontent.com/ome/training-scripts/v0.6.0/practical/javascript/figure_frap_mapannotation_label.js

5.  Drag to select the FRAP movie images in the figure.

6.  Paste the code into the console. **Do not hit enter yet.**

7.  Inspect the code. It will iterate through each of the **selected**
       panels, an AJAX call is made to load the map annotations with the
       namespace that we created from FRAP values above.

8.  The FRAP values are a list of [key, value] pairs and we can get the
       value for the current T index of the panel values[theT][1] and
       use this to create a label.

9.  Edit the ‘position’ of the label to ‘bottomleft’ (can change size
       and color too if desired) and hit Enter to run the code on
       selected panels.

10. The labels should be added. Note that you can undo and redo these
       changes in the UI as normal.

11. Try out other examples in
       https://github.com/ome/training-scripts/tree/v0.6.0/practical/javascript
