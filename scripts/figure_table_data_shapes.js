
//
// Copyright (C) 2021 University of Dundee & Open Microscopy Environment.
// All rights reserved.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// Using the browser devtools to manipulate OMERO.figure is an experimental
// feature for developers.
// N.B.: Never paste untrusted code into your browser console.
//
// This code expects an OMERO.table with an 'Shape' column to be linked
// to the Image(s) and for the Image panel to have Shapes added from
// OMERO (so that the shape.id in the figure corresponds to a Shape in OMERO).
// This code loads values from a named numerical column (see name in code)
// and sets the color of each Shape, creating a heatmap.

async function shapeData(panel) {
    const shapeIds = panel.get("shapes").map(s => s.id).filter(id => id > 0);
    console.log('shapeIds', shapeIds);
    let vals_by_shape = {};
    for (let i = 0; i < shapeIds.length; i++) {
        // Load one at a time - more reliable
        let shape_id = shapeIds[i];
        let base_url = window.location.href.split("figure")[0];
        let shape_url = base_url + `api/v0/m/shapes/${shape_id}/`;
        let shape = await fetch(shape_url).then(rsp => rsp.json());
        let roi_id = parseInt(shape.data['url:roi'].split("rois/")[1]);
        console.log("Shape ID", shape_id, "ROI ID", roi_id);
        let url = base_url + `webgateway/table/Image/${panel.get('imageId')}/query/?query=Roi-${roi_id}`;
        let r = await fetch(url).then(rsp => rsp.json());
        let colIndex = r.data?.columns?.indexOf("Sphericity");
        if (colIndex && r.data?.rows.length > 0) {
            console.log("Value", r.data.rows[0][colIndex]);
            vals_by_shape[shape_id] = r.data.rows[0][colIndex];
        }
    };
    // Once all loaded, we can calculate range and assign colours to shapes
    const values = Object.values(vals_by_shape);
    let minVal = Math.min(...values);
    let valRange = Math.max(...values) - minVal;
    console.log('min, range', minVal, valRange);
    const new_shapes = panel.get("shapes").map(shape => {
        // hide any shapes we don't have data for
        if (!vals_by_shape[shape.id]) return { ...shape, strokeWidth: 0.01 };
        let value = (vals_by_shape[shape.id] - minVal) / valRange;
        let red = parseInt(value * 255).toString(16);
        let green = (255 - parseInt(value * 255)).toString(16);
        // if e.g. "f", -> "0f"
        red = red.length == 1 ? `0` + red : red;
        green = green.length == 1 ? `0` + green : green;
        return { ...shape, strokeColor: `#${red}${green}00`, strokeWidth: 5 }
    });
    panel.set('shapes', new_shapes);
}
figureModel.getSelected().forEach(shapeData);
