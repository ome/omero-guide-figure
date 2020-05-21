#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#   Copyright (C) 2017-2018 University of Dundee. All rights reserved.

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# ------------------------------------------------------------------------------

"""
Simple FRAP plots from Ellipses on images and creates an OMERO.figure.

This an OMERO script that runs server-side.
"""

import omero
import json
from io import BytesIO

import omero.scripts as scripts
from omero.rtypes import rlong, rstring, unwrap
from omero.gateway import BlitzGateway
from omero.model import FileAnnotationI, OriginalFileI
from omero.sys import ParametersI


JSON_FILEANN_NS = "omero.web.figure.json"


def channelMarshal(channel):
    """
    Return a dict with all there is to know about a channel.

    NB: This is copied from omeroweb.webgateway.marshal.py since we don't know
    that OMERO.web is installed on same environment as scripts

    @param channel:     L{omero.gateway.ChannelWrapper}
    @return:            Dict
    """
    chan = {
            'label': channel.getLabel(),
            'color': channel.getColor().getHtml(),
            'inverted': channel.isInverted(),
            'window': {'min': channel.getWindowMin(),
                       'max': channel.getWindowMax(),
                       'start': channel.getWindowStart(),
                       'end': channel.getWindowEnd()},
            'active': False,    # channel.isActive()
        }
    lut = channel.getLut()
    if lut and len(lut) > 0:
        chan['lut'] = lut
    return chan


def get_timestamps(conn, image):
    """Return a list of times (secs) 1 for each T-index in image."""
    params = ParametersI()
    params.addLong('pid', image.getPixelsId())
    query = "from PlaneInfo as Info where"\
        " Info.theZ=0 and Info.theC=0 and pixels.id=:pid"
    info_list = conn.getQueryService().findAllByQuery(
        query, params, conn.SERVICE_OPTS)
    timemap = {}
    for info in info_list:
        t_index = info.theT.getValue()
        if info.deltaT is not None:
            delta_t = info.deltaT.getValue()
            timemap[t_index] = round(delta_t, 2)
    time_list = []
    for t in range(image.getSizeT()):
        if t in timemap:
            time_list.append(timemap[t])
    return time_list


def create_figure_file(conn, figure_json):
    """Create Figure FileAnnotation from json data."""
    figure_name = "Split View Figure"
    if len(figure_json['panels']) == 0:
        raise Exception('No Panels')
    first_img_id = figure_json['panels'][0]['imageId']

    # we store json in description field...
    description = {}
    description['name'] = figure_name
    description['imageId'] = first_img_id

    # Try to set Group context to the same as first image
    conn.SERVICE_OPTS.setOmeroGroup('-1')
    i = conn.getObject("Image", first_img_id)
    gid = i.getDetails().getGroup().getId()
    conn.SERVICE_OPTS.setOmeroGroup(gid)

    json_bytes = json.dumps(figure_json).encode('utf-8')
    file_size = len(json_bytes)
    f = BytesIO()
    f.write(json_bytes)

    update = conn.getUpdateService()
    orig_file = conn.createOriginalFileFromFileObj(
        f, '', figure_name, file_size, mimetype="application/json")
    fa = FileAnnotationI()
    fa.setFile(OriginalFileI(orig_file.getId(), False))
    fa.setNs(rstring(JSON_FILEANN_NS))
    desc = json.dumps(description)
    fa.setDescription(rstring(desc))
    fa = update.saveAndReturnObject(fa, conn.SERVICE_OPTS)
    return fa.getId().getValue()

def get_ch_label(image, ch_index):
    channel = image.getChannels()[ch_index]
    # positions are: top, left, right, leftvert, bottom, topleft, topright, bottomleft, bottomright
    return {
        "text": channel.getLabel(),
        "size": 12,
        "position": "top",
        "color": channel.getColor().getHtml()
    }

def get_scalebar_json():
    """Return JSON to add a 10 micron scalebar to bottom-right."""
    return {"show": True,
            "length": 10,
            "units": "MICROMETER",
            "position": "bottomright",
            "color": "FFFFFF",
            "show_label": True,
            "font_size": 10}


def get_panel_json(image, x, y, width, height, c_index=None):
    """Get json for a figure panel."""
    px = image.getPrimaryPixels().getPhysicalSizeX()
    py = image.getPrimaryPixels().getPhysicalSizeY()

    # channelMarshal gives us 'active':False for each channel
    channels = [channelMarshal(x) for x in image.getChannels()]

    # Just turn on 1 channel
    if c_index is not None:
        channels[c_index]['active'] = True
    else:
        # Or ALL channels (merged image)
        for c in channels:
            c['active'] = True

    img_json = {
        "imageId": image.id,
        "y": y,
        "x": x,
        "width": width,
        "height": height,
        "orig_width": image.getSizeX(),
        "orig_height": image.getSizeY(),
        "sizeT": image.getSizeT(),
        "sizeZ": image.getSizeZ(),
        "channels": channels,
        "name": image.getName(),
        "theT": image.getDefaultT(),
        "theZ": image.getDefaultZ(),
    }
    if px is not None:
        img_json["pixel_size_x"] = px.getValue()
        img_json["pixel_size_x_unit"] = str(px.getUnit())
        img_json["pixel_size_x_symbol"] = px.getSymbol()
    if py is not None:
        img_json["pixel_size_y"] = py.getValue()
    if image.getSizeT() > 1:
        img_json['deltaT'] = get_timestamps(conn, image)
    return img_json


def create_omero_figure(conn, images):
    """Create OMERO.figure from given images."""
    figure_json = {"version": 5}

    panel_width = 80
    panel_height = panel_width
    spacing = panel_width/20
    margin = 40

    panels_json = []

    for i, image in enumerate(images):
        print('image', image.id, image.name)
        panel_x = margin
        panel_y = (i * (panel_height + spacing)) + margin
        for col in range(image.getSizeC()):
            j = get_panel_json(image, panel_x, panel_y,
                               panel_width, panel_height, col)
            if i == 0:
                j['labels'] = [get_ch_label(image, col)]
            panels_json.append(j)
            panel_x += panel_width + spacing
        # Add merged panel
        j = get_panel_json(image, panel_x, panel_y,
                           panel_width, panel_height)
        panels_json.append(j)
        # Add scalebar to last panel
        panels_json[-1]['scalebar'] = get_scalebar_json()

    figure_json['panels'] = panels_json
    return create_figure_file(conn, figure_json)


if __name__ == "__main__":
    dataTypes = [rstring('Dataset'), rstring('Image')]
    client = scripts.client(
        'Split_View_Figure.py',
        """
    This script creates an OMERO.figure 'spilt-view' figure.
        """,
        scripts.String(
            "Data_Type", optional=False, grouping="1",
            description="Choose source of images",
            values=dataTypes, default="Dataset"),

        scripts.List(
            "IDs", optional=False, grouping="2",
            description="Dataset or Image IDs.").ofType(rlong(0)),

        authors=["Will Moore", "OME Team"],
        institutions=["University of Dundee"],
        contact="ome-users@lists.openmicroscopy.org.uk",
    )

    try:
        # process the list of args above.
        params = client.getInputs(unwrap=True)
        print(params)

        # wrap client to use the Blitz Gateway
        conn = BlitzGateway(client_obj=client)
        # Call the main script - returns the new OMERO.figure ann ID
        images = list(conn.getObjects('Image', params["IDs"]))
        print(f'Found {len(images)} images')
        print(images)
        if len(images) == 0:
            message = "No images found"
        else:
            figure_id = create_omero_figure(conn, images)
            message = "Created figure: %s" % figure_id

        client.setOutput("Message", rstring(message))
    except Exception:
        raise

    finally:
        client.closeSession()
